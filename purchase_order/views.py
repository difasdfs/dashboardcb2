from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from rm_app.models import ProfilPengguna

from .models import PurchaseOrder, BarangPurchaseOrder, StatusPurchaseOrder, BarangDiterima

from supply_chain import logika_update_struk
from .logika import logika_po_gunung_mas, orderan

from datetime import date, timedelta
import math
import imgkit

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# ----------------------- LOGIKA -----------------------
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None
# ----------------------- LOGIKA -----------------------

# Create your views here.
@login_required(login_url='login_page')
def purchase_order(request):

    logika_update_struk.main()

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)
    context = {
        'profile' : profile
    }

    return render(request, 'rm_app/purchase_order/purchase_order.html', context)

@login_required(login_url='login_page')
def gunung_mas(request):

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)

    tanggal_po = date.today()

    if request.method == "POST":
        variabel_skip = "csrfmiddlewaretoken"
        
        diisi2 = [nama_kunci for nama_kunci in request.POST.keys() if (request.POST.get(nama_kunci) != "") and (nama_kunci != variabel_skip)]
        
        on_hand = {}

        for nama_kunci in diisi2:
            on_hand[nama_kunci] = float(request.POST.get(nama_kunci))

        konversi = {
            'kertas_roll_printer' : 0.5,
            'kertas_nasi_puas' : 0.0666,
            'packaging_combo' : 0.5,
            'packaging_ala_carte' : 0.333333,
            'packaging_paper_tray_dine_in' : 0.333333,
            'packaging_paper_bag_cokelat' : 0.333333,
            'paper_bowl_crisbee_5oz' : 1,
            'tutup_lid_paper_bowl_5oz' : 1,
            'dus_silky_pudding' : 0.0416666,
            'dus_perkedelku' : 0.008333333,
            'dus_sambal_sachet' : 0.5
        }

        for kunci in on_hand.keys():
            try:
                on_hand[kunci] = on_hand[kunci] * konversi[kunci]
            except:
                continue

        nomor_po_bener = {
            "Crisbar Unjani" : "UN" + tanggal_po.strftime("%d%m%y"),
            "Crisbar Cisitu" : "CT" + tanggal_po.strftime("%d%m%y"),
            "Crisbar Sukajadi" : "BT" + tanggal_po.strftime("%d%m%y"),
            "Crisbar Kopo" : "UN" + tanggal_po.strftime("%d%m%y"),
            "Crisbar Sukapura" : "SP" + tanggal_po.strftime("%d%m%y"),
            "Crisbar Sukabirus" : "SB" + tanggal_po.strftime("%d%m%y"),
            "Crisbar Antapani" : "AP" + tanggal_po.strftime("%d%m%y"),
            "Crisbar Jatinangor" : "JT" + tanggal_po.strftime("%d%m%y"),
            "Crisbar Metro Margahayu" : "UN" + tanggal_po.strftime("%d%m%y"),
        }

        total_po = logika_po_gunung_mas.main(on_hand, profile.cabang.nama_cabang)
        data_po = {
            "nama_pic" : profile.nama,
            "nomor_pic" : profile.nomor_hp,
            "alamat" : profile.alamat,
            "supplier" : "Gunung Mas",
            "tanggal_po" : tanggal_po.strftime("%d %b %Y"),
            "item_po" : total_po
        }
        po = PurchaseOrder(
            nomor_po = nomor_po_bener[profile.cabang.nama_cabang] + "GM",
            profil_pengguna = profile,
            nama_pic = data_po['nama_pic'],
            nomor_pic = data_po['nomor_pic'],
            alamat = data_po['alamat'],
            tanggal_po = tanggal_po
        )
        po.save()
        akhir_no_po = "000" + str(po.id)
        po.nomor_po = po.nomor_po + akhir_no_po[-3:]
        po.save()

        spo = StatusPurchaseOrder(
            purchase_order = po,
            status = "Belum Diterima"
        )
        spo.save()

        for kunci in total_po.keys():
            bpo = BarangPurchaseOrder(
                purchase_order = po,
                nama_item = total_po[kunci]['nama_item'],
                jumlah_order = total_po[kunci]['total_po'],
                satuan = total_po[kunci]['satuan']
            )
            bpo.save()
        return redirect('konfirmasi_order', po.id)

        # format PO : cabang, tanggal, nomor urut
    
    context = {
        'profile' : profile
    }

    return render(request, 'rm_app/purchase_order/supplier/gunung_mas.html', context)


