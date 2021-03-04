from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage

from .decorators import unauthenticated_user
from .logic import *
from .models import TugasProyek, TugasRutin, IsiTugasRutin, DataKaryawan

from django.utils import timezone
from datetime import datetime, timedelta
import pytz

from django.http import HttpResponse

# Create your views here.

def test_webhook(request):
    data = request.POST
    context = {'data' : data}
    return render(request, 'test_webhook.html', context)

@login_required(login_url='login')
def index(request):
    ngecekdeadline()
    if request.user.groups.filter(name='Eksekutif').exists():
        return redirect('eksekutif')
    elif request.user.groups.filter(name='Manager').exists():
        return redirect('manager')
    elif request.user.groups.filter(name='CEO').exists():
        return redirect('ceo')
    else:
        return redirect('logout')


@unauthenticated_user
def loginpage(request):
    ngecekdeadline()

    context = {}
 
    # jika metode request adalah post
    if request.method == 'POST':
        # ambil username dan passwordnya
        username = request.POST.get('username')
        password = request.POST.get('password')

        # autentifikasi usernya
        user = authenticate(request, username=username, password=password)

        # kalau user berhasil diautentifikasi, login
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'username atau password salah')
            return render(request, 'login.html', context)

    return render(request, 'login.html', context)

def logoutuser(request):
    # ini halaman logout
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):

    context = {}

    usr = User.objects.get(pk=request.user.id)
    username = usr.username
    nama = request.user.first_name
    context = {'nama': nama, 'username': username}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if request.method == 'POST':
        name = request.POST.get('nama_lengkap')
        username = request.POST.get('username')
        password = request.POST.get('password')
        usr.username = username
        usr.first_name = name        
        usr.set_password(password)
        usr.save()

        return redirect('index')

    return render(request, 'profile.html', context)


# ------------------------------- KLASEMEN ----------------------------------
@login_required(login_url='login')
def klasemen(request):

    nama = request.user.first_name
    bagian = request.user.last_name
    usr = User.objects.all()

    id_terlarang = [1, 5, 17, 18, 19]
    user = []

    for a in usr:
        if a.id not in id_terlarang:
            user.append((a,hitungskor(a.id)))

    user.sort(key=lambda tup: tup[1])
    user = user[::-1]

    context = {'bagian': bagian, 'nama': nama, 'usr' : user}

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'klasemen.html', context)

# ------------------------------- CEO ----------------------------------

@login_required(login_url='login')
def index_ceo(request):
    
    ngecekdeadline()
    nama = request.user.first_name
    context = {
        'nama': nama,
        'data_kar' : True,
    }

    if request.user.groups.filter(name='Eksekutif').exists() or request.user.groups.filter(name='Manager').exists():
        context['data_kar'] = False
        return redirect('logout')

    return render(request, 'ceo/index.html', context)


@login_required(login_url='login')
def daftar_manager(request):
    
    ngecekdeadline()
    nama = request.user.first_name
    context = {
        'nama': nama,
        'data_kar' : True,
        'anggota' : User.objects.filter(groups__name='Manager')
    }
    # anggota = anggotabagian(nama, bagian)
    # print(anggota)

    if request.user.groups.filter(name='Eksekutif').exists() or request.user.groups.filter(name='Manager').exists():
        context['data_kar'] = False
        return redirect('logout')

    return render(request, 'ceo/manager.html', context)

# ------------------------------- MANAGER ----------------------------------

@login_required(login_url='login')
def manager(request):
    
    ngecekdeadline()
    nama = request.user.first_name
    context = {'nama': nama}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'manager/home.html', context)

@login_required(login_url='login')
def registrasi_eksekutif(request):

    nama = request.user.first_name
    bagian = request.user.last_name

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username, '', password)
        user.first_name = request.POST['nama_lengkap']
        user.last_name = request.POST['bagian']
        user.save()

        grup_staff = Group.objects.get(name='Eksekutif')
        grup_staff.user_set.add(user)

        return redirect('daftar_eksekutif')

    else:
        context = {'bagian': bagian, 'nama': nama}
        if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
            context['data_kar'] = True

    return render(request, 'manager/registrasi_eksekutif.html', context)

