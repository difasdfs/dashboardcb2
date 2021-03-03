from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

import pyqrcode
import requests
import json
import time
from datetime import date

from .decorators import unauthenticated_user
from .models import Member

# Create your views here. a
@login_required(login_url='login')
def index(request):
    if request.user.groups.filter(name='IT').exists():
        return redirect('index_it')
    elif request.user.groups.filter(name='Member').exists():
        return redirect('index_member')

def halaman_login(request):
    context = {}

    if request.method == 'POST':
        uname = request.POST.get('username')
        pword = request.POST.get('password')

        user = authenticate(request, username=uname, password=pword)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username atau Password salah')
            return render(request, 'halaman_login.html', context)

    return render(request, 'halaman_login.html')

def logoutuser(request):
    logout(request)
    return redirect('login')

# MEMBER
@login_required(login_url='login')
def index_member(request):

    if not request.user.groups.filter(name='Member').exists():
        return redirect('index')

    user = User.objects.get(pk=request.user.id)
    membernya = Member.objects.filter(member=user)[0]
    
    if membernya.keaktifan == False:
        return redirect('logout')

    # MINTA DATA MEMBER KE LOYVERSE, UPDATE KE DATABASE
    # respon = requests.get('https://api.loyverse.com/v1.0/customers/' + membernya.id_loyverse, headers={'Authorization' : 'Bearer 0f0cb26bfbb048cf8251d314e2a679bc'})
    # hasil = json.loads(respon.text)

    # membernya.nama = hasil['name']
    # membernya.email = hasil['email']
    # membernya.phone_number = hasil['phone_number']
    # membernya.address = hasil['address']
    # membernya.city = hasil['city']
    # membernya.region = hasil['region']
    # membernya.postal_code = hasil['postal_code']
    # membernya.country_code = hasil['country_code']
    # membernya.customer_code = hasil['customer_code']
    # membernya.note = hasil['note']
    # membernya.first_visit = hasil['first_visit']
    # membernya.last_visit = hasil['last_visit']
    # membernya.total_visit = hasil['total_visits']
    # membernya.total_spent = hasil['total_spent']
    # membernya.total_points = hasil['total_points']
    # membernya.created_at = hasil['created_at']
    # membernya.updated_at = hasil['updated_at']
    # membernya.deleted_at = hasil['deleted_at']
    # membernya.save()

    # print(hasil)

    context = {'title' : 'Index', 'home' : True, 'detail_member' : membernya}
    return render(request, 'member/index.html', context)

def ubah_akun_member(request):

    if not request.user.groups.filter(name='Member').exists():
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(pk=request.user.id)
        membernya = Member.objects.filter(member=user)[0]

        user.username = username
        user.set_password(password)
        user.save()

        membernya.username = username
        membernya.password = password
        membernya.save()
        return redirect('index')

    context = {'title' : 'Profile', 'ubah_akun_member' : True}
    return render(request, 'member/ubah_akun_member.html', context)

# DEPARTEMEN IT
@login_required(login_url='login')
def index_it(request):

    # logika update data

    membernya = Member.objects.filter(keaktifan=True)
    context = {'home' : 'class="active"', 'title' : 'Index IT', 'akun' : membernya}

    if not request.user.groups.filter(name='IT').exists():
        return redirect('index')

    return render(request, 'IT/index.html', context)

@login_required(login_url='login')
def akun_member(request):

    if not request.user.groups.filter(name='IT').exists():
        return redirect('index')

    # update_loyverse()
    membernya = Member.objects.all()

    context = {'member' : 'class="active"', 'title' : 'Akun Member', 'akun' : membernya}
    return render(request, 'IT/akun_member.html', context)

@login_required(login_url='login')
def akun_backoffice(request):

    if not request.user.groups.filter(name='IT').exists():
        return redirect('index')

    backoffice = User.objects.filter(groups__name='Backoffice')

    context = {'backoffice' : 'class="active"', 'title' : 'Akun Backoffice', 'akun' : backoffice}
    return render(request, 'IT/akun_backoffice.html', context)