@login_required(login_url='login_page')
def form_po_cabang(request, id_po):

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)
    po = PurchaseOrder.objects.get(pk=id_po)
    barang = BarangPurchaseOrder.objects.filter(purchase_order=po)
    tanggal_kirim = po.tanggal_po + timedelta(days=1)

    item_dc = ['Dus Kertas Roll Printer','Kertas Nasi Puas','Packaging Combo','Packaging Ala Carte','Packaging Paper Tray Dine In','Packaging Paper Bag Cokelat','Paper Bowl Crisbee 5oz','Tutup Lid Paper Bowl 5oz','BRCCBS 735 G (Crisbar)','SRMATCS 345 G (Matah)','SRMAMCS 250 G (Mamah)','JRBCSS 573 G (Gravy Crisbee)','Dus Teh Sisri','Dus Silky Pudding','Dus Perkedelku','Sak Tepung FC','Dus Sambal Sachet']

    barang_non_dc = []
    barang_dc = []
    for a in barang:
        if a.nama_item in item_dc:
            barang_dc.append(a)
        else:
            barang_non_dc.append(a)

    context = {
        'profile' : profile,
        'po' : po,
        'id_po' : id_po,
        'barang_non_dc' : barang_non_dc,
        'barang_dc' : barang_dc,
        'tanggal_kirim' : tanggal_kirim.strftime("%d %b %Y")
    }

    return render(request, 'rm_app/purchase_order/form_po_cabang.html', context)

@login_required(login_url='login_page')
def po_gunung_mas(request, id_po):

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)
    po = PurchaseOrder.objects.get(pk=id_po)
    barang = BarangPurchaseOrder.objects.filter(purchase_order=po)
    tanggal_kirim = po.tanggal_po + timedelta(days=1)

    item_dc = ['Dus Kertas Roll Printer','Kertas Nasi Puas','Packaging Combo','Packaging Ala Carte','Packaging Paper Tray Dine In','Packaging Paper Bag Cokelat','Paper Bowl Crisbee 5oz','Tutup Lid Paper Bowl 5oz','BRCCBS 735 G (Crisbar)','SRMATCS 345 G (Matah)','SRMAMCS 250 G (Mamah)','JRBCSS 573 G (Gravy Crisbee)','Dus Teh Sisri','Dus Silky Pudding','Dus Perkedelku','Sak Tepung FC','Dus Sambal Sachet']

    barang_non_dc = []
    barang_dc = []
    for a in barang:
        if a.nama_item in item_dc:
            barang_dc.append(a)
        else:
            barang_non_dc.append(a)

    context = {
        'profile' : profile,
        'po' : po,
        'barang_non_dc' : barang_non_dc,
        'barang_dc' : barang_dc,
        'tanggal_kirim' : tanggal_kirim.strftime("%d %b %Y")
    }

    pdf = render_to_pdf('rm_app/purchase_order/supplier/po_gunung_mas.html', context)

    # return HttpResponse(pdf, content_type='application/pdf')
    return render(request, 'rm_app/purchase_order/supplier/po_gunung_mas.html', context)


