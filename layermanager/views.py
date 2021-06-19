#from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

from .models import *
from .forms import DocumentForm

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
            return redirect('layermanager:index')
        else:
            messages.info(request, 'username atau password salah')
            return render(request, 'login.html', context)

    return render(request, 'login.html', context)

@login_required(login_url='loginpage')
def index(request):
    layer_list = Layer.objects.order_by('-nama')
    item_count = Item.objects.count()
    modifier_count = Modifier.objects.count()
    context = {'layer_list' : layer_list, 'item_count' : item_count, 'modifier_count' : modifier_count }
    return render(request, 'layermanager/index.html', context)

@login_required(login_url='loginpage')
def view_layer(request, layer_id):
    layer = get_object_or_404(Layer, pk=layer_id)
    context = {
        'layer':layer,
    }
    return render(request, 'layermanager/view_layer.html', context)

@login_required(login_url='loginpage')
def add_layer(request):
    return render(request, 'layermanager/add_layer.html')

@login_required(login_url='loginpage')
def add_layer_post(request):
    layer = Layer(nama=request.POST.get("nama"))
    layer.save()
    return redirect('layermanager:index')

@login_required(login_url='loginpage')
def update_layer(request, layer_id):
    layer = get_object_or_404(Layer, pk=layer_id)
    layer.nama = request.POST.get("nama")
    layer.save()
    return redirect('layermanager:index')

@login_required(login_url='loginpage')
def add_cabang(request, layer_id):
    layer = get_object_or_404(Layer, pk=layer_id)
    return render(request, 'layermanager/add_cabang.html', {'layer':layer})

@login_required(login_url='loginpage')
def add_cabang_post(request, layer_id):
    layer = get_object_or_404(Layer, pk=layer_id)
    layer.cabang_set.create(nama=request.POST.get("nama"))
    layer.save()
    return redirect('layermanager:index')

@login_required(login_url='loginpage')
def add_kategori(request):
    return render(request, 'layermanager/add_kategori.html')

@login_required(login_url='loginpage')
def add_kategori_post(request):
    kategori = Kategori(nama=request.POST.get("nama"))
    kategori.save()
    return redirect('layermanager:list_item')

@login_required(login_url='loginpage')
def add_item(request):
    kategori_list = Kategori.objects.order_by('-nama')
    context = {'kategori_list': kategori_list}
    return render(request, 'layermanager/add_item.html', context)

@login_required(login_url='loginpage')
def add_item_post(request):
    kategori = get_object_or_404(Kategori, pk=request.POST.get("kategori_id"))
    kategori.item_set.create(nama=request.POST.get("nama"))
    kategori.save()
    messages.add_message(request, messages.SUCCESS, 'Successfully inserted')
    return redirect('layermanager:list_item')

@login_required(login_url='loginpage')
def list_item(request):
    messages.get_messages(request)
    kategori_list = Kategori.objects.order_by('-nama')
    modifier_list = Modifier.objects.order_by('-nama')
    context = {'kategori_list': kategori_list, 'modifier_list': modifier_list}
    return render(request, 'layermanager/list_item.html', context)

@login_required(login_url='loginpage')
def add_modifier(request):
    return render(request, 'layermanager/add_modifier.html')

@login_required(login_url='loginpage')
def add_modifier_post(request):
    modifier = Modifier(nama=request.POST.get("nama"))
    modifier.save()
    return redirect('layermanager:list_item')

@login_required(login_url='loginpage')
def add_modifier_varian(request):
    modifier_list = Modifier.objects.order_by('-nama')
    context = {'modifier_list':modifier_list}
    return render(request, 'layermanager/add_modifier_varian.html', context)

@login_required(login_url='loginpage')
def add_modifier_varian_post(request):
    modifier = get_object_or_404(Modifier, pk=request.POST.get("modifier_id"))
    modifier.varian_set.create(nama=request.POST.get("nama"), harga=request.POST.get("harga"))
    modifier.save()
    return redirect('layermanager:list_item')

@login_required(login_url='loginpage')
def edit_modifier_varian(request, varian_id):
    varian = get_object_or_404(Varian, pk=varian_id)
    context = {'varian': varian}
    return render(request, 'layermanager/edit_modifier_varian.html', context)

@login_required(login_url='loginpage')
def edit_modifier_varian_post(request, varian_id):
    varian = get_object_or_404(Varian, pk=varian_id)
    varian.nama = request.POST.get("nama")
    varian.harga = int(request.POST.get("harga").replace('.',''))
    varian.save()
    return redirect('layermanager:list_item')

