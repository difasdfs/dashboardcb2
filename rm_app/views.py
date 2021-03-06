from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from datetime import date
from django.core.paginator import Paginator, EmptyPage

from rm_app.logika.isrm import is_rm
from rm_app.logika.ngecek_hari import cek_hari
from .models import *

from .decorators import unauthenticated_user

# Create your views here.
def hello_world(request):
    # test.print_test()
    return render(request, 'rm_app/hello_world.html')


@unauthenticated_user
def login_page(request):

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
            return redirect('index_rm')
        else:
            messages.info(request, 'username atau password salah')
            return render(request, 'rm_app/login_page.html', context)

    return render(request, 'rm_app/login_page.html', context)

def logoutuser(request):
    # ini halaman logout
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
def index_rm(request):
    is_rm(request.user)

    try:
        profile = ProfilPengguna.objects.get(pengguna=User.objects.get(pk=request.user.id))
    except:
        messages.info(request, 'Gunakan akun RM untuk login')
        return redirect('logoutuser')

    cabangnya = profile.cabang

    hari_ini = date.today()

    if 'tanggal' in request.GET.keys():
        hari_ini = date.fromisoformat(request.GET.get('tanggal'))

        if hari_ini >= date.today():
            hari_ini = date.today()
            a = ProduksiAyam.objects.filter(cabang = cabangnya, tanggal = hari_ini)[0]
        else:
            cek_hari(request.user.id, hari_ini, cabangnya)
            a = ProduksiAyam.objects.filter(cabang = cabangnya, tanggal = hari_ini)[0]

    else:
        cek_hari(request.user.id, hari_ini, cabangnya)
        a = ProduksiAyam.objects.filter(cabang = cabangnya, tanggal = hari_ini)[0]

    if request.method == "POST":
        a.id_pelapor = request.user.id
        a.waktu_lapor = timezone.now()

        a.jam_9_ayam = request.POST.get('angka_produksi_ayam_9') if request.POST.get('angka_produksi_ayam_9') != '' else a.jam_11_ayam
        a.jam_9_nasi = request.POST.get('angka_produksi_nasi_9') if request.POST.get('angka_produksi_nasi_9') != '' else a.jam_11_nasi
        a.jam_9_teh = request.POST.get('angka_produksi_teh_9') if request.POST.get('angka_produksi_teh_9') != '' else a.jam_11_teh
        a.jam_9_milo = request.POST.get('angka_produksi_milo_9') if request.POST.get('angka_produksi_milo_9') != '' else a.jam_11_milo
        a.jam_9_orange = request.POST.get('angka_produksi_orange_9') if request.POST.get('angka_produksi_orange_9') != '' else a.jam_11_orange
        a.jam_9_lemontea = request.POST.get('angka_produksi_lemontea_9') if request.POST.get('angka_produksi_lemontea_9') != '' else a.jam_11_lemontea

        a.jam_10_ayam = request.POST.get('angka_produksi_ayam_10') if request.POST.get('angka_produksi_ayam_10') != '' else a.jam_11_ayam
        a.jam_10_nasi = request.POST.get('angka_produksi_nasi_10') if request.POST.get('angka_produksi_nasi_10') != '' else a.jam_11_nasi
        a.jam_10_teh = request.POST.get('angka_produksi_teh_10') if request.POST.get('angka_produksi_teh_10') != '' else a.jam_11_teh
        a.jam_10_milo = request.POST.get('angka_produksi_milo_10') if request.POST.get('angka_produksi_milo_10') != '' else a.jam_11_milo
        a.jam_10_orange = request.POST.get('angka_produksi_orange_10') if request.POST.get('angka_produksi_orange_10') != '' else a.jam_11_orange
        a.jam_10_lemontea = request.POST.get('angka_produksi_lemontea_10') if request.POST.get('angka_produksi_lemontea_10') != '' else a.jam_11_lemontea

        a.jam_11_ayam = request.POST.get('angka_produksi_ayam_11') if request.POST.get('angka_produksi_ayam_11') != '' else a.jam_11_ayam
        a.jam_11_nasi = request.POST.get('angka_produksi_nasi_11') if request.POST.get('angka_produksi_nasi_11') != '' else a.jam_11_nasi
        a.jam_11_teh = request.POST.get('angka_produksi_teh_11') if request.POST.get('angka_produksi_teh_11') != '' else a.jam_11_teh
        a.jam_11_milo = request.POST.get('angka_produksi_milo_11') if request.POST.get('angka_produksi_milo_11') != '' else a.jam_11_milo
        a.jam_11_orange = request.POST.get('angka_produksi_orange_11') if request.POST.get('angka_produksi_orange_11') != '' else a.jam_11_orange
        a.jam_11_lemontea = request.POST.get('angka_produksi_lemontea_11') if request.POST.get('angka_produksi_lemontea_11') != '' else a.jam_11_lemontea

        a.jam_12_ayam = request.POST.get('angka_produksi_ayam_12') if request.POST.get('angka_produksi_ayam_12') != '' else a.jam_12_ayam
        a.jam_12_nasi = request.POST.get('angka_produksi_nasi_12') if request.POST.get('angka_produksi_nasi_12') != '' else a.jam_12_nasi
        a.jam_12_teh = request.POST.get('angka_produksi_teh_12') if request.POST.get('angka_produksi_teh_12') != '' else a.jam_12_teh
        a.jam_12_milo = request.POST.get('angka_produksi_milo_12') if request.POST.get('angka_produksi_milo_12') != '' else a.jam_12_milo
        a.jam_12_orange = request.POST.get('angka_produksi_orange_12') if request.POST.get('angka_produksi_orange_12') != '' else a.jam_12_orange
        a.jam_12_lemontea = request.POST.get('angka_produksi_lemontea_12') if request.POST.get('angka_produksi_lemontea_12') != '' else a.jam_12_lemontea

        a.jam_13_ayam = request.POST.get('angka_produksi_ayam_13') if request.POST.get('angka_produksi_ayam_13') != '' else a.jam_13_ayam
        a.jam_13_nasi = request.POST.get('angka_produksi_nasi_13') if request.POST.get('angka_produksi_nasi_13') != '' else a.jam_13_nasi
        a.jam_13_teh = request.POST.get('angka_produksi_teh_13') if request.POST.get('angka_produksi_teh_13') != '' else a.jam_13_teh
        a.jam_13_milo = request.POST.get('angka_produksi_milo_13') if request.POST.get('angka_produksi_milo_13') != '' else a.jam_13_milo
        a.jam_13_orange = request.POST.get('angka_produksi_orange_13') if request.POST.get('angka_produksi_orange_13') != '' else a.jam_13_orange
        a.jam_13_lemontea = request.POST.get('angka_produksi_lemontea_13') if request.POST.get('angka_produksi_lemontea_13') != '' else a.jam_13_lemontea

        a.jam_14_ayam = request.POST.get('angka_produksi_ayam_14') if request.POST.get('angka_produksi_ayam_14') != '' else a.jam_14_ayam
        a.jam_14_nasi = request.POST.get('angka_produksi_nasi_14') if request.POST.get('angka_produksi_nasi_14') != '' else a.jam_14_nasi
        a.jam_14_teh = request.POST.get('angka_produksi_teh_14') if request.POST.get('angka_produksi_teh_14') != '' else a.jam_14_teh
        a.jam_14_milo = request.POST.get('angka_produksi_milo_14') if request.POST.get('angka_produksi_milo_14') != '' else a.jam_14_milo
        a.jam_14_orange = request.POST.get('angka_produksi_orange_14') if request.POST.get('angka_produksi_orange_14') != '' else a.jam_14_orange
        a.jam_14_lemontea = request.POST.get('angka_produksi_lemontea_14') if request.POST.get('angka_produksi_lemontea_14') != '' else a.jam_14_lemontea

        a.jam_15_ayam = request.POST.get('angka_produksi_ayam_15') if request.POST.get('angka_produksi_ayam_15') != '' else a.jam_15_ayam
        a.jam_15_nasi = request.POST.get('angka_produksi_nasi_15') if request.POST.get('angka_produksi_nasi_15') != '' else a.jam_15_nasi
        a.jam_15_teh = request.POST.get('angka_produksi_teh_15') if request.POST.get('angka_produksi_teh_15') != '' else a.jam_15_teh
        a.jam_15_milo = request.POST.get('angka_produksi_milo_15') if request.POST.get('angka_produksi_milo_15') != '' else a.jam_15_milo
        a.jam_15_orange = request.POST.get('angka_produksi_orange_15') if request.POST.get('angka_produksi_orange_15') != '' else a.jam_15_orange
        a.jam_15_lemontea = request.POST.get('angka_produksi_lemontea_15') if request.POST.get('angka_produksi_lemontea_15') != '' else a.jam_15_lemontea

        a.jam_16_ayam = request.POST.get('angka_produksi_ayam_16') if request.POST.get('angka_produksi_ayam_16') != '' else a.jam_16_ayam
        a.jam_16_nasi = request.POST.get('angka_produksi_nasi_16') if request.POST.get('angka_produksi_nasi_16') != '' else a.jam_16_nasi
        a.jam_16_teh = request.POST.get('angka_produksi_teh_16') if request.POST.get('angka_produksi_teh_16') != '' else a.jam_16_teh
        a.jam_16_milo = request.POST.get('angka_produksi_milo_16') if request.POST.get('angka_produksi_milo_16') != '' else a.jam_16_milo
        a.jam_16_orange = request.POST.get('angka_produksi_orange_16') if request.POST.get('angka_produksi_orange_16') != '' else a.jam_16_orange
        a.jam_16_lemontea = request.POST.get('angka_produksi_lemontea_16') if request.POST.get('angka_produksi_lemontea_16') != '' else a.jam_16_lemontea

        a.jam_17_ayam = request.POST.get('angka_produksi_ayam_17') if request.POST.get('angka_produksi_ayam_17') != '' else a.jam_17_ayam
        a.jam_17_nasi = request.POST.get('angka_produksi_nasi_17') if request.POST.get('angka_produksi_nasi_17') != '' else a.jam_17_nasi
        a.jam_17_teh = request.POST.get('angka_produksi_teh_17') if request.POST.get('angka_produksi_teh_17') != '' else a.jam_17_teh
        a.jam_17_milo = request.POST.get('angka_produksi_milo_17') if request.POST.get('angka_produksi_milo_17') != '' else a.jam_17_milo
        a.jam_17_orange = request.POST.get('angka_produksi_orange_17') if request.POST.get('angka_produksi_orange_17') != '' else a.jam_17_orange
        a.jam_17_lemontea = request.POST.get('angka_produksi_lemontea_17') if request.POST.get('angka_produksi_lemontea_17') != '' else a.jam_17_lemontea

        a.jam_18_ayam = request.POST.get('angka_produksi_ayam_18') if request.POST.get('angka_produksi_ayam_18') != '' else a.jam_18_ayam
        a.jam_18_nasi = request.POST.get('angka_produksi_nasi_18') if request.POST.get('angka_produksi_nasi_18') != '' else a.jam_18_nasi
        a.jam_18_teh = request.POST.get('angka_produksi_teh_18') if request.POST.get('angka_produksi_teh_18') != '' else a.jam_18_teh
        a.jam_18_milo = request.POST.get('angka_produksi_milo_18') if request.POST.get('angka_produksi_milo_18') != '' else a.jam_18_milo
        a.jam_18_orange = request.POST.get('angka_produksi_orange_18') if request.POST.get('angka_produksi_orange_18') != '' else a.jam_18_orange
        a.jam_18_lemontea = request.POST.get('angka_produksi_lemontea_18') if request.POST.get('angka_produksi_lemontea_18') != '' else a.jam_18_lemontea

        a.jam_19_ayam = request.POST.get('angka_produksi_ayam_19') if request.POST.get('angka_produksi_ayam_19') != '' else a.jam_19_ayam
        a.jam_19_nasi = request.POST.get('angka_produksi_nasi_19') if request.POST.get('angka_produksi_nasi_19') != '' else a.jam_19_nasi
        a.jam_19_teh = request.POST.get('angka_produksi_teh_19') if request.POST.get('angka_produksi_teh_19') != '' else a.jam_19_teh
        a.jam_19_milo = request.POST.get('angka_produksi_milo_19') if request.POST.get('angka_produksi_milo_19') != '' else a.jam_19_milo
        a.jam_19_orange = request.POST.get('angka_produksi_orange_19') if request.POST.get('angka_produksi_orange_19') != '' else a.jam_19_orange
        a.jam_19_lemontea = request.POST.get('angka_produksi_lemontea_19') if request.POST.get('angka_produksi_lemontea_19') != '' else a.jam_19_lemontea

        a.jam_20_ayam = request.POST.get('angka_produksi_ayam_20') if request.POST.get('angka_produksi_ayam_20') != '' else a.jam_20_ayam
        a.jam_20_nasi = request.POST.get('angka_produksi_nasi_20') if request.POST.get('angka_produksi_nasi_20') != '' else a.jam_20_nasi
        a.jam_20_teh = request.POST.get('angka_produksi_teh_20') if request.POST.get('angka_produksi_teh_20') != '' else a.jam_20_teh
        a.jam_20_milo = request.POST.get('angka_produksi_milo_20') if request.POST.get('angka_produksi_milo_20') != '' else a.jam_20_milo
        a.jam_20_orange = request.POST.get('angka_produksi_orange_20') if request.POST.get('angka_produksi_orange_20') != '' else a.jam_20_orange
        a.jam_20_lemontea = request.POST.get('angka_produksi_lemontea_20') if request.POST.get('angka_produksi_lemontea_20') != '' else a.jam_20_lemontea

        a.jam_21_ayam = request.POST.get('angka_produksi_ayam_21') if request.POST.get('angka_produksi_ayam_21') != '' else a.jam_21_ayam
        a.jam_21_nasi = request.POST.get('angka_produksi_nasi_21') if request.POST.get('angka_produksi_nasi_21') != '' else a.jam_21_nasi
        a.jam_21_teh = request.POST.get('angka_produksi_teh_21') if request.POST.get('angka_produksi_teh_21') != '' else a.jam_21_teh
        a.jam_21_milo = request.POST.get('angka_produksi_milo_21') if request.POST.get('angka_produksi_milo_21') != '' else a.jam_21_milo
        a.jam_21_orange = request.POST.get('angka_produksi_orange_21') if request.POST.get('angka_produksi_orange_21') != '' else a.jam_21_orange
        a.jam_21_lemontea = request.POST.get('angka_produksi_lemontea_21') if request.POST.get('angka_produksi_lemontea_21') != '' else a.jam_21_lemontea

        a.jam_22_ayam = request.POST.get('angka_produksi_ayam_22') if request.POST.get('angka_produksi_ayam_22') != '' else a.jam_22_ayam
        a.jam_22_nasi = request.POST.get('angka_produksi_nasi_22') if request.POST.get('angka_produksi_nasi_22') != '' else a.jam_22_nasi
        a.jam_22_teh = request.POST.get('angka_produksi_teh_22') if request.POST.get('angka_produksi_teh_22') != '' else a.jam_22_teh
        a.jam_22_milo = request.POST.get('angka_produksi_milo_22') if request.POST.get('angka_produksi_milo_22') != '' else a.jam_22_milo
        a.jam_22_orange = request.POST.get('angka_produksi_orange_22') if request.POST.get('angka_produksi_orange_22') != '' else a.jam_22_orange
        a.jam_22_lemontea = request.POST.get('angka_produksi_lemontea_22') if request.POST.get('angka_produksi_lemontea_22') != '' else a.jam_22_lemontea

        a.jam_23_ayam = request.POST.get('angka_produksi_ayam_23') if request.POST.get('angka_produksi_ayam_23') != '' else a.jam_23_ayam
        a.jam_23_nasi = request.POST.get('angka_produksi_nasi_23') if request.POST.get('angka_produksi_nasi_23') != '' else a.jam_23_nasi
        a.jam_23_teh = request.POST.get('angka_produksi_teh_23') if request.POST.get('angka_produksi_teh_23') != '' else a.jam_23_teh
        a.jam_23_milo = request.POST.get('angka_produksi_milo_23') if request.POST.get('angka_produksi_milo_23') != '' else a.jam_23_milo
        a.jam_23_orange = request.POST.get('angka_produksi_orange_23') if request.POST.get('angka_produksi_orange_23') != '' else a.jam_23_orange
        a.jam_23_lemontea = request.POST.get('angka_produksi_lemontea_23') if request.POST.get('angka_produksi_lemontea_23') != '' else a.jam_23_lemontea

        a.jam_24_ayam = request.POST.get('angka_produksi_ayam_24') if request.POST.get('angka_produksi_ayam_24') != '' else a.jam_24_ayam
        a.jam_24_nasi = request.POST.get('angka_produksi_nasi_24') if request.POST.get('angka_produksi_nasi_24') != '' else a.jam_24_nasi
        a.jam_24_teh = request.POST.get('angka_produksi_teh_24') if request.POST.get('angka_produksi_teh_24') != '' else a.jam_24_teh
        a.jam_24_milo = request.POST.get('angka_produksi_milo_24') if request.POST.get('angka_produksi_milo_24') != '' else a.jam_24_milo
        a.jam_24_orange = request.POST.get('angka_produksi_orange_24') if request.POST.get('angka_produksi_orange_24') != '' else a.jam_24_orange
        a.jam_24_lemontea = request.POST.get('angka_produksi_lemontea_24') if request.POST.get('angka_produksi_lemontea_24') != '' else a.jam_24_lemontea

        a.jam_1_ayam = 0
        a.jam_1_nasi = 0
        a.jam_1_teh = 0
        a.jam_1_milo = 0
        a.jam_1_orange = 0
        a.jam_1_lemontea = 0

        a.jam_2_ayam = 0
        a.jam_2_nasi = 0
        a.jam_2_teh = 0
        a.jam_2_milo = 0
        a.jam_2_orange = 0
        a.jam_2_lemontea = 0

        a.jam_3_ayam = 0
        a.jam_3_nasi = 0
        a.jam_3_teh = 0
        a.jam_3_milo = 0
        a.jam_3_orange = 0
        a.jam_3_lemontea = 0

        a.stok_ayam = request.POST.get('stok_ayam') if request.POST.get('stok_ayam') != '' else a.stok_ayam
        a.stok_chicken_skin = request.POST.get('stok_chicken_skin') if request.POST.get('stok_chicken_skin') != '' else a.stok_chicken_skin
        a.save()

    hari = {
        "0" : "Senin",
        "1" : "Selasa",
        "2" : "Rabu",
        "3" : "Kamis",
        "4" : "Jumat",
        "5" : "Sabtu",
        "6" : "Minggu"
    }

    nama_hari = hari[str(hari_ini.weekday()) ]

    context = {
        'query_data' : a,
        'nama_hari' : nama_hari,
        'hari_ini' : str(hari_ini),
        'nama_cabang' : cabangnya.nama_cabang
    }

    return render(request, 'rm_app/index.html', context)

