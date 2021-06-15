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
from .supply_chain import update_pemakaian_ayam, periksa_hari_dalam_pemakaian_ayam, query_rata_rata_deman_ayam
from .operation import coba_query
from .models import *
from .rm_app import query_rm_app

from rm_app.models import ProduksiAyam

from django.utils import timezone
from datetime import datetime, timedelta, date, time
import pytz
import django_excel


from django.http import HttpResponse, request

PERIODE = 6

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

    ac = AverageCheck.objects.all().order_by('hari')
    ac_master = AverageCheck.objects.all().order_by('hari')
    jumlah = 7

    if request.method == 'POST':
        awal = request.POST.get('awal')
        akhir = request.POST.get('akhir')
        
        awal = awal.split('-')
        akhir = akhir.split('-')

        awal_date = date( int(awal[0]), int(awal[1]), int(awal[2]) )
        akhir_date = date( int(akhir[0]), int(akhir[1]), int(akhir[2]) )
        selisih = akhir_date - awal_date
        if selisih.days <= 0:
            pass
        else:
            ac = ac.filter(hari__range=[awal_date, akhir_date])
            ac_master = ac_master.filter(hari__range=[awal_date, akhir_date])
            jumlah = selisih.days + 1
   
    ac = [[i.hari, i.formatnya(i.total_sales), i.total_check, i.formatnya(i.average_check), i.formatnya(i.total_sales_online), i.total_check_online, i.formatnya(i.average_check_online)] for i in ac]
    ac = ac[-jumlah:]
    ac.reverse()
    context['ac'] = ac

    ac_antapani = [[i.hari, i.formatnya(i.total_sales_antapani), i.total_check_antapani, i.formatnya(i.average_check_antapani), i.formatnya(i.total_sales_online_antapani), i.total_check_online_antapani, i.formatnya(i.average_check_online_antapani)] for i in ac_master]
    ac_antapani = ac_antapani[-jumlah:]
    ac_antapani.reverse()
    context['ac_antapani'] = ac_antapani

    ac_cisitu = [[i.hari, i.formatnya(i.total_sales_cisitu), i.total_check_cisitu, i.formatnya(i.average_check_cisitu), i.formatnya(i.total_sales_online_cisitu), i.total_check_online_cisitu, i.formatnya(i.average_check_online_cisitu)] for i in ac_master]
    ac_cisitu = ac_cisitu[-jumlah:]
    ac_cisitu.reverse()
    context['ac_cisitu'] = ac_cisitu

    ac_jatinangor = [[i.hari, i.formatnya(i.total_sales_jatinangor), i.total_check_jatinangor, i.formatnya(i.average_check_jatinangor), i.formatnya(i.total_sales_online_jatinangor), i.total_check_online_jatinangor, i.formatnya(i.average_check_online_jatinangor)] for i in ac_master]
    ac_jatinangor = ac_jatinangor[-jumlah:]
    ac_jatinangor.reverse()
    context['ac_jatinangor'] = ac_jatinangor

    ac_metro = [[i.hari, i.formatnya(i.total_sales_metro), i.total_check_metro, i.formatnya(i.average_check_metro), i.formatnya(i.total_sales_online_metro), i.total_check_online_metro, i.formatnya(i.average_check_online_metro)] for i in ac_master]
    ac_metro = ac_metro[-jumlah:]
    ac_metro.reverse()
    context['ac_metro'] = ac_metro

    ac_sukajadi = [[i.hari, i.formatnya(i.total_sales_sukajadi), i.total_check_sukajadi, i.formatnya(i.average_check_sukajadi), i.formatnya(i.total_sales_online_sukajadi), i.total_check_online_sukajadi, i.formatnya(i.average_check_online_sukajadi)] for i in ac_master]
    ac_sukajadi = ac_sukajadi[-jumlah:]
    ac_sukajadi.reverse()
    context['ac_sukajadi'] = ac_sukajadi

    ac_sukabirus = [[i.hari, i.formatnya(i.total_sales_sukabirus), i.total_check_sukabirus, i.formatnya(i.average_check_sukabirus), i.formatnya(i.total_sales_online_sukabirus), i.total_check_online_sukabirus, i.formatnya(i.average_check_online_sukabirus)] for i in ac_master]
    ac_sukabirus = ac_sukabirus[-jumlah:]
    ac_sukabirus.reverse()
    context['ac_sukabirus'] = ac_sukabirus

    ac_sukapura = [[i.hari, i.formatnya(i.total_sales_sukapura), i.total_check_sukapura, i.formatnya(i.average_check_sukapura), i.formatnya(i.total_sales_online_sukapura), i.total_check_online_sukapura, i.formatnya(i.average_check_online_sukapura)] for i in ac_master]
    ac_sukapura = ac_sukapura[-jumlah:]
    ac_sukapura.reverse()
    context['ac_sukapura'] = ac_sukapura

    ac_unjani = [[i.hari, i.formatnya(i.total_sales_unjani), i.total_check_unjani, i.formatnya(i.average_check_unjani), i.formatnya(i.total_sales_online_unjani), i.total_check_online_unjani, i.formatnya(i.average_check_online_unjani)] for i in ac_master]
    ac_unjani = ac_unjani[-jumlah:]
    ac_unjani.reverse()
    context['ac_unjani'] = ac_unjani

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'average_check.html', context)

def upgrade_tc_ac(request):
    try:
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
    except:
        pass
    
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

    return django_excel.make_response_from_array(datanya, "xls", file_name="data_karyawan")