@login_required(login_url='login')
def daftar_eksekutif(request):
    
    nama = request.user.first_name
    bagian = request.user.last_name
    anggota = anggotabagian(nama, bagian)

    context = {'nama': nama, 'anggota': anggota}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'manager/daftar_eksekutif.html', context)

@login_required(login_url='login')
def input_tugas_proyek(request, id_eksekutif):

    nama = request.user.first_name
    context = {'nama' : nama}

    ceo = request.user.groups.filter(name='CEO').exists()

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if ceo:
        context['sidebar_ceo'] = True

    if request.method == 'POST':
        data_judul = request.POST.get('judul')
        data_isi = request.POST.get('isi')
        data_deadline = request.POST.get('deadline')
        
        if ceo:
            t = TugasProyek(
                pemilik_tugas = User.objects.get(pk=id_eksekutif),
                judul = data_judul,
                isi = data_isi,
                deadline = data_deadline,
                status = 'On Progress',
                bagian = 'Management',
                bukti = '#'
            )
        else:
            t = TugasProyek(
                pemilik_tugas = User.objects.get(pk=id_eksekutif),
                judul = data_judul,
                isi = data_isi,
                deadline = data_deadline,
                status = 'On Progress',
                bagian = request.user.last_name,
                bukti = '#'
            )
        t.save()
        return redirect('lihat_tugas')

    return render(request, 'manager/input_tugas_proyek.html', context)


@login_required(login_url='login')
def input_tugas_rutin(request, id_eksekutif):

    ceo = request.user.groups.filter(name='CEO').exists()

    if request.method == 'POST':
        object_eksekutif = User.objects.get(pk=id_eksekutif)

        data_judul = request.POST.get('judul')
        data_isi = request.POST.get('isi')
        data_mulai = request.POST.get('mulai')
        data_selesai = request.POST.get('selesai')

        if ceo:
            tgs_rutin = TugasRutin(
                pemilik_tugas= object_eksekutif, 
                judul=data_judul,
                isi = data_isi,
                bagian = 'Management',
            )
        else:
            tgs_rutin = TugasRutin(
                pemilik_tugas= object_eksekutif, 
                judul=data_judul,
                isi = data_isi,
                bagian = request.user.last_name,
            )
        tgs_rutin.save()

        data_mulai += "T18:00"
        data_selesai += "T18:00"

        objek_tugas = TugasRutin.objects.get(pk=tgs_rutin.id)
        statusnya = "On Progress"

        d_dikerjakan_dari = datetime.fromisoformat(data_mulai)
        d_dikerjakan_sampai = datetime.fromisoformat(data_selesai)

        d_dikerjakan_dari_utc = d_dikerjakan_dari.astimezone(pytz.utc)
        # d_dikerjakan_sampai_utc = d_dikerjakan_sampai.astimezone(pytz.utc)

        selisih = d_dikerjakan_sampai - d_dikerjakan_dari
        banyak_hari = selisih.days + 1

        tanggal = d_dikerjakan_dari_utc

        for i in range(banyak_hari):
            isitgs_rutin = IsiTugasRutin(
                tugas_rutin = objek_tugas,
                deadline = tanggal,
                status = statusnya,
                judul = data_judul,
                isi = data_isi
            )

            isitgs_rutin.save()
            tanggal += timedelta(days=1)

        return redirect('lihat_tugas')

    nama = request.user.first_name
    context = {'nama' : nama}

    if ceo:
        context['sidebar_ceo'] = True 

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'manager/input_tugas_rutin.html', context)