@login_required(login_url='login')
def buat_akun_backoffice(request):

    if not request.user.groups.filter(name='IT').exists():
        return redirect('index')

    if request.method == 'POST':
        nama = request.POST.get('nama')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.create_user(username, '', password)
        user.first_name = nama
        user.save()

        grup_user = Group.objects.get(name='Backoffice')
        grup_user.user_set.add(user)
        return redirect('akun_backoffice')


    context = {'backoffice' : 'class="active"', 'title' : 'Buat Akun Backoffice'}
    return render(request, 'IT/buat_akun_backoffice.html', context)

@login_required(login_url='login')
def buat_akun_member(request):

    if not request.user.groups.filter(name='IT').exists():
        return redirect('index')

    if request.method == 'POST':
        uname = request.POST.get('username')
        pswrd = request.POST.get('password')
        kode_pelanggan = request.POST.get('kode_pelanggan')

        user = User.objects.create_user(uname, '', pswrd)
        user.save()

        membernya = Member(
            member = User.objects.get(pk=user.id),
            username = uname,
            password = pswrd,
            customer_code = kode_pelanggan,
            keaktifan = False
        )
        membernya.save()

        nomor_qr_code = kode_pelanggan
        qrcode = pyqrcode.create(nomor_qr_code)
        qrcode.png('qrcode/' + str(nomor_qr_code) + '.png', scale=8)
        membernya.link_qrcode = 'qrcode/' + str(nomor_qr_code) + '.png'
        membernya.save()

        grup_user = Group.objects.get(name='Member')
        grup_user.user_set.add(user)

        return redirect('akun_member')

    context = {'member' : 'class="active"', 'title' : 'Buat Akun Member'}
    return render(request, 'IT/buat_akun_member.html', context)


@login_required(login_url='login')
def detail_akun_member(request, id_member):

    if not request.user.groups.filter(name='IT').exists():
        return redirect('index')

    membernya = Member.objects.get(pk=id_member)

    context = {'member' : 'class="active"', 'title' : 'Detail Akun Member', 'detail_member' : membernya}
    return render(request, 'IT/detail_akun_member.html', context)

# LOGIKA
def update_loyverse():
    # baca query akun member yang belum aktif, masukkin ke list (member_nonaktif)
    member_nonaktif = Member.objects.filter(keaktifan = False)
    kode_pelanggan = [isi.customer_code for isi in member_nonaktif]

    # baca akun member yang dibuat sejal awal hari ini
    baseUrl = 'https://api.loyverse.com/v1.0/customers'
    access_token = '0f0cb26bfbb048cf8251d314e2a679bc'
    header = {'Authorization' : 'Bearer ' + access_token }
    hariini = date.today()
    awal_hari = hariini.strftime('%Y-%m-%d') + 'T00:00:00.000Z'
    payload = {'created_at_min': awal_hari, 'limit' : 250}
    respon = requests.get('https://api.loyverse.com/v1.0/customers', headers=header, params=payload)
    hasil = json.loads(respon.text)

    # inisiasi variabel akun_akan_aktif a
    # DATA PELANGGAN yang ingin diaktifkan dikumpulkan disini
    # iterasi DATA member dari loyverse, jika customer code ada di kode_pelanggan, append ke DATA akun_akan_aktif
    akun_akan_aktif = [isi for isi in hasil['customers'] if isi['customer_code'] in kode_pelanggan]

    # aktifkan akun member yang ada di akun_akan_aktif
    for kode_p in akun_akan_aktif:
        objek_member = Member.objects.filter(customer_code = kode_p['customer_code'])
        objek_member = objek_member[0]
        objek_member.id_loyverse = kode_p['id']
        objek_member.nama = kode_p['name']
        objek_member.email = kode_p['email']
        objek_member.phone_number = kode_p['phone_number']
        objek_member.address = kode_p['address']
        objek_member.city = kode_p['city']
        objek_member.region = kode_p['region']
        objek_member.postal_code = kode_p['postal_code']
        objek_member.country_code = kode_p['country_code']
        objek_member.note = kode_p['note']
        objek_member.first_visit = kode_p['first_visit']
        objek_member.last_visit = kode_p['last_visit']
        objek_member.total_visit = str(kode_p['total_visits'])
        objek_member.total_spent = str(kode_p['total_spent'])
        objek_member.total_points = str(kode_p['total_points'])
        objek_member.created_at = kode_p['created_at']
        objek_member.updated_at = kode_p['updated_at']
        objek_member.deleted_at = kode_p['deleted_at']
        objek_member.keaktifan = True
        objek_member.save()


# def update_data_aktif()