def export_karyawan_out(request):
    karyawan_out = DataKaryawan.objects.filter(status="KELUAR").order_by('-tanggal_keluar')
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
    datanya = [["NIK", "Nama", "Jabatan", "Area", "Tanggal Masuk", "Tanggal Keluar", "Alasan"]]
    for k in karyawan_out:
        tanggal_masuk = k.tanggal_masuk.strftime("%d") + " " + bulan[str(k.tanggal_masuk.month)] + " " + k.tanggal_masuk.strftime("%Y")
        
        if k.tanggal_keluar == None:
            continue
        else:
            tanggal_keluar = k.tanggal_keluar.strftime("%d") + " " + bulan[str(k.tanggal_keluar.month)] + " " + k.tanggal_keluar.strftime("%Y")
        
        datanya.append([k.nik, k.nama, k.nama_posisi, k.area, tanggal_masuk, tanggal_keluar, k.alasan_keluar])

    return django_excel.make_response_from_array(datanya, "xls", file_name="data_karyawan_out")

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
    periode3 = query_rekap(3, request.user.id)
    periode4 = query_rekap(4, request.user.id)
    periode5 = query_rekap(5, request.user.id)
    periode6 = query_rekap(6, request.user.id)
    periode7 = query_rekap(7, request.user.id)

    context = {
        'bagian': bagian, 
        'nama': nama,
        'periode1' : periode1,
        'periode2' : periode2,
        'periode3' : periode3,
        'periode4' : periode4,
        'periode5' : periode5,
        'periode6' : periode6,
        'periode7' : periode7,
        
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
    
    kenasp_periode_maret2 = SuratPeringatan.objects.filter(mulai_sp=date(2021, 3, 26))
    context['kenasp_periode_maret2'] = kenasp_periode_maret2

    kenasp_periode_april1 = SuratPeringatan.objects.filter(mulai_sp=date(2021, 4, 11))
    context['kenasp_periode_april1'] = kenasp_periode_april1

    kenasp_periode_april2 = SuratPeringatan.objects.filter(mulai_sp=date(2021, 4, 26))
    context['kenasp_periode_april2'] = kenasp_periode_april2

    kenasp_periode_mei1 = SuratPeringatan.objects.filter(mulai_sp=date(2021, 5, 11))
    context['kenasp_periode_mei1'] = kenasp_periode_mei1
    
    kenasp_periode_mei2 = SuratPeringatan.objects.filter(mulai_sp=date(2021, 5, 26))
    context['kenasp_periode_mei2'] = kenasp_periode_mei2

    kenasp_periode_juni1 = SuratPeringatan.objects.filter(mulai_sp=date(2021, 6, 11))
    context['kenasp_periode_juni1'] = kenasp_periode_juni1

    kenasp_periode_juni1 = SuratPeringatan.objects.filter(mulai_sp=date(2021, 6, 26))
    context['kenasp_periode_juni1'] = kenasp_periode_juni1

    # ---------------------------------------------
    hasil = evaluasi(1)
    hasil.sort(key=lambda tup: tup[6])
    hasil = hasil[::-1]
    context['evalmaret2'] = hasil

    evalapril1 = evaluasi(2)
    evalapril1.sort(key=lambda tup: tup[6])
    evalapril1 = evalapril1[::-1]
    context['evalapril1'] = evalapril1

    evalapril2 = evaluasi(3)
    evalapril2.sort(key=lambda tup: tup[6])
    evalapril2 = evalapril2[::-1]
    context['evalapril2'] = evalapril2

    mei1 = evaluasi(4)
    mei1.sort(key=lambda tup: tup[6])
    mei1 = mei1[::-1]
    context['mei1'] = mei1

    mei2 = evaluasi(5)
    mei2.sort(key=lambda tup: tup[6])
    mei2 = mei2[::-1]
    context['mei2'] = mei2

    juni1 = evaluasi(6)
    juni1.sort(key=lambda tup: tup[6])
    juni1 = juni1[::-1]
    context['juni1'] = juni1

    juni2 = evaluasi(7)
    juni2.sort(key=lambda tup: tup[7])
    juni2 = juni2[::-1]
    context['juni2'] = juni2
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
    periksa_hari_dalam_pemakaian_ayam()
    nama = request.user.first_name
    context = {
        'nama': nama,
        'data_kar' : True,
    }

    query_complaint = query_complaint_dashboard(PERIODE)
    periode_kerja = PeriodeKerja.objects.get(pk=PERIODE)
    context['complaint'] = query_complaint
    context['periode_kerja'] = periode_kerja
    context['query_box_home'] = query_box_home(PERIODE)
    context['query_kepuasan_pelanggan'] = query_kepuasan_pelanggan_dashboard()
    context['query_penjualan_harian'] = query_penjualan_harian_dashboard(PERIODE)
    context['tren_penjualan_harian'] = tren_penjualan_harian(PERIODE)
    periode_kerja_sebelumnya = PeriodeKerja.objects.get(pk=PERIODE-1)
    context['periode_kerja_sebelumnya'] = periode_kerja_sebelumnya

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
    periksa_hari_dalam_pemakaian_ayam()

    nama = request.user.first_name
    context = {'nama': nama}

    query_complaint = query_complaint_dashboard(PERIODE)
    periode_kerja = PeriodeKerja.objects.get(pk=PERIODE)
    periode_kerja_sebelumnya = PeriodeKerja.objects.get(pk=PERIODE-1)
    context['periode_kerja_sebelumnya'] = periode_kerja_sebelumnya
    context['complaint'] = query_complaint
    context['periode_kerja'] = periode_kerja
    context['query_box_home'] = query_box_home(PERIODE)
    context['query_kepuasan_pelanggan'] = query_kepuasan_pelanggan_dashboard()
    context['query_penjualan_harian'] = query_penjualan_harian_dashboard(PERIODE)
    context['tren_penjualan_harian'] = tren_penjualan_harian(PERIODE)
    tren_penjualan_harian_all_crisbar(PERIODE)

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
        kunci_post_request = list(request.POST.keys())
        data_judul = request.POST.get('judul')
        data_isi = request.POST.get('isi')
        # DICOMMENT BUAT DEBUGGING AJA
        tipe = request.POST.get('tipe')
        if tipe == "harian":
            
            # EDIT INI KETIKA UDAH TAU FORMAT DATETIME APA YANG DIPAKE
            mulai_utc = datetime.fromisoformat( request.POST.get('mulai') + " " + request.POST.get('deadlinejam') + ":00+07:00" )
            selesai_utc = datetime.fromisoformat( request.POST.get('selesai') + " " + request.POST.get('deadlinejam') + ":00+07:00" )
            # EDIT INI KETIKA UDAH TAU FORMAT DATETIME APA YANG DIPAKE

            selisih = selesai_utc - mulai_utc

            if selisih.days > 0:
                banyak_isi_tugas_rutin = selisih.days + 1
                list_first_name_pemilik_tugas = kunci_post_request[8:]

                for nama in list_first_name_pemilik_tugas:
                    deadline_pemilik = mulai_utc                    
                    u = User.objects.get(first_name=nama)
                    tr = TugasRutin(pemilik_tugas = u, judul = data_judul, isi = data_isi, bagian = u.last_name, archive = False)
                    tr.save()

                    for i in range(banyak_isi_tugas_rutin):
                        itr = IsiTugasRutin(tugas_rutin = tr, deadline = deadline_pemilik, status = "On Progress", ketuntasan = False, judul = data_judul, isi = data_isi, komentar = "")
                        itr.save()
                        deadline_pemilik += timedelta(days=1)

                return redirect('lihat_tugas')
            else:
                # TAMABAHIN PESAN ERROR
                redirect('input_tugas_rutin_kelompok')
                
        else:
            banyak_tugas = int(request.POST.get('banyak-tugas'))
            pemilik_tugas = kunci_post_request[4+banyak_tugas:]

            for nama in pemilik_tugas:
                u = User.objects.get(first_name=nama)
                tr = TugasRutin(pemilik_tugas = u, judul = data_judul, isi = data_isi, bagian = u.last_name, archive = False)
                tr.save()

                for i in range(banyak_tugas):
                    deadlinenya = request.POST.get('deadline' + str(i+1))
                    deadlinenya += ':00+07:00'
                    deadlinenya = datetime.fromisoformat(deadlinenya)
                    itr = IsiTugasRutin(tugas_rutin = tr, deadline = deadlinenya, status = "On Progress", ketuntasan = False, judul = data_judul, isi = data_isi, komentar = "")
                    itr.save()

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
    tugas_rutin_ceo = rinci_tr("Management")

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
    context['tugas_rutin_ceo'] = tugas_rutin_ceo

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

        t = IsiTugasRutin.objects.get(pk=id_tugas)
        t.judul = data_judul
        t.isi = data_isi
        t.deadline = data_deadline
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
    
    periksa_hari_dalam_pemakaian_ayam()

    nama = request.user.first_name
    context = {'nama' : nama}

    query_complaint = query_complaint_dashboard(PERIODE)
    periode_kerja = PeriodeKerja.objects.get(pk=PERIODE)
    context['complaint'] = query_complaint
    context['periode_kerja'] = periode_kerja
    context['query_box_home'] = query_box_home(PERIODE)
    context['query_kepuasan_pelanggan'] = query_kepuasan_pelanggan_dashboard()
    context['query_penjualan_harian'] = query_penjualan_harian_dashboard(PERIODE)
    context['tren_penjualan_harian'] = tren_penjualan_harian(PERIODE)
    periode_kerja_sebelumnya = PeriodeKerja.objects.get(pk=PERIODE-1)
    context['periode_kerja_sebelumnya'] = periode_kerja_sebelumnya

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
    area_kopo = d.filter(area='Kopo')
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
               'area_kopo' : area_kopo,
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
    elif d.area == 'Kopo':
        context['area_kopo'] = True

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
    elif d.pendidikan == 'D1':
        context['pendidikan_d1'] = True
    elif d.pendidikan == 'S2':
        context['pendidikan_d2'] = True

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


@login_required(login_url='login')
def karyawan_onroll(request):

    if request.method == "POST":

        enroll_cisitu = request.POST.get('enroll_cisitu')
        enroll_sukajadi = request.POST.get('enroll_sukajadi')
        enroll_metro = request.POST.get('enroll_metro')
        enroll_antapani = request.POST.get('enroll_antapani')
        enroll_unjani = request.POST.get('enroll_unjani')
        enroll_sukapura = request.POST.get('enroll_sukapura')
        enroll_sukabirus = request.POST.get('enroll_sukabirus')
        enroll_kopo = request.POST.get('enroll_kopo')
        enroll_jatinangor = request.POST.get('enroll_jatinangor')

        targer_labour_cisitu = request.POST.get('target_labour_cisitu')
        targer_labour_sukajadi = request.POST.get('target_labour_sukajadi')
        targer_labour_metro = request.POST.get('target_labour_metro')
        targer_labour_antapani = request.POST.get('target_labour_antapani')
        targer_labour_unjani = request.POST.get('target_labour_unjani')
        targer_labour_sukapura = request.POST.get('target_labour_sukapura')
        targer_labour_sukabirus = request.POST.get('target_labour_sukabirus')
        targer_labour_kopo = request.POST.get('target_labour_kopo')
        targer_labour_jatinangor = request.POST.get('target_labour_jatinangor')

        cabang = ['Cisitu', 'Sukajadi', 'Metro', 'Antapani', 'Unjani', 'Telkom Sukapura', 'Telkom Sukabirus', 'Kopo', 'Jatinangor',]
        kumpulan = [
            [enroll_cisitu, targer_labour_cisitu],
            [enroll_sukajadi, targer_labour_sukajadi],
            [enroll_metro, targer_labour_metro],
            [enroll_antapani, targer_labour_antapani],
            [enroll_unjani, targer_labour_unjani],
            [enroll_sukapura, targer_labour_sukapura],
            [enroll_sukabirus, targer_labour_sukabirus],
            [enroll_kopo, targer_labour_kopo],
            [enroll_jatinangor, targer_labour_jatinangor],
        ]
        i = 0
        for c in cabang:
            onroll_dan_labour = kumpulan[i]
            i += 1      
            objek_onroll = Onroll.objects.get(cabangnya=c)
            objek_onroll.onrollnya = int(onroll_dan_labour[0])
            objek_onroll.target_labour = float(onroll_dan_labour[1])
            objek_onroll.save()

    karyawan_cisitu = len(DataKaryawan.objects.filter(area='Cisitu', status='AKTIF'))
    karyawan_sukajadi = len(DataKaryawan.objects.filter(area='Sukajadi', status='AKTIF'))
    karyawan_metro = len(DataKaryawan.objects.filter(area='Metro', status='AKTIF'))
    karyawan_antapani = len(DataKaryawan.objects.filter(area='Antapani', status='AKTIF'))
    karyawan_unjani = len(DataKaryawan.objects.filter(area='Unjani', status='AKTIF'))
    karyawan_telkom_sukapura = len(DataKaryawan.objects.filter(area='Telkom Sukapura', status='AKTIF'))
    karyawan_telkom_sukabirus = len(DataKaryawan.objects.filter(area='Telkom Sukabirus', status='AKTIF'))
    karyawan_kopo = len(DataKaryawan.objects.filter(area='Kopo', status='AKTIF'))
    karyawan_jatinangor = len(DataKaryawan.objects.filter(area='Jatinangor', status='AKTIF'))
    
    onroll_cisitu = Onroll.objects.get(cabangnya='Cisitu')
    onroll_sukajadi = Onroll.objects.get(cabangnya='Sukajadi')
    onroll_metro = Onroll.objects.get(cabangnya='Metro')
    onroll_antapani = Onroll.objects.get(cabangnya='Antapani')
    onroll_unjani = Onroll.objects.get(cabangnya='Unjani')
    onroll_telkom_sukapura = Onroll.objects.get(cabangnya='Telkom Sukapura')
    onroll_telkom_sukabirus = Onroll.objects.get(cabangnya='Telkom Sukabirus')
    onroll_kopo = Onroll.objects.get(cabangnya='Kopo')
    onroll_jatinangor = Onroll.objects.get(cabangnya='Jatinangor')

    data_actual = [
        karyawan_cisitu,
        karyawan_sukajadi,
        karyawan_metro,
        karyawan_antapani,
        karyawan_unjani,
        karyawan_telkom_sukapura,
        karyawan_telkom_sukabirus,
        karyawan_kopo,
        karyawan_jatinangor,
    ]

    data_onroll = [
        onroll_cisitu,
        onroll_sukajadi,
        onroll_metro,
        onroll_antapani,
        onroll_unjani,
        onroll_telkom_sukapura,
        onroll_telkom_sukabirus,
        onroll_kopo,
        onroll_jatinangor,
    ]

    # actual - onroll
    selisih = []
    i = 0
    for data in data_actual:
        selisih.append(data - data_onroll[i].onrollnya)
        i += 1

    list_data_onroll = [a.onrollnya for a in data_onroll]
    list_target_labour = [a.target_labour for a in data_onroll]

    total_actual = sum(data_actual)
    total_selisih = sum(selisih)
    total_onroll = sum(list_data_onroll)
    total_target_labour = sum(list_target_labour) / len(list_target_labour)
    total_target_labour = str(total_target_labour).split('.')
    total_target_labour = total_target_labour[0] + '.' + total_target_labour[1][:2]
    

    context = {
        'nama' : request.user.first_name,
        'data_actual' : data_actual,
        'data_onroll' : data_onroll,
        'total_actual' : total_actual,
        'total_selisih' : total_selisih,
        'total_onroll' : total_onroll,
        'total_target_labour' : total_target_labour,
        'selisih' : selisih
        }
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'data_karyawan/karyawan_onroll.html', context)

