from .models import TugasRutin, IsiTugasRutin

def rinci_tr(bagian_):

    hasil = []
    tugas_rutin = TugasRutin.objects.filter(bagian=bagian_)
    for tr in tugas_rutin:

        a = hitung_total_tuntas(tr)

        hasil.append( (tr.pemilik_tugas.first_name, tr.judul, tr.id, a[0], a[1]) )

    hasil.sort(key=lambda tup: tup[2])
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