@login_required(login_url='login')
def lihat_tugas(request):

    ceo = request.user.groups.filter(name='CEO').exists()

    ngecekdeadline()
    nama = request.user.first_name
    context = {'nama' : nama}

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if ceo:
        context['sidebar_ceo'] = True

    # tugas proyek

    if ceo:
        tp = TugasProyek.objects.filter(bagian='Management').exclude(status='Tuntas')
        tr = TugasRutin.objects.filter(bagian='Management')
    else:
        tp = TugasProyek.objects.filter(bagian=request.user.last_name).exclude(status='Tuntas')
        tr = TugasRutin.objects.filter(bagian=request.user.last_name)

    context['tugas_proyek'] = tp
    context['tugas_rutin'] = tr

    return render(request, 'manager/lihat_tugas.html', context)


@login_required(login_url='login')
def lihat_tugas_tuntas(request):

    nama = request.user.first_name
    context = {'nama' : nama}
    ceo = request.user.groups.filter(name='CEO').exists()

    if ceo:
        context['sidebar_ceo'] = True

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    
    if ceo:
        tp = TugasProyek.objects.filter(bagian='Management', status='Tuntas')
    else:
        tp = TugasProyek.objects.filter(bagian=request.user.last_name, status='Tuntas')
    
    # tr = TugasRutin.objects.filter(bagian=request.user.last_name, status='Tuntas')
    context['tugas_proyek'] = tp
    # context['tugas_rutin'] = tr

    return render(request, 'manager/lihat_tugas_tuntas.html', context)


@login_required(login_url='login')
def progress_tugas_rutin(request, id_tugas):

    nama = request.user.first_name
    context = {'nama' : nama}

    ceo = request.user.groups.filter(name='CEO').exists()

    if ceo:
        context['sidebar_ceo'] = True

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    # objek tugas rutin
    t = TugasRutin.objects.get(pk=id_tugas)

    tr = IsiTugasRutin.objects.filter(tugas_rutin=t)
    context['tugas_rutin'] = tr
    context['judul'] = t.judul
    context['isi'] = t.isi

    return render(request, 'manager/progress_tugas_rutin.html', context)


@login_required(login_url='login')
def mdetail_rutin(request, id_tugas):

    nama = request.user.first_name
    context = {'nama' : nama}

    ceo = request.user.groups.filter(name='CEO').exists()

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if ceo:
        context['sidebar_ceo'] = True

    t = IsiTugasRutin.objects.get(pk=id_tugas)
    context['tugas'] = t

    if t.status == 'Tuntas':
        context['tuntas'] = True

    if not (t.link_bukti == '#') or (t.link_bukti == None):
        context['ada_link'] = True

    return render(request, 'manager/mdetail_rutin.html', context)


@login_required(login_url='login')
def delete_eksekutif(request, id_eksekutif):

    u = User.objects.get(pk=id_eksekutif)
    u.delete()
    
    return redirect('daftar_eksekutif')


@login_required(login_url='login')
def mdetail_proyek(request, id_tugas):

    nama = request.user.first_name
    t = TugasProyek.objects.get(pk=id_tugas)
    dokumennya = t.bukti

    if (t.status == 'Tuntas'):
        nottuntas = False
    else:
        nottuntas = True

    ceo = request.user.groups.filter(name='CEO').exists()

    context = {'nama' : nama,
                'tugas' : t,
                'dokumen' : dokumennya,
                'nottuntas' : nottuntas
                }

    if ceo:
        context['sidebar_ceo'] = True

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if t.bukti == '#':
        context['belum'] = True
    if t.status == 'Tuntas':
        context['tuntas'] = True

    if not (t.link_bukti == '#') or (t.link_bukti == None):
        context['ada_link'] = True

    return render(request, 'manager/mdetail_proyek.html', context)


@login_required(login_url='login')
def tuntas(request, id_tugas):
    
    if request.method == 'POST':
        t = TugasProyek.objects.get(pk=id_tugas)
        t.komentar = request.POST.get('komentar')
        t.penilaian = request.POST.get('penilaian')
        t.status = 'Tuntas'
        t.save()

        return redirect('lihat_tugas')

    nama = request.user.first_name
    t = TugasProyek.objects.get(pk=id_tugas)
    dokumennya = t.bukti

    context = {'nama' : nama, 
                'tugas' : t,
                'dokumen' : dokumennya,
                'tuntas' : tuntas
                }

    ceo = request.user.groups.filter(name='CEO').exists()

    if ceo:
        context['sidebar_ceo'] = True

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if t.bukti == '#':
        context['belum'] = True

    return render(request, 'manager/proyek_tuntas.html', context)


