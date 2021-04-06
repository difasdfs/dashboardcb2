from .models import TugasRutin, IsiTugasRutin, PeriodeSp
from django.contrib.auth.models import User

def rinci_tr(bagian_, tampilkan_tuntas_semua = False):

    hasil = []
    
    tugas_rutin = TugasRutin.objects.filter(bagian=bagian_).exclude(archive=True)
    for tr in tugas_rutin:

        a = hitung_total_tuntas(tr)

        if not tampilkan_tuntas_semua:
            if a[0] == a[1]:
                continue
            if jangan_tampilkan_tugas(tr):
                continue
        

        hasil.append( (tr.pemilik_tugas.first_name, tr.judul, tr.id, a[0], a[1]) )

    hasil.sort(key=lambda tup: tup[2])
    hasil = hasil[::-1]

    return hasil

def rinci_tr_eksekutif(id, hilang=True):

    hasil = []

    user_eksekutif = User.objects.get(pk=id)
    tugas_rutin = TugasRutin.objects.filter(pemilik_tugas=user_eksekutif)

    for tr in tugas_rutin:

        ht = hitung_total_tuntas(tr)

        if hilang:
            if ht[0] == ht[1]:
                continue
        
        if jangan_tampilkan_tugas(tr):
            continue

        hasil.append( (tr.judul, tr.id, ht[0], ht[1]) )

    hasil.sort(key=lambda tup: tup[1])
    hasil = hasil[::-1]

    return hasil

def jangan_tampilkan_tugas(tr):
    # input tugas rutin
    # ngecek deadline isi tugas rutin dalam tugas rutin
    # jika deadline semua, jangan dikembalikan
    periode = PeriodeSp.objects.get(pk=2)
    awal = periode.awal_periode
    akhir = periode.akhir_periode
    isi_tugas_rutin = IsiTugasRutin.objects.filter(tugas_rutin=tr)
    banyak_isi_tugas_rutin = len(isi_tugas_rutin)
    banyak_deadline_diluar_periode = 0
    
    kembali = []

    for isitr in isi_tugas_rutin:
        if isitr.deadline < awal:
            banyak_deadline_diluar_periode += 1

    if banyak_deadline_diluar_periode == banyak_isi_tugas_rutin:
        jangan_ditampilkan = True
    else:
        jangan_ditampilkan = False
    
    return jangan_ditampilkan

def hitung_total_tuntas(tr):

    total_tuntas = 0
    isi_tugas_rutin = IsiTugasRutin.objects.filter(tugas_rutin=tr)
    banyak_tugas = len(isi_tugas_rutin)
    for itr in isi_tugas_rutin:
        if (itr.ketuntasan == True):
            total_tuntas += 1

    return (total_tuntas, banyak_tugas)