from .models import TugasProyek, TugasRutin, IsiTugasRutin, KenaSp, PeriodeSp
from django.contrib.auth.models import User
from django.utils import timezone
from .hskor import hitungskor

def evaluasi():

    objekperiodesp = PeriodeSp.objects.get(pk=1)
    awal = objekperiodesp.awal_periode
    akhir = objekperiodesp.akhir_periode

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
        33, # pak arif      
        34, # wida
    ]

    hasil = []
    for id_pengguna in id_user:
        obj_user = User.objects.get(pk=id_pengguna)
        nama = obj_user.first_name
        bagian = obj_user.last_name
        
        nilai_akhir = 0
        total_tuntas = 0
        total_terlambat = 0
        total_deadline = 0

        tp = TugasProyek.objects.filter(pemilik_tugas=obj_user)
        tp = tp.filter(deadline__range=[awal, akhir])
        
        banyak_tp = len(tp)
        for tugas_proyek in tp:
            if tugas_proyek.status == "Tuntas":
                total_tuntas += 1
            elif tugas_proyek.status == "Terlambat":
                total_terlambat += 1
            elif tugas_proyek.status == "Deadline":
                total_deadline += 1
            
            if not (tugas_proyek.penilaian == None):
                nilai_akhir += tugas_proyek.penilaian

        banyak_tr = 0
        tr = TugasRutin.objects.filter(pemilik_tugas=obj_user)
        for itr in tr:
            isi_tr = IsiTugasRutin.objects.filter(tugas_rutin=itr)
            isi_tr = isi_tr.filter(deadline__range=[awal, akhir])
            banyak_tr += len(isi_tr)
            for tugas_rutin in isi_tr:
                if tugas_rutin.status == "Tuntas":
                    total_tuntas += 1
                elif tugas_rutin.status == "Terlambat":
                    total_terlambat += 1
                elif tugas_rutin.status == "Deadline":
                    total_deadline += 1

                if not (tugas_rutin.penilaian == None):
                    nilai_akhir += tugas_rutin.penilaian

        total_tugas = banyak_tp + banyak_tr

        if total_tuntas == 0:
            nilai_akhir = 0.0
            persen_terlambat = 0.0
            persen_deadline = 0.0
        else:
            nilai_akhir = str(nilai_akhir)
            nilai_akhir = nilai_akhir.split('.')
            nilai_akhir = nilai_akhir[0] + '.' + nilai_akhir[1]

            persen_terlambat = persenTerlambat(total_terlambat, total_tugas)
            persen_deadline = persenDeadline(total_deadline, total_tugas)

        hasil.append([nama, bagian, total_tugas, total_tuntas, total_terlambat, total_deadline, nilai_akhir, persen_terlambat, persen_deadline])

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

# def nilaiAkhir(nilai_akhir):
