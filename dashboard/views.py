from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage

from .decorators import unauthenticated_user
from .tc_ac import refresh_tcav, update_tc
from .logic import *
from .hskor import hitungskor
from .index_sp import query_index_sp
from .periode_sp import evaluasi, dapet_sp_periode_ini
from .rekap import query_rekap
from .rinci_tugas_rutin import rinci_tr, rinci_tr_eksekutif
from .models import *

from django.utils import timezone
from datetime import datetime, timedelta, date
import pytz
import django_excel

from django.http import HttpResponse

# Create your views here.

def omset(request):
    nama = request.user.first_name
    bagian = request.user.last_name

    query_omset_semua = OmsetBulan.objects.all()
    for ob in query_omset_semua:
        if ob.id == 1:
            continue
        ob.hitung_omset_bulan()
    query_omset = [ [i.periode, i.formatnya(i.omset_bulan_ini), i.formatnya(i.target_omset), i.selisih_omset_target(), i.selisih_omset_bulan(), i.formatnya(i.sales_to_target())] for i in query_omset_semua]

    context = {'bagian': bagian, 'nama': nama, 'query_omset' : query_omset}

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'omset.html', context)

def average_check(request):
    nama = request.user.first_name
    bagian = request.user.last_name
    context = {'bagian': bagian, 'nama': nama}

    ac = AverageCheck.objects.all()
    ac_master = AverageCheck.objects.all()

    ac = [[i.hari, i.formatnya(i.total_sales), i.total_check, i.formatnya(i.average_check), i.formatnya(i.total_sales_online), i.total_check_online, i.formatnya(i.average_check_online)] for i in ac]
    ac = ac[-7:]
    ac.reverse()
    context['ac'] = ac

    ac_antapani = [[i.hari, i.formatnya(i.total_sales_antapani), i.total_check_antapani, i.formatnya(i.average_check_antapani), i.formatnya(i.total_sales_online_antapani), i.total_check_online_antapani, i.formatnya(i.average_check_online_antapani)] for i in ac_master]
    ac_antapani = ac_antapani[-7:]
    ac_antapani.reverse()
    context['ac_antapani'] = ac_antapani

    ac_cisitu = [[i.hari, i.formatnya(i.total_sales_cisitu), i.total_check_cisitu, i.formatnya(i.average_check_cisitu), i.formatnya(i.total_sales_online_cisitu), i.total_check_online_cisitu, i.formatnya(i.average_check_online_cisitu)] for i in ac_master]
    ac_cisitu = ac_cisitu[-7:]
    ac_cisitu.reverse()
    context['ac_cisitu'] = ac_cisitu

    ac_jatinangor = [[i.hari, i.formatnya(i.total_sales_jatinangor), i.total_check_jatinangor, i.formatnya(i.average_check_jatinangor), i.formatnya(i.total_sales_online_jatinangor), i.total_check_online_jatinangor, i.formatnya(i.average_check_online_jatinangor)] for i in ac_master]
    ac_jatinangor = ac_jatinangor[-7:]
    ac_jatinangor.reverse()
    context['ac_jatinangor'] = ac_jatinangor

    ac_metro = [[i.hari, i.formatnya(i.total_sales_metro), i.total_check_metro, i.formatnya(i.average_check_metro), i.formatnya(i.total_sales_online_metro), i.total_check_online_metro, i.formatnya(i.average_check_online_metro)] for i in ac_master]
    ac_metro = ac_metro[-7:]
    ac_metro.reverse()
    context['ac_metro'] = ac_metro

    ac_sukajadi = [[i.hari, i.formatnya(i.total_sales_sukajadi), i.total_check_sukajadi, i.formatnya(i.average_check_sukajadi), i.formatnya(i.total_sales_online_sukajadi), i.total_check_online_sukajadi, i.formatnya(i.average_check_online_sukajadi)] for i in ac_master]
    ac_sukajadi = ac_sukajadi[-7:]
    ac_sukajadi.reverse()
    context['ac_sukajadi'] = ac_sukajadi

    ac_sukabirus = [[i.hari, i.formatnya(i.total_sales_sukabirus), i.total_check_sukabirus, i.formatnya(i.average_check_sukabirus), i.formatnya(i.total_sales_online_sukabirus), i.total_check_online_sukabirus, i.formatnya(i.average_check_online_sukabirus)] for i in ac_master]
    ac_sukabirus = ac_sukabirus[-7:]
    ac_sukabirus.reverse()
    context['ac_sukabirus'] = ac_sukabirus

    ac_sukapura = [[i.hari, i.formatnya(i.total_sales_sukapura), i.total_check_sukapura, i.formatnya(i.average_check_sukapura), i.formatnya(i.total_sales_online_sukapura), i.total_check_online_sukapura, i.formatnya(i.average_check_online_sukapura)] for i in ac_master]
    ac_sukapura = ac_sukapura[-7:]
    ac_sukapura.reverse()
    context['ac_sukapura'] = ac_sukapura

    ac_unjani = [[i.hari, i.formatnya(i.total_sales_unjani), i.total_check_unjani, i.formatnya(i.average_check_unjani), i.formatnya(i.total_sales_online_unjani), i.total_check_online_unjani, i.formatnya(i.average_check_online_unjani)] for i in ac_master]
    ac_unjani = ac_unjani[-7:]
    ac_unjani.reverse()
    context['ac_unjani'] = ac_unjani

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'average_check.html', context)