@login_required(login_url='loginpage')
def add_modifier_item(request):
    modifier_list = Modifier.objects.order_by('-nama')
    item_list = Item.objects.order_by('-nama')
    context = {
        'modifier_list': modifier_list,
        'item_list': item_list,
    }
    return render(request, 'layermanager/add_modifier_item.html', context)

@login_required(login_url='loginpage')
def add_modifier_item_post(request):
    item = get_object_or_404(Item, pk=request.POST.get("item_id"))
    modifier = get_object_or_404(Modifier, pk=request.POST.get("modifier_id"))
    modifier.item.add(item)
    return redirect('layermanager:list_item')

@login_required(login_url='loginpage')
def remove_modifier_item(request, item_id, modifier_id):
    item = get_object_or_404(Item, pk=item_id)
    modifier = get_object_or_404(Modifier, pk=modifier_id)
    item.modifier_set.remove(modifier)
    return redirect('layermanager:list_item')

@login_required(login_url='loginpage')
def add_harga(request, layer_id):
    layer = get_object_or_404(Layer, pk=layer_id)
    harga_list = Harga.objects.all()
    item_id = []
    for harga in harga_list:
        item_id.append(harga.item.id)
    #kategori_list = Kategori.objects.order_by('-nama')
    item_list = Item.objects.order_by('-nama').exclude(id__in=item_id)
    context = {
        'layer': layer,
        'item_list': item_list,
        #'kategori_list': kategori_list,
    }
    return render(request, 'layermanager/add_harga.html', context)

@login_required(login_url='loginpage')
def add_harga_post(request, layer_id):
    layer = get_object_or_404(Layer, pk=layer_id)
    item = get_object_or_404(Item, pk=request.POST.get("item_id"))
    harga_dinein = int(request.POST.get("harga_dinein").replace('.',''))
    harga_takeaway = int(request.POST.get("harga_takeaway").replace('.',''))
    harga_gofood = int(request.POST.get("harga_gofood").replace('.',''))
    harga_grabfood = int(request.POST.get("harga_grabfood").replace('.',''))
    harga_shopeefood = int(request.POST.get("harga_shopeefood").replace('.',''))
    try:
        harga = get_object_or_404(Harga, layer=layer, item=item)
        if (harga_dinein > 0): harga.harga_dinein = harga_dinein
        if (harga_takeaway > 0): harga.harga_takeaway = harga_takeaway
        if (harga_gofood > 0): harga.harga_gofood = harga_gofood
        if (harga_grabfood > 0): harga.harga_grabfood = harga_grabfood
        if (harga_shopeefood > 0): harga.harga_shopeefood = harga_shopeefood
        harga.save()
        #return HttpResponse("Price edited because entry already exist")
    except:
        harga = layer.harga_set.create(nama="{}-{}".format(layer.nama, item.nama),harga_dinein=harga_dinein, harga_takeaway=harga_takeaway, harga_gofood=harga_gofood, harga_grabfood=harga_grabfood, harga_shopeefood=harga_shopeefood, item=item)
        layer.save()
        item.harga_set.add(harga)
        item.save()
    return redirect('layermanager:index')

@login_required(login_url='loginpage')
def edit_harga(request, harga_id):
    harga = get_object_or_404(Harga, pk=harga_id)
    context = {
        'harga': harga,
    }
    return render(request, 'layermanager/edit_harga.html', context)
    
@login_required(login_url='loginpage')
def edit_harga_post(request, harga_id):
    harga = get_object_or_404(Harga, pk=harga_id)
    harga.harga_dinein = int(request.POST.get("harga_dinein").replace('.',''))
    harga.harga_takeaway = int(request.POST.get("harga_takeaway").replace('.',''))
    harga.harga_gofood = int(request.POST.get("harga_gofood").replace('.',''))
    harga.harga_grabfood = int(request.POST.get("harga_grabfood").replace('.',''))
    harga.harga_shopeefood = int(request.POST.get("harga_shopeefood").replace('.',''))
    harga.save()
    return redirect('layermanager:index')

@login_required(login_url='loginpage')
def uploadfile(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'layermanager/uploadfile.html', {'form':form})
    else:
        form = DocumentForm()
    return render(request, 'layermanager/uploadfile.html', {'form':form})