@login_required(login_url='login')
def rutin_tuntas(request, id_tugas):
    
    if request.method == 'POST':
        t = IsiTugasRutin.objects.get(pk=id_tugas)
        t.komentar = request.POST.get('komentar')
        t.penilaian = request.POST.get('penilaian')
        t.status = 'Tuntas'
        t.save()

        return mdetail_rutin(request, id_tugas)

    nama = request.user.first_name
    t = IsiTugasRutin.objects.get(pk=id_tugas)
    dokumennya = t.bukti
    ceo = request.user.groups.filter(name='CEO').exists()

    context = {'nama' : nama, 'tugas' : t, 'dokumen' : dokumennya}

    if ceo:
        context['sidebar_ceo'] = True

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if t.bukti == '#':
        context['belum'] = True

    return render(request, 'manager/rutin_tuntas.html', context)


@login_required(login_url='login')
def edit_tugas_proyek(request, id_tugas):

    if request.method == 'POST':
        data_judul = request.POST.get('judul')
        data_isi = request.POST.get('isi')
        data_deadline = request.POST.get('deadline')
        data_status = request.POST.get('status')

        t = TugasProyek.objects.get(pk=id_tugas)
        t.judul = data_judul
        t.isi = data_isi
        t.deadline = data_deadline
        t.status = data_status
        t.save()

        return mdetail_proyek(request, id_tugas)    

    nama = request.user.first_name
    t = TugasProyek.objects.get(pk=id_tugas)
    context = {'nama' : nama, 'tugas' : t}

    ceo = request.user.groups.filter(name='CEO').exists()

    if ceo:
            context['sidebar_ceo'] = True

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if t.status == 'Tuntas':
        context['tuntas'] = True
    elif t.status == 'Hold':
        context['hold'] = True
    elif t.status == 'On Progress':
        context['progress'] = True
    elif t.status == 'Selesai':
        context['selesai'] = True
    elif t.status == 'Deadline':
        context['deadline'] = True

    return render(request, 'manager/edit_tugas_proyek.html', context)


@login_required(login_url='login')
def edit_tugas_rutin(request, id_tugas):
    
    if request.method == 'POST':
        data_judul = request.POST.get('judul')
        data_isi = request.POST.get('isi')
        data_deadline = request.POST.get('deadline')
        data_status = request.POST.get('status')

        t = IsiTugasRutin.objects.get(pk=id_tugas)
        t.judul = data_judul
        t.isi = data_isi
        t.deadline = data_deadline
        t.status = data_status
        t.save()

        return mdetail_rutin(request, id_tugas)

    nama = request.user.first_name
    t = IsiTugasRutin.objects.get(pk=id_tugas)
    ceo = request.user.groups.filter(name='CEO').exists()

    context = {'nama' : nama, 'tugas' : t}

    if ceo:
        context['sidebar_ceo'] = True

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    
    if t.status == 'Tuntas':
        context['tuntas'] = True
    elif t.status == 'Hold':
        context['hold'] = True
    elif t.status == 'On Progress':
        context['progress'] = True
    elif t.status == 'Selesai':
        context['selesai'] = True
    elif t.status == 'Deadline':
        context['deadline'] = True

    return render(request, 'manager/edit_tugas_rutin.html', context)

@login_required(login_url='login')
def tugas_aktif_manager(request):

    ngecekdeadline()
    objek_user = User.objects.get(pk=request.user.id)
    t = TugasProyek.objects.filter(pemilik_tugas=objek_user).exclude(status="Tuntas")
    tr = TugasRutin.objects.filter(pemilik_tugas=objek_user)

    nama = request.user.first_name
    context = {'nama' : nama, 'tugas_proyek' : t, 'tugas_rutin':tr}  

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'manager/tugas_aktif_manager.html', context)