def upgrade_tc_ac(request):
    refresh_tcav()
    now = timezone.now() + timedelta(hours=7)
    tanggal_sekarang = date(now.year, now.month, now.day)
    cek_tanggal = AverageCheck.objects.filter(hari=tanggal_sekarang)

    if not cek_tanggal:
        d = AverageCheck(hari=tanggal_sekarang)
        d.tentukan_awal_akhir_hari()
        d.save()
    
    ac = AverageCheck.objects.all()
    for struk in ac:
	    update_tc(struk.id)
    
    return redirect('average_check')

def test_webhook(request):
    data = request.POST
    context = {'data' : data}
    return render(request, 'test_webhook.html', context)

def export_data_karyawan(request):
    
    karyawan_aktif = DataKaryawan.objects.filter(status="AKTIF")

    bulan = {
        "1" : "Jan",
        "2" : "Feb",
        "3" : "Mar",
        "4" : "Apr",
        "5" : "May",
        "6" : "Jun",
        "7" : "Jul",
        "8" : "Aug",
        "9" : "Sep",
        "10" : "Okt",
        "11" : "Nov",
        "12" : "Des"
    }

    i = 1
    datanya = [
        ["NO", "NO ID FING", "NIK", "Nama", "Area", "Level Manajemen", "Nama Posisi", "Kode Posisi", "Status Pegawai", "Tanggal Masuk", "Lama Bekerja", "No KTP", "Tempat Lahir", "Tanggal Lahir", "Umur", "Jenis Kelamin", "Agama", "Pendidikan", "Jurusan", "Alamat", "No Hp", "Marital Status", "Anak", "No.Rek", "BPJS Ketenagakerjaan"], 
    ]
    for d in karyawan_aktif:
        d.update_data()
        tanggal_masuk = d.tanggal_masuk.strftime("%d") + " " + bulan[str(d.tanggal_masuk.month)] + " " + d.tanggal_masuk.strftime("%Y")
        tanggal_lahir = d.tanggal_lahir.strftime("%d") + " " + bulan[str(d.tanggal_lahir.month)] + " " + d.tanggal_lahir.strftime("%Y")

        datanya.append([i, d.no_id_fingerprint, d.nik, d.nama, d.area, d.level_manajemen, d.nama_posisi, d.kode_posisi, d.status_pegawai, tanggal_masuk, d.lama_bekerja, d.no_ktp, d.tempat_lahir, tanggal_lahir, d.umur, d.jenis_kelamin, d.agama, d.pendidikan, d.jurusan, d.alamat, d.no_hp, d.marital_status, d.anak, d.no_rekening, d.bpjs_ketenagakerjaan])
        i += 1
    
    print(datanya)

    return django_excel.make_response_from_array(datanya, "xls", file_name="data_karyawan")

# -------------------------------------------------------------------------------------------------

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


# ------------------------------- REKAP ----------------------------------
@login_required(login_url='login')
def rekap(request):
    nama = request.user.first_name
    bagian = request.user.last_name
    periode1 = query_rekap(1, request.user.id)
    periode2 = query_rekap(2, request.user.id)

    context = {
        'bagian': bagian, 
        'nama': nama,
        'periode1' : periode1,
        'periode2' : periode2
    }

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    return render(request, 'rekap/rekap.html', context)

# ------------------------------- KLASEMEN ----------------------------------
@login_required(login_url='login')
def klasemen(request):

    nama = request.user.first_name
    bagian = request.user.last_name
    usr = User.objects.all()

    id_terlarang = [1, 5, 17, 18, 19, 21]
    user = []

    for a in usr:
        if a.id not in id_terlarang:
            user.append(a)

    id_orang_office = [6,3,23,25,8,22,2,24,4,31,36]
    orang_office = []
    non_office = []

    for a in user:
        skor = hitungskor(a.id)[0]
        total_tugas_tuntas = hitungskor(a.id)[1]
        if a.id in id_orang_office:
            orang_office.append( (a, skor, total_tugas_tuntas ) )
        else:
            non_office.append( (a, skor, total_tugas_tuntas ) )

    orang_office.sort(key=lambda tup: tup[1])
    non_office.sort(key=lambda tup: tup[1])
    orang_office = orang_office[::-1]
    non_office = non_office[::-1]

    context = {'bagian': bagian, 'nama': nama, 'orang_office' : orang_office, 'non_office': non_office}

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'klasemen.html', context)

