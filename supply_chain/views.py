from django.shortcuts import render
from dashboard.models import AssemblyProduct
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required

from .models import KategoriLoyverse
from . import logika_api, logika_api_item

# Create your views here.
@login_required(login_url='login')
def data_sold(request):

    context = {'nama' : request.user.first_name}

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'supply_chain/data_sold.html')


@login_required(login_url='login')
def sku(request):

    context = {'nama' : request.user.first_name}

    data = AssemblyProduct.objects.all()
    banyak_data_per_page = 10
    p = Paginator(data, banyak_data_per_page)
    page_num = request.GET.get('page', 1)

    try:
	    page = p.page(page_num)
    except EmptyPage:
	    page = p.page(1)

    banyak_halaman = [str(a+1) for a in range(p.num_pages)]
    context['banyak_halaman'] = banyak_halaman
    context['jumlah_halaman'] = len(banyak_halaman)
    context['halaman_aktif'] = str(page_num)
    context['data'] = page
    context['info_pagination'] = {
        'has_previous' : page.has_previous(),
        'has_next' : page.has_next()
    }
    if page.has_previous():
        context['info_pagination']['halaman_sebelumnya'] = page.previous_page_number()
    
    if page.has_next():
        context['info_pagination']['halaman_selanjutnya'] = page.next_page_number()

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'supply_chain/sku.html', context)


@login_required(login_url='login')
def update_sku(request):

    context = {'nama' : request.user.first_name}

    sku_ga_ada = logika_api_item.main()
    context['sku_tidak_ada'] = sku_ga_ada

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'supply_chain/update_sku.html', context)


@login_required(login_url='login')
def kategori(request):

    context = {'nama' : request.user.first_name}

    logika_api.main()

    data = KategoriLoyverse.objects.all()
    data = data.order_by('nama_kategori')
    context['data'] = data

    if not request.user.groups.filter(name='Eksekutif').exists() or request.user.last_name == 'Human Resource':
        context['data_kar'] = True

    return render(request, 'supply_chain/kategori.html', context)