# ---------------------- HUMAN RESOURCE -----------------------
@login_required(login_url='login')
def index_alat_test(request):
    context = {'nama' : request.user.first_name}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'human_resource/home.html', context)

@login_required(login_url='login')
def generate_token(request):

    if request.method == 'POST':
        banyak_token = int(request.POST.get('banyak_token'))
        for i in range(banyak_token):
            t = TokenTest()
            t.generate_unique_token()
            t.save()
        return redirect('daftar_token')

    context = {'nama' : request.user.first_name}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'human_resource/generate_token.html', context)

@login_required(login_url='login')
def daftar_token(request):
    t = TokenTest.objects.all()
    context = {'nama' : request.user.first_name}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    t = TokenTest.objects.all().order_by('-aktif')
    banyak_data_per_page = 10
    p = Paginator(t, banyak_data_per_page)
    page_num = request.GET.get('page', 1)

    try:
	    page = p.page(page_num)
    except EmptyPage:
	    page = p.page(1)

    banyak_halaman = [str(a+1) for a in range(p.num_pages)]
    context['banyak_halaman'] = banyak_halaman
    context['halaman_aktif'] = str(page_num)
    context['token'] = page

    return render(request, 'human_resource/daftar_token.html', context)


@login_required(login_url='login')
def hasil_psikotes(request):
    context = {'nama' : request.user.first_name}
    t = PesertaTest.objects.all().order_by('tanggal_test')

    banyak_data_per_page = 10
    p = Paginator(t, banyak_data_per_page)
    page_num = request.GET.get('page', 1)

    try:
	    page = p.page(page_num)
    except EmptyPage:
	    page = p.page(1)

    banyak_halaman = [str(a+1) for a in range(p.num_pages)]
    context['banyak_halaman'] = banyak_halaman
    context['halaman_aktif'] = str(page_num)
    context['peserta'] = page

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    
    return render(request, 'human_resource/hasil_psikotes.html', context)

