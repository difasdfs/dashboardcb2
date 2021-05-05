from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from datetime import date

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

    profile = ProfilPengguna.objects.get(pengguna=User.objects.get(pk=request.user.id))
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
        a = ProduksiAyam.objects.filter(cabang = cabangnya, tanggal = hari_ini)[0]

    if request.method == "POST":
        a.id_pelapor = request.user.id
        a.waktu_lapor = timezone.now()

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

        a.jam_1_ayam = request.POST.get('angka_produksi_ayam_1') if request.POST.get('angka_produksi_ayam_1') != '' else a.jam_1_ayam
        a.jam_1_nasi = request.POST.get('angka_produksi_nasi_1') if request.POST.get('angka_produksi_nasi_1') != '' else a.jam_1_nasi
        a.jam_1_teh = request.POST.get('angka_produksi_teh_1') if request.POST.get('angka_produksi_teh_1') != '' else a.jam_1_teh
        a.jam_1_milo = request.POST.get('angka_produksi_milo_1') if request.POST.get('angka_produksi_milo_1') != '' else a.jam_1_milo
        a.jam_1_orange = request.POST.get('angka_produksi_orange_1') if request.POST.get('angka_produksi_orange_1') != '' else a.jam_1_orange
        a.jam_1_lemontea = request.POST.get('angka_produksi_lemontea_1') if request.POST.get('angka_produksi_lemontea_1') != '' else a.jam_1_lemontea

        a.jam_2_ayam = request.POST.get('angka_produksi_ayam_2') if request.POST.get('angka_produksi_ayam_2') != '' else a.jam_2_ayam
        a.jam_2_nasi = request.POST.get('angka_produksi_nasi_2') if request.POST.get('angka_produksi_nasi_2') != '' else a.jam_2_nasi
        a.jam_2_teh = request.POST.get('angka_produksi_teh_2') if request.POST.get('angka_produksi_teh_2') != '' else a.jam_2_teh
        a.jam_2_milo = request.POST.get('angka_produksi_milo_2') if request.POST.get('angka_produksi_milo_2') != '' else a.jam_2_milo
        a.jam_2_orange = request.POST.get('angka_produksi_orange_2') if request.POST.get('angka_produksi_orange_2') != '' else a.jam_2_orange
        a.jam_2_lemontea = request.POST.get('angka_produksi_lemontea_2') if request.POST.get('angka_produksi_lemontea_2') != '' else a.jam_2_lemontea

        a.jam_3_ayam = request.POST.get('angka_produksi_ayam_3') if request.POST.get('angka_produksi_ayam_3') != '' else a.jam_3_ayam
        a.jam_3_nasi = request.POST.get('angka_produksi_nasi_3') if request.POST.get('angka_produksi_nasi_3') != '' else a.jam_3_nasi
        a.jam_3_teh = request.POST.get('angka_produksi_teh_3') if request.POST.get('angka_produksi_teh_3') != '' else a.jam_3_teh
        a.jam_3_milo = request.POST.get('angka_produksi_milo_3') if request.POST.get('angka_produksi_milo_3') != '' else a.jam_3_milo
        a.jam_3_orange = request.POST.get('angka_produksi_orange_3') if request.POST.get('angka_produksi_orange_3') != '' else a.jam_3_orange
        a.jam_3_lemontea = request.POST.get('angka_produksi_lemontea_3') if request.POST.get('angka_produksi_lemontea_3') != '' else a.jam_3_lemontea

        a.stok_ayam = request.POST.get('stok_ayam') if request.POST.get('stok_ayam') != '' else a.stok_ayam
        a.stok_chicken_skin = request.POST.get('stok_chicken_skin') if request.POST.get('stok_chicken_skin') != '' else a.stok_chicken_skin
        a.save()

    hari = {
        "0" : "Senin",
        "1" : "Selasa",
        "2" : "Rabu",
        "3" : "Kamis",
        "4" : "Jumat",
        "5" : "Sabut",
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