# ------------------------------- SP ----------------------------------

@login_required(login_url='login')
def index_sp(request):
    ngecekdeadline()

    nama = request.user.first_name
    context = {
        'nama': nama,
        'data_kar' : True,
    }

    evaluasi_tugas = query_index_sp()
    evaluasi_tugas.sort(key=lambda tup: tup[6])
    evaluasi_tugas = evaluasi_tugas[::-1]
    context['evaluasi_tugas'] = evaluasi_tugas
    

    if request.user.last_name == 'Information Technology':
        context['debugging'] = True

    if request.user.groups.filter(name='Eksekutif').exists():
        context['data_kar'] = False
        return redirect('logout')

    return render(request, 'sp/index.html', context)


@login_required(login_url='login')
def eval_per_periode(request):

    nama = request.user.first_name
    context = {
        'nama': nama,
        'data_kar' : True,
    }
    
    kenasp_periode_maret2 = SuratPeringatan.objects.all()
    context['kenasp_periode_maret2'] = kenasp_periode_maret2
    
    # ---------------------------------------------
    hasil = evaluasi(1)
    hasil.sort(key=lambda tup: tup[6])
    hasil = hasil[::-1]
    context['evalmaret2'] = hasil

    evalapril1 = evaluasi(2)
    evalapril1.sort(key=lambda tup: tup[6])
    evalapril1 = evalapril1[::-1]
    context['evalapril1'] = evalapril1
    # ---------------------------------------------


    dieksekusi_maret2 = PeriodeSp.objects.get(pk=1).dieksekusi
    yang_kena_sp_maret2 = dapet_sp_periode_ini(hasil)
    context['yang_kena_sp_maret2'] = yang_kena_sp_maret2
    

    if not dieksekusi_maret2:
        context['belum_dieksekusi'] = True

    if request.user.last_name == 'Information Technology':
        context['debugging'] = True

    if request.user.groups.filter(name='Eksekutif').exists():
        context['data_kar'] = False
        return redirect('logout')

    return render(request, 'sp/eval_per_periode.html', context)


@login_required(login_url='login')
def debugging_sp(request):
    if request.user.last_name != 'Information Technology':
        return redirect('logout')

    if request.method == 'POST':
        # nama periode, tahun
        namaperiode = request.POST.get("namaperiode")
        tahun_periode = request.POST.get("tahunperiode")
        mulai = request.POST.get('mulai')
        selesai = request.POST.get('selesai')
        periode_sp = PeriodeSp(
            nama_periode = 'Maret 2 - Input sendiri',
            tahun = tahun_periode,
            awal_periode = mulai,
            akhir_periode = selesai,
            dieksekusi = False
        )
        periode_sp.save()

    context = {
        'nama': request.user.first_name,
        'data_kar' : True,
        'debugging' : True
    }

    return render(request, 'sp/debugging.html', context)

def eksekusi_sp(request, id_periode_sp):

    hasil = evaluasi(id_periode_sp)
    yang_kena_sp = dapet_sp_periode_ini(hasil)

    for isi in yang_kena_sp:
        id_user = isi[-1]
        object_user = User.objects.get(pk=id_user)
        # kenasp = KenaSp()

    return redirect('eval_per_periode')
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


@login_required(login_url='login')
def edit_nilai(request, id_isi_tugas_rutin):

    isitr = TugasProyek.objects.get(pk=id_isi_tugas_rutin)

    if request.method == 'POST':
        komentar = request.POST.get('komentar')
        penilaian = request.POST.get('penilaian')
        isitr.komentar = komentar
        isitr.penilaian = penilaian
        isitr.save()
        return redirect('lihat_tugas_tuntas')

    nama = request.user.first_name    

    context = {
        'nama': nama,
        'data_kar' : True,
        'tugas' : isitr
    }

    # belum ada dokumen
    if isitr == '#':
        context['belum'] = True

    if request.user.groups.filter(name='Eksekutif').exists() or request.user.groups.filter(name='Manager').exists():
        context['data_kar'] = False
        return redirect('logout')

    return render(request, 'ceo/edit_nilai.html', context)


# ------------------------------- MANAGER ----------------------------------