# seharusnya ada id_peserta sebagai argumen
def download_hasil_psikotes(request, id_peserta):

    p = PesertaTest.objects.get(pk=id_peserta)
    j = JawabanIst.objects.get(peserta_test=p)

    # list of list, tiap list dalam merepresentasikan baris
    datanya = [
        ['Nama : ', p.nama],
        ['Tgl Lahir / Usia : ', p.tanggal_lahir.strftime("%d %b %Y") + " / " + str(p.umur)],
        ['Tgl Tes : ', p.tanggal_test.strftime("%d %b %Y")],
        ['Pendidikan : ', p.pendidikan_terakhir],
        ['', ''],
        ['SE', '', '', 'WA', '', '', 'AN', '', '', 'GE', '', '', 'RA', '', '', 'ZR', '', '', 'FA', '', '', 'WU', '', '', 'ME'],
        ['No', 'Jawaban Klien', '', 'No', 'Jawaban Klien', '', 'No', 'Jawaban Klien', '', 'No', 'Jawaban Klien', '', 'No', 'Jawaban Klien', '', 'No', 'Jawaban Klien', '', 'No', 'Jawaban Klien', '', 'No', 'Jawaban Klien', '', 'No', 'Jawaban Klien'],
        ['1. ', j.se_1, '',  '21', j.wa_1, '', '41', j.an_1, '', '61', j.ge_1,  '', '77', j.ra_1,  '', '97', j.zr_1,  '',  '117', j.fa_1,  '', '137', j.wu_1,  '', '157', j.me_1],
        ['2. ', j.se_2, '',  '22', j.wa_2, '', '42', j.an_2, '', '62', j.ge_2,  '', '78', j.ra_2,  '', '98', j.zr_2,  '',  '118', j.fa_2,  '', '138', j.wu_2,  '', '158',j.me_2],
        ['3. ', j.se_3, '',  '23', j.wa_3, '', '43', j.an_3, '', '63', j.ge_3,  '', '79', j.ra_3,  '', '99', j.zr_3,  '',  '119', j.fa_3,  '', '139', j.wu_3,  '', '159',j.me_3],
        ['4. ', j.se_4, '',  '24', j.wa_4, '', '44', j.an_4, '', '64', j.ge_4,  '', '80', j.ra_4,  '', '100', j.zr_4,  '', '120', j.fa_4,  '', '140', j.wu_4,  '', '160',j.me_4],
        ['5. ', j.se_5, '',  '25', j.wa_5, '', '45', j.an_5, '', '65', j.ge_5,  '', '81', j.ra_5,  '', '101', j.zr_5,  '', '121', j.fa_5,  '', '141', j.wu_5,  '', '161',j.me_5],
        ['6. ', j.se_6, '',  '26', j.wa_6, '', '46', j.an_6, '', '66', j.ge_6,  '', '82', j.ra_6,  '', '102', j.zr_6,  '', '122', j.fa_6,  '', '142', j.wu_6,  '', '162',j.me_6],
        ['7. ', j.se_7, '',  '27', j.wa_7, '', '47', j.an_7, '', '67', j.ge_7,  '', '83', j.ra_7,  '', '103', j.zr_7,  '', '123', j.fa_7,  '', '143', j.wu_7,  '', '163',j.me_7],
        ['8. ', j.se_8, '',  '28', j.wa_8, '', '48', j.an_8, '', '68', j.ge_8,  '', '84', j.ra_8,  '', '104', j.zr_8,  '', '124', j.fa_8,  '', '144', j.wu_8,  '', '164',j.me_8],
        ['9. ', j.se_9, '',  '29', j.wa_9, '', '49', j.an_9, '', '69', j.ge_9,  '', '85', j.ra_9,  '', '105', j.zr_9,  '', '125', j.fa_9,  '', '145', j.wu_9,  '', '165',j.me_9],
        ['10. ',j.se_10, '', '30', j.wa_10, '','50', j.an_10, '','70', j.ge_10, '', '86', j.ra_10, '', '106', j.zr_10, '', '126', j.fa_10, '', '146', j.wu_10, '', '166',j.me_10],
        ['11. ',j.se_11, '', '31', j.wa_11, '','51', j.an_11, '','71', j.ge_11, '', '87', j.ra_11, '', '107', j.zr_11, '', '127', j.fa_11, '', '147', j.wu_11, '', '167',j.me_11],
        ['12. ',j.se_12, '', '32', j.wa_12, '','52', j.an_12, '','72', j.ge_12, '', '88', j.ra_12, '', '108', j.zr_12, '', '128', j.fa_12, '', '148', j.wu_12, '', '168',j.me_12],
        ['13. ',j.se_13, '', '33', j.wa_13, '','53', j.an_13, '','73', j.ge_13, '', '89', j.ra_13, '', '109', j.zr_13, '', '129', j.fa_13, '', '149', j.wu_13, '', '169',j.me_13],
        ['14. ',j.se_14, '', '34', j.wa_14, '','54', j.an_14, '','74', j.ge_14, '', '90', j.ra_14, '', '110', j.zr_14, '', '130', j.fa_14, '', '150', j.wu_14, '', '170',j.me_14],
        ['15. ',j.se_15, '', '35', j.wa_15, '','55', j.an_15, '','75', j.ge_15, '', '91', j.ra_15, '', '111',j.zr_15, '',  '131', j.fa_15, '', '151', j.wu_15, '', '171',j.me_15],
        ['16. ',j.se_16, '', '36', j.wa_16, '','56', j.an_16, '','76', j.ge_16, '', '92', j.ra_16, '', '112',j.zr_16, '',  '132', j.fa_16, '', '152', j.wu_16, '', '172',j.me_16],
        ['17. ',j.se_17, '', '37', j.wa_17, '','57', j.an_17, '',  '', '',      '', '93', j.ra_17, '', '113',j.zr_17, '',  '133', j.fa_17, '', '153', j.wu_17, '', '173',j.me_17],
        ['18. ',j.se_18, '', '38', j.wa_18, '','58', j.an_18, '',  '', '',      '', '94', j.ra_18, '', '114',j.zr_18, '',  '134', j.fa_18, '', '154', j.wu_18, '', '174',j.me_18],
        ['19. ',j.se_19, '', '39', j.wa_19, '','59', j.an_19, '',  '', '',      '', '95', j.ra_19, '', '115',j.zr_19, '',  '135', j.fa_19, '', '155', j.wu_19, '', '175',j.me_19],
        ['20. ',j.se_20, '', '40', j.wa_20, '','60', j.an_20, '',  '', '',      '', '96', j.ra_20, '', '116',j.zr_20, '',  '136', j.fa_20, '', '156', j.wu_20, '', '176',j.me_20],
        ['', '','','','','','','','','','','','','','','','','','','','','','','','','',],
        ['DISC', '','','','','','','','','','','','','','','','','','','','','','','','','',],
        ['NO','M','L','','NO','M','L','','NO','M','L',],
        ['1', j.m1, j.l1, '', '9' , j.m9 , j.l9 , '', '17', j.m17, j.l17],
        ['2', j.m2, j.l2, '', '10', j.m10, j.l10, '', '18', j.m18, j.l18],
        ['3', j.m3, j.l3, '', '11', j.m11, j.l11, '', '19', j.m19, j.l19],
        ['4', j.m4, j.l4, '', '12', j.m12, j.l12, '', '20', j.m20, j.l20],
        ['5', j.m5, j.l5, '', '13', j.m13, j.l13, '', '21', j.m21, j.l21],
        ['6', j.m6, j.l6, '', '14', j.m14, j.l14, '', '22', j.m22, j.l22],
        ['7', j.m7, j.l7, '', '15', j.m15, j.l15, '', '23', j.m23, j.l23],
        ['8', j.m8, j.l8, '', '16', j.m16, j.l16, '', '24', j.m24, j.l24],
        
    ]

    return django_excel.make_response_from_array(datanya, "xls", file_name="hasil_psikotes")

# ---------------------- PESERTA PSIKOTES -------------------------------
def psikotes(request):
    context = {}
    if request.method == "POST":
        tokennya = request.POST.get('kode_test')
        try:
            t = TokenTest.objects.get(token=tokennya)
            if t.aktif:
                t.aktif = False
                t.save()
                request.session['kode_tes'] = t.token
                return redirect('data_peserta_psikotes')
            else:
                context['pesan'] = "Kode tes sudah digunakan"
        except:
            pesan = "Kode test salah"
            context['pesan'] = pesan

    return render(request, 'psikotes/index.html', context)

def data_peserta_psikotes(request):
    kode_test = request.session['kode_tes']
    try:
        t = TokenTest.objects.get(token=kode_test)
    except:
        return redirect('psikotes')

    if request.method == "POST":
        p = PesertaTest(
            token = t,
            nama = request.POST.get('nama'),
            tanggal_lahir = date.fromisoformat(request.POST.get('tanggal_lahir')),
            pendidikan_terakhir = request.POST.get('pendidikan_terakhir'),
            tanggal_test = date.today()
        )
        p.hitung_umur()
        p.save()
        request.session['id_peserta'] = str(p.id)
        return redirect('pendahuluan')

    context = {'tanggal_test' : date.today()}
    return render(request, 'psikotes/daftar_peserta_psikotes.html', context)

def pendahuluan(request):
    return render(request, 'psikotes/soal/pendahuluan.html')

def petunjuk_1(request):
    if ('id_peserta' not in request.session):
        return redirect('psikotes')
    return render(request, 'psikotes/soal/1_petunjuk.html')