@login_required(login_url='login')
def tugas_tuntas_manager(request):

    ngecekdeadline()
    nama = request.user.first_name
    objek_user = User.objects.get(pk=request.user.id)
    t = TugasProyek.objects.filter(pemilik_tugas=objek_user, status="Tuntas")

    context = {'nama' : nama, 'tugas_proyek' : t}

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'manager/tugas_tuntas_manager.html', context)

# --------------------------- eksekutif ----------------------------------

@login_required(login_url='login')
def eksekutif(request):
    
    nama = request.user.first_name
    context = {'nama' : nama}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'eksekutif/home.html', context)


@login_required(login_url='login')
def daftar_tugas(request):

    nama = request.user.first_name

    ngecekdeadline()
    objek_user = User.objects.get(pk=request.user.id)
    t = TugasProyek.objects.filter(pemilik_tugas=objek_user).exclude(status="Tuntas")
    tr = TugasRutin.objects.filter(pemilik_tugas=objek_user)

    context = {'nama' : nama, 'tugas_proyek' : t, 'tugas_rutin':tr}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'eksekutif/daftar_tugas.html', context)


@login_required(login_url='login')
def tugas_tuntas(request):

    nama = request.user.first_name
    ngecekdeadline()
    objek_user = User.objects.get(pk=request.user.id)
    t = TugasProyek.objects.filter(pemilik_tugas=objek_user, status="Tuntas")

    context = {'nama' : nama, 'tugas_proyek' : t}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'eksekutif/tugas_tuntas.html', context)

@login_required(login_url='login')
def daftar_tugas_rutin(request, id_tugas):

    nama = request.user.first_name
    t = TugasRutin.objects.get(pk=id_tugas)
    tr = IsiTugasRutin.objects.filter(tugas_rutin=t)
    manager = request.user.groups.filter(name='Manager').exists()

    context = {'nama' : nama, 'judul' : t.judul, 'isi' : t.isi, 'tugas_rutin' : tr}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if manager:
        context['sidebar_manager'] = True

    return render(request, 'eksekutif/daftar_tugas_rutin.html', context)


@login_required(login_url='login')
def detail_tugas_proyek(request, id_tugas):
    nama = request.user.first_name

    t = TugasProyek.objects.get(pk=id_tugas)
    manager = request.user.groups.filter(name='Manager').exists()

    context = {'nama' : nama, 'tugas' : t}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if t.status == 'Tuntas':
        context['tuntas'] = True
    
    if manager:
        context['sidebar_manager'] = True

    return render(request, 'eksekutif/detail_tugas_proyek.html', context)

@login_required(login_url='login')
def upload_dokumentasi_tp(request, id_tugas):

    manager = request.user.groups.filter(name='Manager').exists()

    if request.method == 'POST':

        t = TugasProyek.objects.get(pk=id_tugas)

        if request.POST.get('pilihan') == 'dokumen':
            uploaded_file = request.FILES['dokumen']
            fs = FileSystemStorage()
            nama = fs.save(uploaded_file.name, uploaded_file)
            alamat = fs.url(nama)
            t.bukti = alamat
            t.link_bukti = '#'
        else:
            t.link_bukti = request.POST.get('linkbukti')       
        
        t.selesai_pada = datetime.now()

        if t.status == 'Deadline':
            t.status = 'Terlambat'
        else:
            t.status = 'Selesai'

        t.save()
        if manager:
            return redirect('tugas_aktif_manager')
        else:
            return redirect('daftar_tugas')

    nama = request.user.first_name
    context = {'nama' : nama}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    if manager:
        context['sidebar_manager'] = True

    return render(request, 'eksekutif/upload_dokumentasi_tp.html', context)