@login_required(login_url='login')
def manager(request):
        
    ngecekdeadline()

    nama = request.user.first_name
    context = {'nama': nama}

    sp_user = SuratPeringatan.objects.filter(user=User.objects.get(pk=request.user.id))
    if sp_user:
        context['kena_sp'] = True
        context['surat_peringatan'] = sp_user
    
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
def input_tugas_proyek_kelompok(request):

    nama = request.user.first_name
    eksekutif_bagian = User.objects.filter(last_name=request.user.last_name).exclude(first_name=request.user.first_name)
    eksekutif_bagian = eksekutif_bagian.exclude(id=5)
    context = {
        'nama' : nama, 
        'eksekutif_bagian': eksekutif_bagian
        }

    ceo = request.user.groups.filter(name='CEO').exists()

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if ceo:
        context['sidebar_ceo'] = True

    if request.method == 'POST':
        data_judul = request.POST.get('judul')
        data_isi = request.POST.get('isi')
        data_deadline = request.POST.get('deadline')
        listnya = list(request.POST.keys())
        for k in listnya[4:]:
            k = request.POST.get(k)
            idnya = k.split("_")
            idnya = int(idnya[1])
            if ceo:
                t = TugasProyek(
                    pemilik_tugas = User.objects.get(pk=idnya),
                    judul = data_judul,
                    isi = data_isi,
                    deadline = data_deadline,
                    status = 'On Progress',
                    bagian = 'Management',
                    bukti = '#',
                    ketuntasan = False
                )
            else:
                t = TugasProyek(
                    pemilik_tugas = User.objects.get(pk=idnya),
                    judul = data_judul,
                    isi = data_isi,
                    deadline = data_deadline,
                    status = 'On Progress',
                    bagian = request.user.last_name,
                    bukti = '#',
                    ketuntasan = False
                )
            t.save()
        return redirect("lihat_tugas")

    return render(request, 'manager/input_tugas_proyek_kelompok.html', context)

def input_tugas_rutin_kelompok(request):

    nama = request.user.first_name
    eksekutif_bagian = User.objects.filter(last_name=request.user.last_name).exclude(first_name=request.user.first_name)
    eksekutif_bagian = eksekutif_bagian.exclude(id=5)
    context = {
        'nama' : nama, 
        'eksekutif_bagian': eksekutif_bagian
        }

    ceo = request.user.groups.filter(name='CEO').exists()

    if request.method == 'POST':
        data_judul = request.POST.get('judul')
        data_isi = request.POST.get('isi')
        # DICOMMENT BUAT DEBUGGING AJA

        banyak_tugas = int(request.POST.get('banyak-tugas'))
        # DICOMMENT BUAT DEBUGGING AJA
        skip = banyak_tugas + 4
        listnya = list(request.POST.keys())
        for k in listnya[skip:]:
            k = request.POST.get(k)
            idnya = k.split("_")
            id_eksekutif = int(idnya[1])

            object_eksekutif = User.objects.get(pk=id_eksekutif)

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

            objek_tugas = TugasRutin.objects.get(pk=tgs_rutin.id)
            statusnya = "On Progress"

            tipe = request.POST.get('tipe')
            if tipe == 'harian':
                data_mulai = request.POST.get('mulai')
                data_selesai = request.POST.get('selesai')

                data_mulai += "T" + request.POST.get('deadlinejam')
                data_selesai += "T" + request.POST.get('deadlinejam')

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
                        isi = data_isi,
                        ketuntasan = False
                    )

                    isitgs_rutin.save()
                    tanggal += timedelta(days=1)
            else:
                # banyak_tugas adalah integer
                banyak_tugas = int(request.POST.get('banyak-tugas'))
                for i in range(banyak_tugas):
                    isitgs_rutin = IsiTugasRutin(
                        tugas_rutin = objek_tugas,
                        deadline = request.POST.get('deadline' + str(i+1)),
                        status = statusnya,
                        judul = data_judul,
                        isi = data_isi,
                        link_bukti = '#'
                    )
                    isitgs_rutin.save()
                
        return redirect('lihat_tugas')
        

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if ceo:
        context['sidebar_ceo'] = True

    return render(request, 'manager/input_tugas_rutin_kelompok.html', context)

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
                bukti = '#',
                ketuntasan = False
            )
        else:
            t = TugasProyek(
                pemilik_tugas = User.objects.get(pk=id_eksekutif),
                judul = data_judul,
                isi = data_isi,
                deadline = data_deadline,
                status = 'On Progress',
                bagian = request.user.last_name,
                bukti = '#',
                ketuntasan = False
            )
        t.save()
        return redirect('lihat_tugas')

    return render(request, 'manager/input_tugas_proyek.html', context)