def soal_se_2(request):

    if ('id_peserta' not in request.session):
        return redirect('psikotes')

    if request.method == "POST":
        peserta = PesertaTest.objects.get(pk=int(request.session['id_peserta']))
        j = JawabanIst(
            peserta_test = peserta,
            se_1 = request.POST.get('1_se') if request.POST.get('1_se') != None else '',
            se_2 = request.POST.get('2_se') if request.POST.get('2_se') != None else '',
            se_3 = request.POST.get('3_se') if request.POST.get('3_se') != None else '',
            se_4 = request.POST.get('4_se') if request.POST.get('4_se') != None else '',
            se_5 = request.POST.get('5_se') if request.POST.get('5_se') != None else '',
            se_6 = request.POST.get('6_se') if request.POST.get('6_se') != None else '',
            se_7 = request.POST.get('7_se') if request.POST.get('7_se') != None else '',
            se_8 = request.POST.get('8_se') if request.POST.get('8_se') != None else '',
            se_9 = request.POST.get('9_se') if request.POST.get('9_se') != None else '',
            se_10 = request.POST.get('10_se') if request.POST.get('10_se') != None else '',
            se_11 = request.POST.get('11_se') if request.POST.get('11_se') != None else '',
            se_12 = request.POST.get('12_se') if request.POST.get('12_se') != None else '',
            se_13 = request.POST.get('13_se') if request.POST.get('13_se') != None else '',
            se_14 = request.POST.get('14_se') if request.POST.get('14_se') != None else '',
            se_15 = request.POST.get('15_se') if request.POST.get('15_se') != None else '',
            se_16 = request.POST.get('16_se') if request.POST.get('16_se') != None else '',
            se_17 = request.POST.get('17_se') if request.POST.get('17_se') != None else '',
            se_18 = request.POST.get('18_se') if request.POST.get('18_se') != None else '',
            se_19 = request.POST.get('19_se') if request.POST.get('19_se') != None else '',
            se_20 = request.POST.get('20_se') if request.POST.get('20_se') != None else ''
        )
        j.save()
        del request.session['id_peserta']
        request.session['id_jawaban'] = str(j.id)
        request.session['halaman'] = '2'

        return redirect('petunjuk_3')        

    return render(request, 'psikotes/soal/2_se.html')

def petunjuk_3(request):

    if 'halaman' in request.session:
        if (request.session['halaman'] not in ['2', '3']):
            return redirect('psikotes')
    else:
        return redirect('psikotes')

    request.session['halaman'] = '3'
    return render(request, 'psikotes/soal/3_petunjuk.html')

def soal_wa_4(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['3', '4']):
        return redirect('psikotes')

    request.session['halaman'] = '4'
    if request.method == "POST":
        j = JawabanIst.objects.get(pk=int(request.session['id_jawaban']))
        j.wa_1 = request.POST.get('1_wa') if request.POST.get('1_wa') != None else ''
        j.wa_2 = request.POST.get('2_wa') if request.POST.get('2_wa') != None else ''
        j.wa_3 = request.POST.get('3_wa') if request.POST.get('3_wa') != None else ''
        j.wa_4 = request.POST.get('4_wa') if request.POST.get('4_wa') != None else ''
        j.wa_5 = request.POST.get('5_wa') if request.POST.get('5_wa') != None else ''
        j.wa_6 = request.POST.get('6_wa') if request.POST.get('6_wa') != None else ''
        j.wa_7 = request.POST.get('7_wa') if request.POST.get('7_wa') != None else ''
        j.wa_8 = request.POST.get('8_wa') if request.POST.get('8_wa') != None else ''
        j.wa_9 = request.POST.get('9_wa') if request.POST.get('9_wa') != None else ''
        j.wa_10 = request.POST.get('10_wa') if request.POST.get('10_wa') != None else ''
        j.wa_11 = request.POST.get('11_wa') if request.POST.get('11_wa') != None else ''
        j.wa_12 = request.POST.get('12_wa') if request.POST.get('12_wa') != None else ''
        j.wa_13 = request.POST.get('13_wa') if request.POST.get('13_wa') != None else ''
        j.wa_14 = request.POST.get('14_wa') if request.POST.get('14_wa') != None else ''
        j.wa_15 = request.POST.get('15_wa') if request.POST.get('15_wa') != None else ''
        j.wa_16 = request.POST.get('16_wa') if request.POST.get('16_wa') != None else ''
        j.wa_17 = request.POST.get('17_wa') if request.POST.get('17_wa') != None else ''
        j.wa_18 = request.POST.get('18_wa') if request.POST.get('18_wa') != None else ''
        j.wa_19 = request.POST.get('19_wa') if request.POST.get('19_wa') != None else ''
        j.wa_20 = request.POST.get('20_wa') if request.POST.get('20_wa') != None else ''
        j.save()
        return redirect('petunjuk_5')

    return render(request, 'psikotes/soal/4_wa.html')

def petunjuk_5(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['4', '5']):
        return redirect('psikotes')

    request.session['halaman'] = '5'
    return render(request, 'psikotes/soal/5_petunjuk.html')

def soal_an_6(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['5','6']):
        return redirect('psikotes')

    request.session['halaman'] = '6'
    if request.method == "POST":
        j = JawabanIst.objects.get(pk=int(request.session['id_jawaban']))
        j.an_1 = request.POST.get('1_an') if request.POST.get('1_an') != None else ''
        j.an_2 = request.POST.get('2_an') if request.POST.get('2_an') != None else ''
        j.an_3 = request.POST.get('3_an') if request.POST.get('3_an') != None else ''
        j.an_4 = request.POST.get('4_an') if request.POST.get('4_an') != None else ''
        j.an_5 = request.POST.get('5_an') if request.POST.get('5_an') != None else ''
        j.an_6 = request.POST.get('6_an') if request.POST.get('6_an') != None else ''
        j.an_7 = request.POST.get('7_an') if request.POST.get('7_an') != None else ''
        j.an_8 = request.POST.get('8_an') if request.POST.get('8_an') != None else ''
        j.an_9 = request.POST.get('9_an') if request.POST.get('9_an') != None else ''
        j.an_10 = request.POST.get('10_an') if request.POST.get('10_an') != None else ''
        j.an_11 = request.POST.get('11_an') if request.POST.get('11_an') != None else ''
        j.an_12 = request.POST.get('12_an') if request.POST.get('12_an') != None else ''
        j.an_13 = request.POST.get('13_an') if request.POST.get('13_an') != None else ''
        j.an_14 = request.POST.get('14_an') if request.POST.get('14_an') != None else ''
        j.an_15 = request.POST.get('15_an') if request.POST.get('15_an') != None else ''
        j.an_16 = request.POST.get('16_an') if request.POST.get('16_an') != None else ''
        j.an_17 = request.POST.get('17_an') if request.POST.get('17_an') != None else ''
        j.an_18 = request.POST.get('18_an') if request.POST.get('18_an') != None else ''
        j.an_19 = request.POST.get('19_an') if request.POST.get('19_an') != None else ''
        j.an_20 = request.POST.get('20_an') if request.POST.get('20_an') != None else ''
        j.save()
        return redirect('petunjuk_7')

    return render(request, 'psikotes/soal/6_an.html')

def petunjuk_7(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['6', '7']):
        return redirect('psikotes')

    request.session['halaman'] = '7'
    return render(request, 'psikotes/soal/7_petunjuk.html')

def soal_ge_8(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['7', '8']):
        return redirect('psikotes')

    request.session['halaman'] = '8'

    if request.method == "POST":
        j = JawabanIst.objects.get(pk=int(request.session['id_jawaban']))
        j.ge_1 = request.POST.get('1_ge') if request.POST.get('1_ge') != None else ''
        j.ge_2 = request.POST.get('2_ge') if request.POST.get('2_ge') != None else ''
        j.ge_3 = request.POST.get('3_ge') if request.POST.get('3_ge') != None else ''
        j.ge_4 = request.POST.get('4_ge') if request.POST.get('4_ge') != None else ''
        j.ge_5 = request.POST.get('5_ge') if request.POST.get('5_ge') != None else ''
        j.ge_6 = request.POST.get('6_ge') if request.POST.get('6_ge') != None else ''
        j.ge_7 = request.POST.get('7_ge') if request.POST.get('7_ge') != None else ''
        j.ge_8 = request.POST.get('8_ge') if request.POST.get('8_ge') != None else ''
        j.ge_9 = request.POST.get('9_ge') if request.POST.get('9_ge') != None else ''
        j.ge_10 = request.POST.get('10_ge') if request.POST.get('10_ge') != None else ''
        j.ge_11 = request.POST.get('11_ge') if request.POST.get('11_ge') != None else ''
        j.ge_12 = request.POST.get('12_ge') if request.POST.get('12_ge') != None else ''
        j.ge_13 = request.POST.get('13_ge') if request.POST.get('13_ge') != None else ''
        j.ge_14 = request.POST.get('14_ge') if request.POST.get('14_ge') != None else ''
        j.ge_15 = request.POST.get('15_ge') if request.POST.get('15_ge') != None else ''
        j.ge_16 = request.POST.get('16_ge') if request.POST.get('16_ge') != None else ''
        j.save()
        return redirect('petunjuk_9')

    return render(request, 'psikotes/soal/8_ge.html')