@login_required(login_url='login')
def upload_dokumentasi_tr(request, id_tugas):

    manager = request.user.groups.filter(name='Manager').exists()

    if request.method == 'POST':

        t = IsiTugasRutin.objects.get(pk=id_tugas)
        fs = FileSystemStorage()

        if request.POST.get('pilihan') == 'dokumen':
            uploaded_file = request.FILES['dokumen']
            nama = fs.save(uploaded_file.name, uploaded_file)
            alamat = fs.url(nama)
            t.bukti = alamat
            t.link_bukti = '#'
            alamat = fs.url(nama)
            t.bukti = alamat
        else:
            t.link_bukti = request.POST.get('linkbukti')

        t.selesai_pada = datetime.now()
        
        if t.status == 'Deadline':
            t.status = 'Terlambat'
        else:
            t.status = 'Selesai'
        
        t.save()

        if manager:
            return redirect('tugas_aktif_manager')
        else:
            return daftar_tugas_rutin(request, t.tugas_rutin.id)

    nama = request.user.first_name
    context = {'nama' : nama}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    if manager:
        context['sidebar_manager'] = True

    return render(request, 'eksekutif/upload_dokumentasi_tr.html', context)

    # ---------------------- DATA KARYAWAN -----------------------

@login_required(login_url='login')
def data_karyawan(request):
    
    d = DataKaryawan.objects.filter(status='AKTIF')
    
    context = {'nama' : request.user.first_name, 'data' : d}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    
    return render(request, 'data_karyawan/index.html', context)


@login_required(login_url='login')
def tambah_data_karyawan(request):

    if request.method == 'POST':
        dno_id_fingerprint = request.POST.get('no_id_fingerprint')
        dnama = request.POST.get('nama')
        darea = request.POST.get('area')
        dlevel_manajemen = request.POST.get('level_manajemen')
        dnama_posisi = request.POST.get('nama_posisi')
        dkode_posisi = request.POST.get('kode_posisi')
        dstatus_jabatan = request.POST.get('status_jabatan')
        djabatan_baru = request.POST.get('jabatan_baru')
        dstatus_pegawai = request.POST.get('status_pegawai')
        dtanggal_masuk = request.POST.get('tanggal_masuk')
        dno_ktp = request.POST.get('no_ktp')
        dtempat_lahir = request.POST.get('tempat_lahir')
        dtanggal_lahir = request.POST.get('tanggal_lahir')
        djenis_kelamin = request.POST.get('jenis_kelamin')
        dagama = request.POST.get('agama')
        dpendidikan = request.POST.get('pendidikan')
        djurusan = request.POST.get('jurusan')
        dalamat = request.POST.get('alamat')
        dno_hp = request.POST.get('no_hp')
        dmarital_status = request.POST.get('marital_status')
        danak = request.POST.get('anak')
        dno_rekening = request.POST.get('no_rekening')
        dbpjs_ketenagakerjaan = request.POST.get('bpjs_ketenagakerjaan')
        dstatus = "AKTIF"
        
        # -------------------------------------------------------------
        # darurat
        dnama_darurat = request.POST.get('nama_darurat')
        dalamat_darurat = request.POST.get('alamat_darurat')
        dhubungan_darurat = request.POST.get('hubungan_darurat')
        dno_hp_darurat = request.POST.get('no_hp_darurat')

        d = DataKaryawan(
            no_id_fingerprint = dno_id_fingerprint,
            nama = dnama,
            area = darea,
            level_manajemen = dlevel_manajemen,
            nama_posisi = dnama_posisi,
            kode_posisi = dkode_posisi,
            status_jabatan = dstatus_jabatan,
            jabatan_baru = djabatan_baru,
            status_pegawai = dstatus_pegawai,
            tanggal_masuk = dtanggal_masuk,
            no_ktp = dno_ktp,
            tempat_lahir = dtempat_lahir,
            tanggal_lahir = dtanggal_lahir,
            jenis_kelamin = djenis_kelamin,
            agama = dagama,
            pendidikan = dpendidikan,
            jurusan = djurusan,
            alamat = dalamat,
            no_hp = dno_hp,
            marital_status = dmarital_status,
            anak = danak,
            no_rekening = dno_rekening,
            bpjs_ketenagakerjaan = dbpjs_ketenagakerjaan,
            status = dstatus,
            nama_darurat = dnama_darurat,
            alamat_darurat = dalamat_darurat,
            hubungan_darurat = dhubungan_darurat,
            no_hp_darurat = dno_hp_darurat,
        )
        d.save()
        d.pasang_nik()
        d.inisialisasi()
        d.save()
        return redirect('data_karyawan')

    context = {'nama' : request.user.first_name}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'data_karyawan/tambah_data_karyawan.html', context)