@login_required(login_url='login')
def input_tugas_rutin(request, id_eksekutif):

    ceo = request.user.groups.filter(name='CEO').exists()

    if request.method == 'POST':
        data_judul = request.POST.get('judul')
        data_isi = request.POST.get('isi')
        # DICOMMENT BUAT DEBUGGING AJA
        object_eksekutif = User.objects.get(pk=id_eksekutif)

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

        objek_tugas = TugasRutin.objects.get(pk=tgs_rutin.id)
        statusnya = "On Progress"

        tipe = request.POST.get('tipe')
        if tipe == 'harian':
            data_mulai = request.POST.get('mulai')
            data_selesai = request.POST.get('selesai')

            data_mulai += "T" + request.POST.get('deadlinejam')
            data_selesai += "T" + request.POST.get('deadlinejam')

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
                    isi = data_isi,
                    ketuntasan = False
                )

                isitgs_rutin.save()
                tanggal += timedelta(days=1)
        else:
            # banyak_tugas adalah integer
            banyak_tugas = int(request.POST.get('banyak-tugas'))
            for i in range(banyak_tugas):
                isitgs_rutin = IsiTugasRutin(
                    tugas_rutin = objek_tugas,
                    deadline = request.POST.get('deadline' + str(i+1)),
                    status = statusnya,
                    judul = data_judul,
                    isi = data_isi,
                    link_bukti = '#'
                )
                isitgs_rutin.save()
            
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

    # mengembalikan object user
    anggota = anggotabagian(request.user.first_name, request.user.last_name)

    ceo = request.user.groups.filter(name='CEO').exists()

    ngecekdeadline()
    nama = request.user.first_name
    context = {'nama' : nama, 'anggota' : anggota}

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if ceo:
        context['sidebar_ceo'] = True

    # periode tugas yang mau ditampilkan
    periode = PeriodeSp.objects.get(pk=2) # periode april 2
    awal = periode.awal_periode
    akhir = periode.akhir_periode + timedelta(days=365)

    # tugas proyek
    if ceo:
        tp = TugasProyek.objects.filter(bagian='Management', deadline__range=[awal, akhir]).exclude(status='Tuntas').order_by('-id')
        tr = TugasRutin.objects.filter(bagian='Management').order_by('-id').exclude(archive=True)
    else:
        tp = TugasProyek.objects.filter(bagian=request.user.last_name, deadline__range=[awal, akhir]).exclude(status='Tuntas').order_by('deadline')
        tr = TugasRutin.objects.order_by('-id').exclude(archive=True)
        tr = tr.exclude(bagian='Management')

    tp = tp.exclude(archive=True).order_by('deadline')
    tp = tp.exclude(ketuntasan=True)
    tr = tr.exclude(archive=True)

    tugas_rutin_marketing = rinci_tr("Marketing")
    tugas_rutin_operation = rinci_tr('Operation')
    tugas_rutin_finance = rinci_tr("Finance")
    tugas_rutin_hr = rinci_tr("Human Resource")

    bagian_user = request.user.last_name
    if bagian_user == 'Marketing':
        context['manager_marketing'] = True
    elif bagian_user == 'Finance':
        context['manager_finance'] = True
    elif bagian_user == 'Human Resource':
        context['manager_hr'] = True

    context['tugas_proyek'] = tp
    context['tugas_rutin_marketing'] = tugas_rutin_marketing
    context['tugas_rutin_operation'] = tugas_rutin_operation
    context['tugas_rutin_finance'] = tugas_rutin_finance
    context['tugas_rutin_hr'] = tugas_rutin_hr

    return render(request, 'manager/lihat_tugas.html', context)


@login_required(login_url='login')
def lihat_tugas_per_nama(request, id_user):

    nama = request.user.first_name
    ceo = request.user.groups.filter(name='CEO').exists()
    anggota = anggotabagian(request.user.first_name, request.user.last_name)
    tp = TugasProyek.objects.filter(pemilik_tugas=User.objects.get(pk=id_user), ketuntasan=False).order_by('deadline')
    # nama, id, tuntas, total tugas
    tr = rinci_tr_eksekutif(id_user)
    nama_pemilik_tugas = User.objects.get(pk=id_user).first_name
    context = {
        'nama' : nama,
        'anggota' : anggota,
        'tugas_proyek' : tp,
        'tugas_rutin' : tr,
        'nama_pemilik_tugas' : nama_pemilik_tugas
    }

    if ceo:
        context['sidebar_ceo'] = True

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'manager/lihat_tugas_per_nama.html', context)


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
        tp = TugasProyek.objects.filter(bagian='Management', ketuntasan=True).order_by('-id')
    else:
        tp = TugasProyek.objects.filter(bagian=request.user.last_name, ketuntasan=True).order_by('-id')
    
    banyak_data_per_page = 10
    p = Paginator(tp, banyak_data_per_page)
    page_num = request.GET.get('page', 1)

    try:
	    page = p.page(page_num)
    except EmptyPage:
	    page = p.page(1)

    banyak_halaman = [str(a+1) for a in range(p.num_pages)]
    context['banyak_halaman'] = banyak_halaman
    context['halaman_aktif'] = str(page_num)

    # tr = TugasRutin.objects.filter(bagian=request.user.last_name, status='Tuntas')
    context['tugas_proyek'] = page
    # context['tugas_rutin'] = tr

    # KHUSUS TUGAS RUTIN YANG UDAH TUNTAS
    if ceo:
        tr = TugasRutin.objects.filter(bagian='Management').order_by('-id')
    else:
        tr = TugasRutin.objects.filter(bagian=request.user.last_name).order_by('-id')
    context['tugas_rutin'] = tr

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

    tr = IsiTugasRutin.objects.filter(tugas_rutin=t, ketuntasan=False)
    context['tr'] = tr
    context['judul'] = t.judul
    context['isi'] = t.isi

    return render(request, 'manager/progress_tugas_rutin.html', context)