def petunjuk_9(request):
    
    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['8', '9']):
        return redirect('psikotes')

    request.session['halaman'] = '9'
    return render(request, 'psikotes/soal/9_petunjuk.html')

def soal_ra_10(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['9', '10']):
        return redirect('psikotes')

    request.session['halaman'] = '10'

    if request.method == "POST":
        j = JawabanIst.objects.get(pk=int(request.session['id_jawaban']))
        j.ra_1 = request.POST.get('1_ra') if request.POST.get('1_ra') != None else ''
        j.ra_2 = request.POST.get('2_ra') if request.POST.get('2_ra') != None else ''
        j.ra_3 = request.POST.get('3_ra') if request.POST.get('3_ra') != None else ''
        j.ra_4 = request.POST.get('4_ra') if request.POST.get('4_ra') != None else ''
        j.ra_5 = request.POST.get('5_ra') if request.POST.get('5_ra') != None else ''
        j.ra_6 = request.POST.get('6_ra') if request.POST.get('6_ra') != None else ''
        j.ra_7 = request.POST.get('7_ra') if request.POST.get('7_ra') != None else ''
        j.ra_8 = request.POST.get('8_ra') if request.POST.get('8_ra') != None else ''
        j.ra_9 = request.POST.get('9_ra') if request.POST.get('9_ra') != None else ''
        j.ra_10 = request.POST.get('10_ra') if request.POST.get('10_ra') != None else ''
        j.ra_11 = request.POST.get('11_ra') if request.POST.get('11_ra') != None else ''
        j.ra_12 = request.POST.get('12_ra') if request.POST.get('12_ra') != None else ''
        j.ra_13 = request.POST.get('13_ra') if request.POST.get('13_ra') != None else ''
        j.ra_14 = request.POST.get('14_ra') if request.POST.get('14_ra') != None else ''
        j.ra_15 = request.POST.get('15_ra') if request.POST.get('15_ra') != None else ''
        j.ra_16 = request.POST.get('16_ra') if request.POST.get('16_ra') != None else ''
        j.ra_17 = request.POST.get('17_ra') if request.POST.get('17_ra') != None else ''
        j.ra_18 = request.POST.get('18_ra') if request.POST.get('18_ra') != None else ''
        j.ra_19 = request.POST.get('19_ra') if request.POST.get('19_ra') != None else ''
        j.ra_20 = request.POST.get('20_ra') if request.POST.get('20_ra') != None else ''
        j.save()
        return redirect('petunjuk_11')

    return render(request, 'psikotes/soal/10_ra.html')

def petunjuk_11(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['10', '11']):
        return redirect('psikotes')

    request.session['halaman'] = '11'
    return render(request, 'psikotes/soal/11_petunjuk.html')

def soal_zr_12(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['11', '12']):
        return redirect('psikotes')

    request.session['halaman'] = '12'

    if request.method == "POST":
        j = JawabanIst.objects.get(pk=int(request.session['id_jawaban']))
        j.zr_1 = request.POST.get('1_zr') if request.POST.get('1_zr') != None else ''
        j.zr_2 = request.POST.get('2_zr') if request.POST.get('2_zr') != None else ''
        j.zr_3 = request.POST.get('3_zr') if request.POST.get('3_zr') != None else ''
        j.zr_4 = request.POST.get('4_zr') if request.POST.get('4_zr') != None else ''
        j.zr_5 = request.POST.get('5_zr') if request.POST.get('5_zr') != None else ''
        j.zr_6 = request.POST.get('6_zr') if request.POST.get('6_zr') != None else ''
        j.zr_7 = request.POST.get('7_zr') if request.POST.get('7_zr') != None else ''
        j.zr_8 = request.POST.get('8_zr') if request.POST.get('8_zr') != None else ''
        j.zr_9 = request.POST.get('9_zr') if request.POST.get('9_zr') != None else ''
        j.zr_10 = request.POST.get('10_zr') if request.POST.get('10_zr') != None else ''
        j.zr_11 = request.POST.get('11_zr') if request.POST.get('11_zr') != None else ''
        j.zr_12 = request.POST.get('12_zr') if request.POST.get('12_zr') != None else ''
        j.zr_13 = request.POST.get('13_zr') if request.POST.get('13_zr') != None else ''
        j.zr_14 = request.POST.get('14_zr') if request.POST.get('14_zr') != None else ''
        j.zr_15 = request.POST.get('15_zr') if request.POST.get('15_zr') != None else ''
        j.zr_16 = request.POST.get('16_zr') if request.POST.get('16_zr') != None else ''
        j.zr_17 = request.POST.get('17_zr') if request.POST.get('17_zr') != None else ''
        j.zr_18 = request.POST.get('18_zr') if request.POST.get('18_zr') != None else ''
        j.zr_19 = request.POST.get('19_zr') if request.POST.get('19_zr') != None else ''
        j.zr_20 = request.POST.get('20_zr') if request.POST.get('20_zr') != None else ''
        j.save()
        return redirect('petunjuk_13')

    return render(request, 'psikotes/soal/12_zr.html')

def petunjuk_13(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['12', '13']):
        return redirect('psikotes')

    request.session['halaman'] = '13'
    return render(request, 'psikotes/soal/13_petunjuk.html')

def soal_fa_14(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['13', '14']):
        return redirect('psikotes')

    request.session['halaman'] = '14'

    if request.method == "POST":
        j = JawabanIst.objects.get(pk=int(request.session['id_jawaban']))
        j.fa_1 = request.POST.get('1_fa') if request.POST.get('1_fa') != None else ''
        j.fa_2 = request.POST.get('2_fa') if request.POST.get('2_fa') != None else ''
        j.fa_3 = request.POST.get('3_fa') if request.POST.get('3_fa') != None else ''
        j.fa_4 = request.POST.get('4_fa') if request.POST.get('4_fa') != None else ''
        j.fa_5 = request.POST.get('5_fa') if request.POST.get('5_fa') != None else ''
        j.fa_6 = request.POST.get('6_fa') if request.POST.get('6_fa') != None else ''
        j.fa_7 = request.POST.get('7_fa') if request.POST.get('7_fa') != None else ''
        j.fa_8 = request.POST.get('8_fa') if request.POST.get('8_fa') != None else ''
        j.fa_9 = request.POST.get('9_fa') if request.POST.get('9_fa') != None else ''
        j.fa_10 = request.POST.get('10_fa') if request.POST.get('10_fa') != None else ''
        j.fa_11 = request.POST.get('11_fa') if request.POST.get('11_fa') != None else ''
        j.fa_12 = request.POST.get('12_fa') if request.POST.get('12_fa') != None else ''
        j.fa_13 = request.POST.get('13_fa') if request.POST.get('13_fa') != None else ''
        j.fa_14 = request.POST.get('14_fa') if request.POST.get('14_fa') != None else ''
        j.fa_15 = request.POST.get('15_fa') if request.POST.get('15_fa') != None else ''
        j.fa_16 = request.POST.get('16_fa') if request.POST.get('16_fa') != None else ''
        j.fa_17 = request.POST.get('17_fa') if request.POST.get('17_fa') != None else ''
        j.fa_18 = request.POST.get('18_fa') if request.POST.get('18_fa') != None else ''
        j.fa_19 = request.POST.get('19_fa') if request.POST.get('19_fa') != None else ''
        j.fa_20 = request.POST.get('20_fa') if request.POST.get('20_fa') != None else ''
        j.save()
        return redirect('petunjuk_15')

    return render(request, 'psikotes/soal/14_fa.html')

def petunjuk_15(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['14', '15']):
        return redirect('psikotes')

    request.session['halaman'] = '15'
    return render(request, 'psikotes/soal/15_petunjuk.html')

