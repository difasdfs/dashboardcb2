from .models import TugasRutin, IsiTugasRutin
from django.contrib.auth.models import User

def rinci_tr(bagian_, tampilkan_tuntas_semua = False):

    hasil = []
    tugas_rutin = TugasRutin.objects.filter(bagian=bagian_)
    for tr in tugas_rutin:

        a = hitung_total_tuntas(tr)

        if not tampilkan_tuntas_semua:
            if a[0] == a[1]:
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

        hasil.append( (tr.judul, tr.id, ht[0], ht[1]) )

    hasil.sort(key=lambda tup: tup[1])
    hasil = hasil[::-1]

    return hasil

def hitung_total_tuntas(tr):

    total_tuntas = 0
    isi_tugas_rutin = IsiTugasRutin.objects.filter(tugas_rutin=tr)
    banyak_tugas = len(isi_tugas_rutin)
    for itr in isi_tugas_rutin:
        if (itr.ketuntasan == True):
            total_tuntas += 1

    return (total_tuntas, banyak_tugas)