@login_required(login_url='login')
def tugas_rutin_tuntas(request, id_tugas):

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
    tr = tr.filter(status='Tuntas', ketuntasan=True)

    context['tugas_rutin'] = tr
    context['judul'] = t.judul
    context['isi'] = t.isi

    return render(request, 'manager/tugas_rutin_tuntas.html', context)



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

    if not (t.link_bukti == None):
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

    if (t.status == 'Tuntas') or (t.ketuntasan):
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
        context['tombol_edit_nilai'] = True

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if t.bukti == '#':
        context['belum'] = True
    if (t.status == 'Tuntas') or (t.ketuntasan):
        context['tuntas'] = True

    if not (t.link_bukti == None):
        context['ada_link'] = True

    return render(request, 'manager/mdetail_proyek.html', context)

@login_required(login_url='login')
def tuntas(request, id_tugas):
    
    if request.method == 'POST':
        t = TugasProyek.objects.get(pk=id_tugas)
        t.komentar = request.POST.get('komentar')
        t.penilaian = request.POST.get('penilaian')
        t.ketuntasan = True
        if (t.status == 'Terlambat'):
            t.status = 'Terlambat'
        else:
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
        tr = t.tugas_rutin
        t.komentar = request.POST.get('komentar')
        t.penilaian = request.POST.get('penilaian')
        t.ketuntasan = True
        if (t.status == 'Terlambat'):
            t.status = 'Terlambat'
        else:
            t.status = 'Tuntas'
        t.save()

        return progress_tugas_rutin(request, tr.id)

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
    elif t.status == 'Terlambat':
        context['terlambat'] = True

    return render(request, 'manager/edit_tugas_proyek.html', context)

@login_required(login_url='login')
def duplikasi_tugas_proyek(request, id_tugas):
    
    ceo = request.user.groups.filter(name='CEO').exists()
    tugas = TugasProyek.objects.get(pk=id_tugas)

    if request.method == 'POST':
        data_judul = request.POST.get('judul')
        data_isi = request.POST.get('isi')
        data_deadline = request.POST.get('deadline')
        pemilik = tugas.pemilik_tugas
        
        if ceo:
            t = TugasProyek(
                pemilik_tugas = pemilik,
                judul = data_judul,
                isi = data_isi,
                deadline = data_deadline,
                status = 'On Progress',
                bagian = 'Management',
                bukti = '#'
            )
        else:
            t = TugasProyek(
                pemilik_tugas = pemilik,
                judul = data_judul,
                isi = data_isi,
                deadline = data_deadline,
                status = 'On Progress',
                bagian = request.user.last_name,
                bukti = '#'
            )
        t.save()

        return redirect('lihat_tugas')

    nama = request.user.first_name
    context = {'nama' : nama, 'tugas' : tugas}
    if ceo:
        context['sidebar_ceo'] = True

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True   

    return render(request, 'manager/duplikasi_tugas_proyek.html', context)


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

        return progress_tugas_rutin(request, t.tugas_rutin.id)

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
    t = TugasProyek.objects.filter(pemilik_tugas=objek_user).exclude(status="Tuntas").order_by('deadline')
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


@login_required(login_url='login')
def archive_tugas(request):
    nama = request.user.first_name
    context = {'nama' : nama}
    
    tp = TugasProyek.objects.filter(archive=True)
    tr = TugasRutin.objects.filter(archive=True)

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    context['tugas_proyek'] = tp
    context['tugas_rutin'] = tr
    return render(request, 'manager/archive_tugas.html', context)

def eksekusi_archive_proyek(request, id_tugas):

    tp = TugasProyek.objects.get(pk=id_tugas)
    tp.archive = True
    tp.save()

    return redirect('lihat_tugas')

def eksekusi_archive_rutin(request, id_tugas):

    tr = TugasRutin.objects.get(pk=id_tugas)
    tr.archive = True
    tr.save()
    
    return redirect('lihat_tugas')

def kembalikan_archive_proyek(request, id_tugas):

    tp = TugasProyek.objects.get(pk=id_tugas)
    tp.archive = False
    tp.save()

    return redirect('archive_tugas')