def soal_wu_16(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['15', '16']):
        return redirect('psikotes')

    request.session['halaman'] = '16'

    if request.method == "POST":
        j = JawabanIst.objects.get(pk=int(request.session['id_jawaban']))
        j.wu_1 = request.POST.get('1_wu') if request.POST.get('1_wu') != None else ''
        j.wu_2 = request.POST.get('2_wu') if request.POST.get('2_wu') != None else ''
        j.wu_3 = request.POST.get('3_wu') if request.POST.get('3_wu') != None else ''
        j.wu_4 = request.POST.get('4_wu') if request.POST.get('4_wu') != None else ''
        j.wu_5 = request.POST.get('5_wu') if request.POST.get('5_wu') != None else ''
        j.wu_6 = request.POST.get('6_wu') if request.POST.get('6_wu') != None else ''
        j.wu_7 = request.POST.get('7_wu') if request.POST.get('7_wu') != None else ''
        j.wu_8 = request.POST.get('8_wu') if request.POST.get('8_wu') != None else ''
        j.wu_9 = request.POST.get('9_wu') if request.POST.get('9_wu') != None else ''
        j.wu_10 = request.POST.get('10_wu') if request.POST.get('10_wu') != None else ''
        j.wu_11 = request.POST.get('11_wu') if request.POST.get('11_wu') != None else ''
        j.wu_12 = request.POST.get('12_wu') if request.POST.get('12_wu') != None else ''
        j.wu_13 = request.POST.get('13_wu') if request.POST.get('13_wu') != None else ''
        j.wu_14 = request.POST.get('14_wu') if request.POST.get('14_wu') != None else ''
        j.wu_15 = request.POST.get('15_wu') if request.POST.get('15_wu') != None else ''
        j.wu_16 = request.POST.get('16_wu') if request.POST.get('16_wu') != None else ''
        j.wu_17 = request.POST.get('17_wu') if request.POST.get('17_wu') != None else ''
        j.wu_18 = request.POST.get('18_wu') if request.POST.get('18_wu') != None else ''
        j.wu_19 = request.POST.get('19_wu') if request.POST.get('19_wu') != None else ''
        j.wu_20 = request.POST.get('20_wu') if request.POST.get('20_wu') != None else ''
        j.save()
        return redirect('petunjuk_17')

    return render(request, 'psikotes/soal/16_wu.html')

def petunjuk_17(request):
    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['16', '17']):
        return redirect('psikotes')

    request.session['halaman'] = '17'
    return render(request, 'psikotes/soal/17_petunjuk.html')

def hafalan_18(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['17', '18']):
        return redirect('psikotes')


    request.session['halaman'] = '18'
    return render(request, 'psikotes/soal/18_hafalan.html')

def soal_me_19(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['18', '19']):
        return redirect('psikotes')

    request.session['halaman'] = '19'

    if request.method == "POST":
        j = JawabanIst.objects.get(pk=int(request.session['id_jawaban']))
        j.me_1 = request.POST.get('1_me') if request.POST.get('1_me') != None else ''
        j.me_2 = request.POST.get('2_me') if request.POST.get('2_me') != None else ''
        j.me_3 = request.POST.get('3_me') if request.POST.get('3_me') != None else ''
        j.me_4 = request.POST.get('4_me') if request.POST.get('4_me') != None else ''
        j.me_5 = request.POST.get('5_me') if request.POST.get('5_me') != None else ''
        j.me_6 = request.POST.get('6_me') if request.POST.get('6_me') != None else ''
        j.me_7 = request.POST.get('7_me') if request.POST.get('7_me') != None else ''
        j.me_8 = request.POST.get('8_me') if request.POST.get('8_me') != None else ''
        j.me_9 = request.POST.get('9_me') if request.POST.get('9_me') != None else ''
        j.me_10 = request.POST.get('10_me') if request.POST.get('10_me') != None else ''
        j.me_11 = request.POST.get('11_me') if request.POST.get('11_me') != None else ''
        j.me_12 = request.POST.get('12_me') if request.POST.get('12_me') != None else ''
        j.me_13 = request.POST.get('13_me') if request.POST.get('13_me') != None else ''
        j.me_14 = request.POST.get('14_me') if request.POST.get('14_me') != None else ''
        j.me_15 = request.POST.get('15_me') if request.POST.get('15_me') != None else ''
        j.me_16 = request.POST.get('16_me') if request.POST.get('16_me') != None else ''
        j.me_17 = request.POST.get('17_me') if request.POST.get('17_me') != None else ''
        j.me_18 = request.POST.get('18_me') if request.POST.get('18_me') != None else ''
        j.me_19 = request.POST.get('19_me') if request.POST.get('19_me') != None else ''
        j.me_20 = request.POST.get('20_me') if request.POST.get('20_me') != None else ''
        j.save()
        return redirect('disc')

    return render(request, 'psikotes/soal/19_me.html')
    

def disc(request):

    if 'halaman' not in request.session:
        return redirect('psikotes')
    elif (request.session['halaman'] not in ['19', '20']):
        return redirect('psikotes')

    request.session['halaman'] = '20'

    if request.method == 'POST':
        j = JawabanIst.objects.get(pk=int(request.session['id_jawaban']))
        # nomor 1
        j.m1 = request.POST.get('1_m_disc') if request.POST.get('1_m_disc') != None else ''
        j.l1 = request.POST.get('1_l_disc') if request.POST.get('1_l_disc') != None else ''

        # nomor 2
        j.m2 = request.POST.get('2_m_disc') if request.POST.get('2_m_disc') != None else ''
        j.l2 = request.POST.get('2_l_disc') if request.POST.get('2_l_disc') != None else ''

        # nomor 3
        j.m3 = request.POST.get('3_m_disc') if request.POST.get('3_m_disc') != None else ''
        j.l3 = request.POST.get('3_l_disc') if request.POST.get('3_l_disc') != None else ''
        
        # nomor 4
        j.m4 = request.POST.get('4_m_disc') if request.POST.get('4_m_disc') != None else ''
        j.l4 = request.POST.get('4_l_disc') if request.POST.get('4_l_disc') != None else ''
        
        # nomor 5
        j.m5 = request.POST.get('5_m_disc') if request.POST.get('5_m_disc') != None else ''
        j.l5 = request.POST.get('5_l_disc') if request.POST.get('5_l_disc') != None else ''
        
        # nomor 6
        j.m6 = request.POST.get('6_m_disc') if request.POST.get('6_m_disc') != None else ''
        j.l6 = request.POST.get('6_l_disc') if request.POST.get('6_l_disc') != None else ''
        
        # nomor 7
        j.m7 = request.POST.get('7_m_disc') if request.POST.get('7_m_disc') != None else ''
        j.l7 = request.POST.get('7_l_disc') if request.POST.get('7_l_disc') != None else ''
        
        # nomor 8
        j.m8 = request.POST.get('8_m_disc') if request.POST.get('8_m_disc') != None else ''
        j.l8 = request.POST.get('8_l_disc') if request.POST.get('8_l_disc') != None else ''
        
        # nomor 9
        j.m9 = request.POST.get('9_m_disc') if request.POST.get('9_m_disc') != None else ''
        j.l9 = request.POST.get('9_l_disc') if request.POST.get('9_l_disc') != None else ''
        
        # nomor 10
        j.m10 = request.POST.get('10_m_disc') if request.POST.get('10_m_disc') != None else ''
        j.l10 = request.POST.get('10_l_disc') if request.POST.get('10_l_disc') != None else ''
        
        # nomor 11
        j.m11 = request.POST.get('11_m_disc') if request.POST.get('11_m_disc') != None else ''
        j.l11 = request.POST.get('11_l_disc') if request.POST.get('11_l_disc') != None else ''
        
        # nomor 12
        j.m12 = request.POST.get('12_m_disc') if request.POST.get('12_m_disc') != None else ''
        j.l12 = request.POST.get('12_l_disc') if request.POST.get('12_l_disc') != None else ''
        
        # nomor 13
        j.m13 = request.POST.get('13_m_disc') if request.POST.get('13_m_disc') != None else ''
        j.l13 = request.POST.get('13_l_disc') if request.POST.get('13_l_disc') != None else ''
        
        # nomor 14
        j.m14 = request.POST.get('14_m_disc') if request.POST.get('14_m_disc') != None else ''
        j.l14 = request.POST.get('14_l_disc') if request.POST.get('14_l_disc') != None else ''
        
        # nomor 15
        j.m15 = request.POST.get('15_m_disc') if request.POST.get('15_m_disc') != None else ''
        j.l15 = request.POST.get('15_l_disc') if request.POST.get('15_l_disc') != None else ''
        
        # nomor 16
        j.m16 = request.POST.get('16_m_disc') if request.POST.get('16_m_disc') != None else ''
        j.l16 = request.POST.get('16_l_disc') if request.POST.get('16_l_disc') != None else ''
        
        # nomor 17
        j.m17 = request.POST.get('17_m_disc') if request.POST.get('17_m_disc') != None else ''
        j.l17 = request.POST.get('17_l_disc') if request.POST.get('17_l_disc') != None else ''
        
        # nomor 18
        j.m18 = request.POST.get('18_m_disc') if request.POST.get('18_m_disc') != None else ''
        j.l18 = request.POST.get('18_l_disc') if request.POST.get('18_l_disc') != None else ''
        
        # nomor 19
        j.m19 = request.POST.get('19_m_disc') if request.POST.get('19_m_disc') != None else ''
        j.l19 = request.POST.get('19_l_disc') if request.POST.get('19_l_disc') != None else ''
        
        # nomor 20
        j.m20 = request.POST.get('20_m_disc') if request.POST.get('20_m_disc') != None else ''
        j.l20 = request.POST.get('20_l_disc') if request.POST.get('20_l_disc') != None else ''
        
        # nomor 21
        j.m21 = request.POST.get('21_m_disc') if request.POST.get('21_m_disc') != None else ''
        j.l21 = request.POST.get('21_l_disc') if request.POST.get('21_l_disc') != None else ''
        
        # nomor 22
        j.m22 = request.POST.get('22_m_disc') if request.POST.get('22_m_disc') != None else ''
        j.l22 = request.POST.get('22_l_disc') if request.POST.get('22_l_disc') != None else ''
        
        # nomor 23
        j.m23 = request.POST.get('23_m_disc') if request.POST.get('23_m_disc') != None else ''
        j.l23 = request.POST.get('23_l_disc') if request.POST.get('23_l_disc') != None else ''
        
        # nomor 24
        j.m24 = request.POST.get('24_m_disc') if request.POST.get('24_m_disc') != None else ''
        j.l24 = request.POST.get('24_l_disc') if request.POST.get('24_l_disc') != None else ''
        j.save()
        return redirect('psikotes')

        # print(m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24)
        # print(l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20, l21, l22, l23, l24)

    return render(request, 'psikotes/soal/disc.html')