@login_required(login_url='login_page')
def konfirmasi_order(request, id_po):

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)
    po = PurchaseOrder.objects.get(pk=id_po)
    barang_po = BarangPurchaseOrder.objects.filter(purchase_order=po)

    if request.method == 'POST':
        for kunci in request.POST.keys():
            if kunci == 'csrfmiddlewaretoken':
                continue
            else:
                barangnya = barang_po.filter(nama_item=kunci)[0]

                if int(request.POST.get(kunci)) == 0:
                    barangnya.delete()

                barangnya.jumlah_order = orderan.main(int(request.POST.get(kunci)), barangnya.jumlah_order)
                # barangnya.jumlah_order = int(request.POST.get(kunci), barangnya.jumlah_order)
                barangnya.save()
        return redirect('form_po_cabang', id_po)

    maksimal = lambda x: math.ceil(x) + math.ceil(x*0.1)
    minimal = lambda x: math.ceil(x) - math.ceil(x*0.1)

    query_konfirmasi_order = [(p.nama_item, p.satuan, p.jumlah_order, minimal(p.jumlah_order), maksimal(p.jumlah_order)) for p in barang_po]

    context = {
        'profile' : profile,
        'barang_po' : barang_po,
        'query_konfirmasi_order' : query_konfirmasi_order
    }

    return render(request, 'rm_app/purchase_order/konfirmasi_order.html', context)

@login_required(login_url='login_page')
def penerimaan(request):

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)
    
    context = {
        'profile' : profile,
    }

    data_po = PurchaseOrder.objects.filter(profil_pengguna=profile).order_by("-id")
    query_penerimaan = []
    for d in data_po:
        status = StatusPurchaseOrder.objects.get(purchase_order=d)
        query_penerimaan.append([d,status])

    banyak_data_per_page = 10
    p = Paginator(query_penerimaan, banyak_data_per_page)
    page_num = request.GET.get('page', 1)

    try:
	    page = p.page(page_num)
    except EmptyPage:
	    page = p.page(1)

    banyak_halaman = [str(a+1) for a in range(p.num_pages)]
    context['banyak_halaman'] = banyak_halaman
    context['jumlah_halaman'] = len(banyak_halaman)
    context['halaman_aktif'] = str(page_num)
    context['data_po'] = page
    context['info_pagination'] = {
        'has_previous' : page.has_previous(),
        'has_next' : page.has_next()
    }
    if page.has_previous():
        context['info_pagination']['halaman_sebelumnya'] = page.previous_page_number()
    
    if page.has_next():
        context['info_pagination']['halaman_selanjutnya'] = page.next_page_number()

    return render(request, 'rm_app/purchase_order/history_purchase_order.html', context)


@login_required(login_url='login_page')
def terima_barang(request, id_po):

    u = User.objects.get(pk=request.user.id)
    profile = ProfilPengguna.objects.get(pengguna = u)
    po = PurchaseOrder.objects.get(pk=id_po)
    spo = StatusPurchaseOrder.objects.get(purchase_order = po)
    barang_po = BarangPurchaseOrder.objects.filter(purchase_order = po)

    if request.method == 'POST':
        for k in request.POST.keys():
            if k == 'csrfmiddlewaretoken':
                continue
            hasil_split = k.split('-')
            id_barang = int(hasil_split[1])
            barang_ponya = BarangPurchaseOrder.objects.get(pk=id_barang)
            bd = BarangDiterima(
                purchase_order = po,
                diterima_sebenarnya = barang_ponya,
                nama_barang = barang_ponya.nama_item,
                jumlah_diterima = int( request.POST.get(k) )
            )
            bd.save()
        baru_diterima = BarangDiterima.objects.filter(purchase_order = po)
        lengkap = True
        for bd in baru_diterima:
            if bd.jumlah_diterima != bd.diterima_sebenarnya.jumlah_order:
                lengkap = False
        if lengkap:
            spo.status = "Diterima Lengkap"
        else:
            spo.status = "Diterima Tidak Lengkap"

        spo.save()
        return redirect('penerimaan')

    context = {
        'profile' : profile,
        'barang_po' : barang_po
    }

    if spo.status == "Belum Diterima":
        context['belum_diterima'] = True
    else:
        diterima = BarangDiterima.objects.filter(purchase_order = po)
        context['barang_po'] = diterima


    return render(request, 'rm_app/purchase_order/terima_barang.html', context)