def kembalikan_archive_rutin(request, id_tugas):

    tr = TugasRutin.objects.get(pk=id_tugas)
    tr.archive = False
    tr.save()
    
    return redirect('archive_tugas')


# --------------------------- eksekutif ----------------------------------

@login_required(login_url='login')
def eksekutif(request):
    
    nama = request.user.first_name
    context = {'nama' : nama}

    sp_user = SuratPeringatan.objects.filter(user=User.objects.get(pk=request.user.id))
    if sp_user:
        context['kena_sp'] = True
        context['surat_peringatan'] = sp_user

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'eksekutif/home.html', context)


@login_required(login_url='login')
def daftar_tugas(request):

    nama = request.user.first_name

    tugas_rutin = rinci_tr_eksekutif(request.user.id)

    ngecekdeadline()
    objek_user = User.objects.get(pk=request.user.id)
    t = TugasProyek.objects.filter(pemilik_tugas=objek_user).order_by('deadline').exclude(status="Tuntas")
    tr = TugasRutin.objects.filter(pemilik_tugas=objek_user).order_by('-id')

    context = {'nama' : nama, 'tugas_proyek' : t, 'tugas_rutin': tugas_rutin}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'eksekutif/daftar_tugas.html', context)


@login_required(login_url='login')
def tugas_tuntas(request):

    nama = request.user.first_name
    ngecekdeadline()
    objek_user = User.objects.get(pk=request.user.id)
    t = TugasProyek.objects.filter(pemilik_tugas=objek_user, status="Tuntas").order_by('-id')
    tr = rinci_tr_eksekutif(request.user.id, False)

    context = {'nama' : nama, 'tugas_proyek' : t, 'tugas_rutin' : tr}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'eksekutif/tugas_tuntas.html', context)

@login_required(login_url='login')
def daftar_tugas_rutin(request, id_tugas):

    nama = request.user.first_name
    t = TugasRutin.objects.get(pk=id_tugas)
    tr = IsiTugasRutin.objects.filter(tugas_rutin=t).order_by('deadline')
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
    context['nottuntas'] = True
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    if t.status == 'Tuntas':
        context['tuntas'] = True
        context['nottuntas'] = False
    
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
        
        t.selesai_pada = timezone.now()

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

        t.selesai_pada = timezone.now()
        
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
    karyawan_office = d.filter(area='Office')
    area_antapani = d.filter(area="Antapani")
    area_cisitu = d.filter(area='Cisitu')
    area_jatinangor = d.filter(area='Jatinangor')
    area_metro = d.filter(area='Metro')
    area_sukajadi = d.filter(area='Sukajadi')
    area_sukabirus = d.filter(area='Telkom Sukabirus')
    area_sukapura = d.filter(area='Telkom Sukapura')
    area_unjani = d.filter(area='Unjani')

    context = {'nama' : request.user.first_name,
               'data' : d,
               'karyawan_office' : karyawan_office,
               'area_antapani' : area_antapani,
               'area_cisitu' : area_cisitu,
               'area_jatinangor' : area_jatinangor,
               'area_metro' : area_metro,
               'area_sukajadi' : area_sukajadi,
               'area_sukabirus' : area_sukabirus,
               'area_sukapura' : area_sukapura,
               'area_unjani' : area_unjani
            }
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

    d = DataKaryawan.objects.all().order_by('-id')[0]
    nik_terakhir = '0000' + str(d.id+1)
    nik_terakhir = nik_terakhir[-4:]

    context = {
        'nama' : request.user.first_name, 
        'nik_terakhir' : nik_terakhir
    }

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
    tanggal_masuk = d.tanggal_masuk.strftime("%Y-%m-%d")
    tanggal_lahir = d.tanggal_lahir.strftime("%Y-%m-%d")

    context = {'nama' : request.user.first_name, 
               'data' : d,
               'tanggal_masuk' : tanggal_masuk,
               'tanggal_lahir' : tanggal_lahir
            }
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
    elif (d.pendidikan == 'SMA/SMK') or (d.pendidikan == "SMA"):
        context['pendidikan_sma'] = True
    elif d.pendidikan == 'SMK':
        context['pendidikan_smk'] = True
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

# ---------------------- MARKETING -------------------------------
@login_required(login_url='login')
def complaint_list(request):
    c = Complaint.objects.all()
    context = {'nama' : request.user.first_name, 'complaint' : c}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    return render(request, 'marketing/complaint_list.html', context)

@login_required(login_url='login')
def detail_complaint(request, id_complaint):
    c = Complaint.objects.get(pk=id_complaint)
    context = {'nama' : request.user.first_name, 'complaint' : c}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    return render(request, 'marketing/detail_complaint.html', context)