# ---------------------- MARKETING -------------------------------
@login_required(login_url='login')
def complaint_list(request):
    context = {'nama' : request.user.first_name}
    c = Complaint.objects.all().order_by('-tanggal')
    
    banyak_data_per_page = 10
    p = Paginator(c, banyak_data_per_page)
    page_num = request.GET.get('page', 1)

    try:
	    page = p.page(page_num)
    except EmptyPage:
	    page = p.page(1)

    banyak_halaman = [str(a+1) for a in range(p.num_pages)]
    context['banyak_halaman'] = banyak_halaman
    context['halaman_aktif'] = str(page_num)
    context['complaint'] = page

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
    mg = mg.order_by('-tanggal')
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


@login_required(login_url='login')
def kepuasan_pelanggan(request):
    kp = KepuasanPelanggan.objects.all().order_by('-tanggal')
    context = {'nama' : request.user.first_name, 'kepuasan_pelanggan' : kp}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    return render(request, 'marketing/kepuasan_pelanggan.html', context)

@login_required(login_url='login')
def input_kepuasan_pelanggan(request):

    if request.method == 'POST':
        kp = KepuasanPelanggan(
            tanggal = request.POST.get('tanggal'),

            google_antapani = request.POST.get('google_antapani'),
            google_cisitu = request.POST.get('google_cisitu'),
            google_jatinangor  = request.POST.get('google_jatinangor'),
            google_metro = request.POST.get('google_metro'),
            google_sukabirus  = request.POST.get('google_sukabirus'),
            google_sukapura  = request.POST.get('google_sukapura'),
            google_sukajadi  = request.POST.get('google_sukajadi'),
            google_unjani = request.POST.get('google_unjani'),

            gofood_antapani = request.POST.get('gofood_antapani'),
            gofood_cisitu = request.POST.get('gofood_cisitu'),
            gofood_jatinangor  = request.POST.get('gofood_jatinangor'),
            gofood_metro = request.POST.get('gofood_metro'),
            gofood_sukabirus  = request.POST.get('gofood_sukabirus'),
            gofood_sukapura  = request.POST.get('gofood_sukapura'),
            gofood_sukajadi  = request.POST.get('gofood_sukajadi'),
            gofood_unjani = request.POST.get('gofood_unjani'),

            grabfood_antapani = request.POST.get('grabfood_antapani'),
            grabfood_cisitu = request.POST.get('grabfood_cisitu'),
            grabfood_jatinangor  = request.POST.get('grabfood_jatinangor'),
            grabfood_metro = request.POST.get('grabfood_metro'),
            grabfood_sukabirus  = request.POST.get('grabfood_sukabirus'),
            grabfood_sukapura  = request.POST.get('grabfood_sukapura'),
            grabfood_sukajadi  = request.POST.get('grabfood_sukajadi'),
            grabfood_unjani = request.POST.get('grabfood_unjani'),

            survei_antapani = request.POST.get('survei_antapani'),
            survei_cisitu = request.POST.get('survei_cisitu'),
            survei_jatinangor  = request.POST.get('survei_jatinangor'),
            survei_metro = request.POST.get('survei_metro'),
            survei_sukabirus  = request.POST.get('survei_sukabirus'),
            survei_sukapura  = request.POST.get('survei_sukapura'),
            survei_sukajadi  = request.POST.get('survei_sukajadi'),
            survei_unjani = request.POST.get('survei_unjani')
        )
        kp.save()
        return redirect('kepuasan_pelanggan')

    context = {'nama' : request.user.first_name}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True
    return render(request, 'marketing/input_kepuasan_pelanggan.html', context)


@login_required(login_url='login')
def detail_kepuasan_pelanggan(request, id_kepuasan_pelanggan):
    kp = KepuasanPelanggan.objects.get(pk=id_kepuasan_pelanggan)
    context = {'nama' : request.user.first_name, 'kepuasan_pelanggan' : kp}
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'marketing/detail_kepuasan_pelanggan.html', context)

# ---------------------- SUPPLY CHAIN -------------------------------

@login_required(login_url='login')
def index_supply_chain(request):
    
    periksa_hari_dalam_pemakaian_ayam()
    update_pemakaian_ayam()
    pemakaian_ayam_weekday, pemakaian_ayam_weekend, data_awal_akhir = query_rata_rata_deman_ayam()
    context = {
        'nama' : request.user.first_name,
        'pemakaian_ayam_weekday' : pemakaian_ayam_weekday,
        'pemakaian_ayam_weekend' : pemakaian_ayam_weekend,
        'data_awal_akhir' : data_awal_akhir
        }
    
    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'supply_chain/index.html', context)

# ---------------------- OPERATION -------------------------------
@login_required(login_url='login')
def index_operation(request):
    
    context = {'nama' : request.user.first_name}

    header, isi = coba_query()
    context['header'] = header
    context['isi'] = isi

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'operation/index.html', context)

@login_required(login_url='login')
def index_rm_app(request):
    
    context = {'nama' : request.user.first_name}

    if 'tanggal' in request.GET.keys():
        hari_ini = date.fromisoformat(request.GET.get('tanggal'))
        
        if hari_ini >= date.today():
            hari_ini = date.today()
            
        querynya = query_rm_app(hari_ini)
    else:
        hari_ini = date.today()
        querynya = query_rm_app(hari_ini)

    header = ['Jam', 'Produksi Ayam (Pcs)', 'Produksi Nasi (Gram)', 'Produksi Teh Sisri (sachet)', 'Produksi Milo (Gram)', 'Produksi Orange (Gram)', 'Produksi Lemon Tea (Gram)']
    context['header'] = header
    context['tanggal'] = str(hari_ini)
    context['querynya'] = querynya    

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'operation/index_rm_app.html', context)

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

def update_dashboard(request):
    try:
        refresh_tcav()
        now = timezone.now() + timedelta(hours=7)
        tanggal_sekarang = date(now.year, now.month, now.day)
        cek_tanggal = AverageCheck.objects.filter(hari=tanggal_sekarang)

        if not cek_tanggal:
            d = AverageCheck(hari=tanggal_sekarang)
            d.tentukan_awal_akhir_hari()
            d.save()
        
        a = AverageCheck.objects.all()
        a = a.order_by('-hari')
        for i in a[:4]:
            print(i.hari)
    except:
        pass
    return redirect('index')
