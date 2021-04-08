from .models import TugasProyek, TugasRutin, IsiTugasRutin
from django.contrib.auth.models import User
from .hskor import hitungskor

def query_index_sp():

    id_user = [
        2, # pak randy
        3, # difa
        4, # teddy
        6, # astia
        8, # vivi
        22, # bu novi
        23, # hafizh
        24, # bu ratih
        25, # hanifah
        26, # bu santi
        27, # pak djuki
        28, # pak beben
        29, # friski
        30, # farhan
        31, # rara
        32, # salma
    ]

    hasil = []
    for id_pengguna in id_user:
        
        total_tuntas = 0
        total_terlambat = 0
        total_deadline = 0

        skor = hitungskor(id_pengguna)

        # NAMA
        objek_pengguna = User.objects.get(pk=id_pengguna)
        nama = objek_pengguna.first_name
        bagian = objek_pengguna.last_name

        # TOTAL TUGAS
        tp = TugasProyek.objects.filter(pemilik_tugas=objek_pengguna)
        banyak_tp = len(tp)
        for tugas in tp:
            if tugas.status == 'Tuntas':
                total_tuntas += 1
            elif tugas.status == 'Terlambat':
                total_terlambat += 1
            elif tugas.status == 'Deadline':
                total_deadline += 1

        banyak_tr = 0
        tr = TugasRutin.objects.filter(pemilik_tugas=objek_pengguna)
        for tugasrutin in tr:
            isitr = IsiTugasRutin.objects.filter(tugas_rutin=tugasrutin)
            banyak_tr += len(isitr)
            for isi in isitr:
                if isi.status == 'Tuntas':
                    total_tuntas += 1
                elif isi.status == 'Terlambat':
                    total_terlambat += 1
                elif isi.status == 'Deadline':
                    total_deadline += 1

        total_tugas = banyak_tp + banyak_tr

        persen_terlambat = persenTerlambat(total_terlambat, total_tugas)
        persen_deadline = persenDeadline(total_deadline, total_tugas)

        hasil.append((nama, bagian, total_tugas, total_tuntas, total_terlambat, total_deadline, skor[0], persen_terlambat, persen_deadline))

    return hasil

def persenTerlambat(total_terlambat, total_tugas):
    hasil = total_terlambat / total_tugas
    hasil *= 100

    hasil = str(hasil)
    pisah = hasil.split('.')
    hasil = '%' + pisah[0] + '.' + pisah[1][:2]

    return hasil

def persenDeadline(total_deadline, total_tugas):
    hasil = total_deadline / total_tugas
    hasil *= 100

    hasil = str(hasil)
    pisah = hasil.split('.')
    hasil = '%' + pisah[0] + '.' + pisah[1][:2]

    return hasil