def edit_complaint(request, id_complaint):

    if request.method == "POST":
        c = Complaint.objects.get(pk=id_complaint)
        c.tanggal = request.POST.get('tanggal')
        c.jam_operasional = request.POST.get('jamoperasional')
        c.nama = request.POST.get('nama')
        c.media_penyampaian_complain = request.POST.get('mediapenyampaiancomplaint')
        c.nomor_kontak = request.POST.get('nomorkontak')
        c.complaint = request.POST.get('complaint')
        c.handling = request.POST.get('handling')
        c.cabang = request.POST.get('cabang')
        c.status = request.POST.get('status')
        c.jenis = request.POST.get('jenis')

        c.save()
        return redirect('complaint_list')


    c = Complaint.objects.get(pk=id_complaint)
    tgl = str(c.tanggal)
    jam_ops = str(c.jam_operasional)
    context = {
        'nama' : request.user.first_name, 
        'complaint' : c, 
        'tanggal' : tgl, 
        'jam' : jam_ops
        }
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    return render(request, 'marketing/edit_complaint.html', context)

@login_required(login_url='login')
def input_complaint(request):

    if request.method == 'POST':
        input_tanggal = request.POST.get('tanggal')
        input_jam_operasional = request.POST.get('jamoperasional')
        input_nama = request.POST.get('nama')
        input_media_penyampaian_complaint = request.POST.get('mediapenyampaiancomplaint')
        input_nomor_kontak = request.POST.get('nomorkontak')
        input_complaint = request.POST.get('complaint')
        input_handling = request.POST.get('handling')
        input_jenis = request.POST.get('jenis')
        input_cabang = request.POST.get('cabang')
        input_status = request.POST.get('status')

        c = Complaint(
            tanggal=input_tanggal,
            jam_operasional=input_jam_operasional,
            nama=input_nama,
            media_penyampaian_complain=input_media_penyampaian_complaint,
            nomor_kontak=input_nomor_kontak,
            complaint=input_complaint,
            handling=input_handling,
            cabang=input_cabang,
            jenis = input_jenis,
            status = input_status
        )
        c.save()
        return redirect('complaint_list')

    context = {'nama' : request.user.first_name}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    return render(request, 'marketing/input_complaint.html', context)

@login_required(login_url='login')
def mystery_guest(request):
    mg = MysteryGuest.objects.all()
    context = {'nama' : request.user.first_name, 'mg' : mg}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    return render(request, 'marketing/mystery_guest.html', context)


@login_required(login_url='login')
def input_mystery_guest(request):

    if request.method == 'POST':
        input_cabang = request.POST.get('cabang')
        input_nama = request.POST.get('nama')
        input_tanggal = request.POST.get('tanggal')
        input_nilai_appearance = request.POST.get('nilai_appearance')
        input_komentar_appearance = request.POST.get('komentar_appearance')
        input_nilai_aroma = request.POST.get('nilai_aroma')
        input_komentar_aroma = request.POST.get('komentar_aroma')
        input_nilai_rasa = request.POST.get('nilai_rasa')
        input_komentar_rasa = request.POST.get('komentar_rasa')
        input_nilai_overall = request.POST.get('nilai_overall')
        input_komentar_overall = request.POST.get('komentar_overall')
        input_nilai_manajemen = request.POST.get('nilai_manajemen')

        uploaded_dokumentasi_luar = request.FILES['dokumentasi_luar']
        fs1 = FileSystemStorage()
        nama1 = fs1.save(uploaded_dokumentasi_luar.name, uploaded_dokumentasi_luar)
        alamat1 = fs1.url(nama1)

        uploaded_dokumentasi_dalam = request.FILES['dokumentasi_dalam']
        fs2 = FileSystemStorage()
        nama2 = fs2.save(uploaded_dokumentasi_dalam.name, uploaded_dokumentasi_dalam)
        alamat2 = fs2.url(nama2)

        mg = MysteryGuest(
            cabang = input_cabang,
            nama = input_nama,
            tanggal = input_tanggal,
            nilai_appearance = input_nilai_appearance,
            komentar_appearance = input_komentar_appearance,
            nilai_aroma = input_nilai_aroma,
            komentar_aroma = input_komentar_aroma,
            nilai_rasa = input_nilai_rasa,
            komentar_rasa = input_komentar_rasa,
            nilai_overall = input_nilai_overall,
            komentar_overall = input_komentar_overall,
            dokumentasi_luar = alamat1,
            dokumentasi_dalam = alamat2,
            nilai_manajemen = input_nilai_manajemen
        )
        mg.save()
        return redirect('mystery_guest')

    context = {'nama' : request.user.first_name}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    return render(request, 'marketing/input_mystery_guest.html', context)

@login_required(login_url='login')
def detail_mystery_guest(request, id_mystery_guest):
    mg = MysteryGuest.objects.get(pk=id_mystery_guest)
    context = {'nama' : request.user.first_name, 'mg' : mg}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    return render(request, 'marketing/detail_mystery_guest.html', context)

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