@login_required(login_url='login_page')
def ubah_akun(request):

    if request.method == "POST":
        u = User.objects.get(pk=request.user.id)

        p = ProfilPengguna.objects.get(pengguna=u)

        u.first_name = request.POST.get('nama')

        u.username = request.POST.get('username')
        p.username = request.POST.get('username')

        u.set_password(request.POST.get('password'))
        p.password = request.POST.get('password')

        u.save()
        p.save()
        return redirect('index_rm')

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)
    context = {
        'profile' : profile
    }

    return render(request, 'rm_app/ubah_akun.html', context)

from dashboard.models import DataKaryawan
@login_required(login_url='login_page')
def absen(request):

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)

    if request.method == "POST":
        kunci = request.POST.keys()
        tanggalnya = date.fromisoformat(request.POST.get("tanggal"))
        cabangnya = profile.cabang.nama_cabang

        at = AbsenTanggal(
            tanggal = tanggalnya,
            cabang = cabangnya
        )
        at.save()

        for k in kunci:
            if "idkaryawan" in k:
                absennya = request.POST.get(k)
                k = k.split('-')
                iddatakaryawan = int(k[1])
                karyawan = DataKaryawan.objects.get(pk=iddatakaryawan)

                absensi = AbsenKaryawan(
                    nik = karyawan.nik,
                    tanggal = at,
                    absen = absennya
                )
                absensi.save()

    cabangnya = profile.cabang.nama_cabang
    absen_tanggal = AbsenTanggal.objects.filter(cabang=cabangnya).order_by("-tanggal")
    # Hadir, Sakit, Libur, Cuti, Izin, Alpha, WFH

    # list of dictionary [(tanggal, jumlah hadir, sakit, libur, cuti, izin, alpha, wfh)]
    query_absen_tanggal = []
    for at in absen_tanggal:
        jumlah_hadir = 0
        jumlah_sakit = 0
        jumlah_libur = 0
        jumlah_cuti = 0
        jumlah_izin = 0
        jumlah_alpha = 0
        jumlah_wfh = 0
        absen_karyawan = AbsenKaryawan.objects.filter(tanggal=at)
        nik_nama_absen = []
        for ak in absen_karyawan:
            kar = DataKaryawan.objects.get(nik=ak.nik)
            nik_nama_absen.append( (ak.nik, kar.nama, ak.absen) )
            if "Hadir" in ak.absen:
                jumlah_hadir += 1
            elif "Sakit" in ak.absen:
                jumlah_sakit += 1
            elif "Libur" in ak.absen:
                jumlah_libur += 1
            elif "Cuti" in ak.absen:
                jumlah_cuti += 1
            elif "Izin" in ak.absen:
                jumlah_izin += 1
            elif "Alpha" in ak.absen:
                jumlah_alpha += 1
            elif "WHF" in ak.absen:
                jumlah_wfh += 1
        query_absen_tanggal.append({
                "tanggal" : at.tanggal.strftime("%d %B %Y"), 
                "jumlah_hadir" : jumlah_hadir,
                "jumlah_sakit" : jumlah_sakit,
                "jumlah_libur" : jumlah_libur,
                "jumlah_cuti" : jumlah_cuti,
                "jumlah_izin" : jumlah_izin,
                "jumlah_alpha" : jumlah_alpha,
                "jumlah_wfh" : jumlah_wfh,
                "nik_nama_absen" : nik_nama_absen
        })
    print(query_absen_tanggal)
    
    karyawan = DataKaryawan.objects.filter(area=cabangnya, status="AKTIF")

    # querynya nama dan id object kelas DataKaryawan untuk modals
    query_karyawan = [(a.nama, str(a.id), a.nik) for a in karyawan]
    
    banyak_data_per_page = 10
    p = Paginator(query_absen_tanggal, banyak_data_per_page)
    page_num = request.GET.get('page', 1)

    try:
	    page = p.page(page_num)
    except EmptyPage:
	    page = p.page(1)

    banyak_halaman = [str(a+1) for a in range(p.num_pages)]

    context = {
        'profile' : profile,
        'data_karyawan_cabang' : query_karyawan,
        'query_absen_tanggal' : page,
        'hari_ini' : str(date.today()),
        'banyak_halaman' : banyak_halaman,
        'halaman_aktif' : str(page_num)
    }

    return render(request, 'rm_app/absen.html', context)

@login_required(login_url='login_page')
def shift(request):

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)

    context = {
        'profile' : profile,
    }

    return render(request, 'rm_app/shift.html', context)

@login_required(login_url='login_page')
def jadwal_kerja_rencana(request):

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)

    context = {
        'profile' : profile,
    }

    return render(request, 'rm_app/jadwal_kerja_rencana.html', context)

@login_required(login_url='login_page')
def statistik_jadwal_kerja(request):

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)

    context = {
        'profile' : profile,
    }

    return render(request, 'rm_app/statistik_jadwal_kerja.html', context)

@login_required(login_url='login_page')
def varian_shift(request):

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)

    if request.method == "POST":
        so = ShiftOperasional(
            cabang = profile.cabang,
            kode = request.POST.get('kode_shift'),
            deskripsi = request.POST.get('deskripsi_shift'),
            warna  = request.POST.get('warna')
        )
        so.save()
        
    shift_operasional = ShiftOperasional.objects.filter(cabang=profile.cabang)

    context = {
        'profile' : profile,
        'shift_operasional' : shift_operasional
    }

    return render(request, 'rm_app/varian_shift.html', context)