@login_required(login_url='login')
def detail_data(request, id_karyawan):
    
    context = {}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    data = DataKaryawan.objects.get(pk=id_karyawan)
    data.update_data()

    if data.status == 'AKTIF':
        context['masih_aktif'] = True

    context['nama'] = request.user.first_name
    context['data_kar'] = True
    context['data'] = data

    return render(request, 'data_karyawan/detail.html', context)


@login_required(login_url='login')
def karyawan_tidak_aktif(request):

    d = DataKaryawan.objects.filter(status='KELUAR')
    
    context = {'nama' : request.user.first_name, 'data' : d}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'data_karyawan/karyawan_tidak_aktif.html', context)


@login_required(login_url='login')
def karyawan_keluar(request, id_karyawan):

    context = {'nama' : request.user.first_name}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if request.method == 'POST':
        data = DataKaryawan.objects.get(pk=id_karyawan)
        data.tanggal_keluar = request.POST.get('tanggal_keluar')
        data.alasan_keluar = request.POST.get('alasan_keluar')
        data.status = 'KELUAR'
        data.save()

        return redirect('data_karyawan')

    return render(request, 'data_karyawan/karyawan_keluar.html', context)


@login_required(login_url='login')
def halaman_edit(request, id_karyawan):

    d = DataKaryawan.objects.get(pk=id_karyawan)

    context = {'nama' : request.user.first_name, 'data' : d}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if d.area == 'Office':
        context['area_office'] = True
    elif d.area == 'Cisitu':
        context['area_cisitu'] = True
    elif d.area == 'Jatinangor':
        context['area_jatinangor'] = True
    elif d.area == 'Metro':
        context['area_metro'] = True
    elif d.area == 'Sukajadi':
        context['area_sukajadi'] = True
    elif d.area == 'Telkom Sukabirus':
        context['area_telkom_sukabirus'] = True
    elif d.area == 'Telkom Sukapura':
        context['area_telkom_sukapura'] = True
    elif d.area == 'Unjani':
        context['area_unjadi'] = True

    if d.jenis_kelamin == 'L':
        context['lakilaki'] = True

    if d.pendidikan == 'SD':
        context['pendidikan_sd'] = True
    elif d.pendidikan == 'SMP':
        context['pendidikan_smp'] = True
    elif d.pendidikan == 'SMA/SMK':
        context['pendidikan_sma'] = True
    elif d.pendidikan == 'D3':
        context['pendidikan_d3'] = True
    elif d.pendidikan == 'S1':
        context['pendidikan_s1'] = True
    elif d.pendidikan == 'S2':
        context['pendidikan_s2'] = True
    elif d.pendidikan == 'S3':
        context['pendidikan_s3'] = True

    if d.marital_status == 'BELUM MENIKAH':
        context['status_belum'] = True
    elif d.marital_status == 'MENIKAH':
        context['status_menikah'] = True
    elif d.marital_status == 'CERAI':
        context['status_cerai'] = True

    if d.status == 'AKTIF':
        context['status_aktif'] = True

    if request.method == 'POST':
        dno_id_fingerprint = request.POST.get('no_id_fingerprint')
        dnama = request.POST.get('nama')
        darea = request.POST.get('area')
        dlevel_manajemen = request.POST.get('level_manajemen')
        dnama_posisi = request.POST.get('nama_posisi')
        dkode_posisi = request.POST.get('kode_posisi')
        dstatus_jabatan = request.POST.get('status_jabatan')
        djabatan_baru = request.POST.get('jabatan_baru')
        dstatus_pegawai = request.POST.get('status_pegawai')
        dtanggal_masuk = request.POST.get('tanggal_masuk')
        dno_ktp = request.POST.get('no_ktp')
        dtempat_lahir = request.POST.get('tempat_lahir')
        dtanggal_lahir = request.POST.get('tanggal_lahir')
        djenis_kelamin = request.POST.get('jenis_kelamin')
        dagama = request.POST.get('agama')
        dpendidikan = request.POST.get('pendidikan')
        djurusan = request.POST.get('jurusan')
        dalamat = request.POST.get('alamat')
        dno_hp = request.POST.get('no_hp')
        dmarital_status = request.POST.get('marital_status')
        danak = request.POST.get('anak')
        dno_rekening = request.POST.get('no_rekening')
        dbpjs_ketenagakerjaan = request.POST.get('bpjs_ketenagakerjaan')
        dstatus = request.POST.get('status')
        
        # -------------------------------------------------------------
        # darurat
        dnama_darurat = request.POST.get('nama_darurat')
        dalamat_darurat = request.POST.get('alamat_darurat')
        dhubungan_darurat = request.POST.get('hubungan_darurat')
        dno_hp_darurat = request.POST.get('no_hp_darurat')

        d.no_id_fingerprint = int(dno_id_fingerprint)
        d.nama = dnama
        d.area = darea
        d.level_manajemen = dlevel_manajemen
        d.nama_posisi = dnama_posisi
        d.kode_posisi = dkode_posisi
        d.status_jabatan = dstatus_jabatan
        d.jabatan_baru = djabatan_baru
        d.status_pegawai = dstatus_pegawai
        d.tanggal_masuk = dtanggal_masuk
        d.no_ktp = dno_ktp
        d.tempat_lahir = dtempat_lahir
        d.tanggal_lahir = dtanggal_lahir
        d.jenis_kelamin = djenis_kelamin
        d.agama = dagama
        d.pendidikan = dpendidikan
        d.jurusan = djurusan
        d.alamat = dalamat
        d.no_hp = dno_hp
        d.marital_status = dmarital_status
        d.anak = danak
        d.no_rekening = dno_rekening
        d.bpjs_ketenagakerjaan = dbpjs_ketenagakerjaan
        d.status = dstatus
        d.nama_darurat = dnama_darurat
        d.alamat_darurat = dalamat_darurat
        d.hubungan_darurat = dhubungan_darurat
        d.no_hp_darurat = dno_hp_darurat
        
        d.save()
        d.inisialisasi()
        d.save()
        return redirect('data_karyawan')

    return render(request, 'data_karyawan/halaman_edit.html', context)


