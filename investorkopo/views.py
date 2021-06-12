from django.shortcuts import render, redirect
from . import update_struk, update_sales, format_rupiah, kumpulan_struk
from datetime import date, timedelta
from .models import Sales
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .decorators import unauthenticated_user


# Create your views here.
def logoutuser(request):
    # ini halaman logout
    logout(request)
    return redirect('loginpage')

@unauthenticated_user
def loginpage(request):

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
            return redirect('indexcrisbarkopo')
        else:
            messages.info(request, 'username atau password salah')
            return render(request, 'investorkopo/login.html', context)

    return render(request, 'login.html', context)


@login_required(login_url='loginpage')
def index(request):
    update_struk.main()
    update_sales.main()

    tanggal_akhir = date.today()
    tanggal_awal = tanggal_akhir - timedelta(days=7)

    if request.method == 'POST':
        tanggal_akhir =  date.fromisoformat(request.POST.get('tanggal_akhir'))
        tanggal_awal = date.fromisoformat(request.POST.get('tanggal_awal'))

        if tanggal_akhir < tanggal_awal:
            tanggal_awal, tanggal_akhir = tanggal_akhir, tanggal_awal
        
        if tanggal_akhir > date.today():
            tanggal_akhir = date.today()

    kumpulan_sales = Sales.objects.filter(tanggal__range=[tanggal_awal, tanggal_akhir])
    list_sales = [a.total_sales for a in kumpulan_sales]
    
    total_sales = sum(list_sales)

    maksimum = max(list_sales)
    maksimum_grafik = maksimum*1.4
    pembagi = maksimum_grafik // 5
    urutan = [format_rupiah.main(a*pembagi) for a in range(6)]
    urutan.reverse()

    persenan = ["{:.2f}".format((b / maksimum_grafik)*100) for b in list_sales]
    list_tanggal = [a.tanggal for a in kumpulan_sales]

    query_grafik = [(persenan[a], list_tanggal[a], format_rupiah.main(list_sales[a])) for a in range(len(persenan))]

    # query kotak depan
    total_penjualan = format_rupiah.main(total_sales, total_penjualan=True)
    jumlah_struk = kumpulan_struk.main(tanggal_awal, tanggal_akhir)
    average_spend = format_rupiah.main(total_sales / jumlah_struk, total_penjualan=True)
    revenue_sharing = format_rupiah.main(total_sales*0.15, total_penjualan=True)
    # akhir query kotak depan

    # timezone asia/jakarta, untuk ngeliatin aja. kalau di sistem pakenya harus utc
    context = {
        'tanggal_awal' : str(tanggal_awal),
        'tanggal_akhir' : str(tanggal_akhir),
        'total_penjualan' : total_penjualan,
        'jumlah_struk' : jumlah_struk,
        'average_spend' : average_spend,
        'revenue_sharing' : revenue_sharing,
        'urutan_grafik' : urutan,
        'persenan' : persenan,
        'list_tanggal' : list_tanggal,
        'query_grafik' : query_grafik
    }
    
    return render(request, 'investorkopo/index.html', context)