# ---------------------- LOGIC -------------------------------

def ngecekdeadline():
    tugas = TugasProyek.objects.all()
    for a in tugas:
        deadline = a.deadline
        saat_ini = timezone.now()
        apakah_deadline = (deadline - saat_ini)
        if (apakah_deadline.days < 0) and (a.status == 'On Progress'):
            a.status = "Deadline"
            a.save()

    tugas_rutin = IsiTugasRutin.objects.all()
    for a in tugas_rutin:
        deadline = a.deadline
        saat_ini = timezone.now()
        apakah_deadline = (deadline - saat_ini)
        if (apakah_deadline.days < 0) and (a.status == 'On Progress'):
            a.status = "Deadline"
            a.save()

def apa_manager(user):
    return user.groups.filter(name='Manager').exists()

def hitungskor(user_id):
	pemilik = User.objects.get(id=user_id)
	tp = TugasProyek.objects.filter(pemilik_tugas=pemilik)
	tr = TugasRutin.objects.filter(pemilik_tugas=pemilik)

	total_skor_rutin = 0
	for rutin in tr:
		isi_tr = IsiTugasRutin.objects.filter(tugas_rutin = rutin)
		for isi in isi_tr:
			if isi.status == 'Tuntas':
			    total_skor_rutin += isi.penilaian		

	total_skor_proyek = 0
	for tugas_proyek in tp:
		if tugas_proyek.status == 'Tuntas':
		    total_skor_proyek += tugas_proyek.penilaian

	return total_skor_rutin + total_skor_proyek