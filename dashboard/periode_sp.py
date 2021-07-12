from .models import TugasProyek, TugasRutin, IsiTugasRutin, KenaSp, PeriodeSp
from django.contrib.auth.models import User
from django.utils import timezone
from .hskor import hitungskor
from datetime import date, timedelta

def evaluasi(periode):

    objekperiodesp = PeriodeSp.objects.get(pk=periode)
    awal = objekperiodesp.awal_periode
    akhir = objekperiodesp.akhir_periode

    id_user = [
        2, # pak randy
        3, # difa
        4, # teddy
        8, # vivi
        22, # bu novi
        23, # hafizh
        24, # bu ratih
        25, # hanifah
        26, # bu santi
        28, # pak beben
        32, # salma
        37, # pak dicky
        40, # pak jofy
        41, # pak hikmatullah
        42, # pak ilyas
        51, # tyo
        53, # annisa puzianti
        57, # bu karin
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

        banyaknya_tugas_yang_tuntas = 0

        tp = TugasProyek.objects.filter(pemilik_tugas=obj_user)
        tp = tp.filter(deadline__range=[awal, akhir])

        banyak_tp = len(tp)
        for tugas_proyek in tp:

            if tugas_proyek.ketuntasan:
                banyaknya_tugas_yang_tuntas += 1

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

                if tugas_rutin.ketuntasan:
                    banyaknya_tugas_yang_tuntas += 1

                if tugas_rutin.status == "Tuntas":
                    total_tuntas += 1
                elif tugas_rutin.status == "Terlambat":
                    total_terlambat += 1
                elif tugas_rutin.status == "Deadline":
                    total_deadline += 1

                if not (tugas_rutin.penilaian == None):
                    nilai_akhir += tugas_rutin.penilaian

        total_tugas = banyak_tp + banyak_tr

        print(nama)
        print(banyaknya_tugas_yang_tuntas)
        print(nilai_akhir)

        if banyaknya_tugas_yang_tuntas == 0:
            nilai_akhir = 0.0
            persen_terlambat = persenTerlambat(total_terlambat, total_tugas)
            persen_deadline = persenDeadline(total_deadline, total_tugas)
        else:
            nilai_akhir = str(nilai_akhir/banyaknya_tugas_yang_tuntas)
            list_nilai = nilai_akhir.split('.')
            nilai_akhir = list_nilai[0] + '.' + list_nilai[1][:2]
            nilai_akhir = float(nilai_akhir)

            persen_terlambat = persenTerlambat(total_terlambat, total_tugas)
            persen_deadline = persenDeadline(total_deadline, total_tugas)

        hasil.append((nama, bagian, total_tugas, total_tuntas, total_terlambat, total_deadline, nilai_akhir, persen_terlambat, persen_deadline, obj_user.id))

    # hasil.append(objekperiodesp.dieksekusi)
    return hasil

def persenTerlambat(total_terlambat, total_tugas):

    if total_tugas == 0:
        return 0

    hasil = total_terlambat / total_tugas
    hasil *= 100

    hasil = str(hasil)
    pisah = hasil.split('.')
    hasil = pisah[0] + '.' + pisah[1][:2]

    return float(hasil)

def persenDeadline(total_deadline, total_tugas):

    if total_tugas == 0:
        return 0

    hasil = total_deadline / total_tugas
    hasil *= 100

    hasil = str(hasil)
    pisah = hasil.split('.')
    hasil = pisah[0] + '.' + pisah[1][:2]

    return float(hasil)

def dapet_sp_periode_ini(rekap):

    hasil = []
    mulai_sp = date(2021, 3, 26)
    berakhir_dalam = timedelta(days=90)
    berakhir_sp = mulai_sp + berakhir_dalam

    for isi in rekap:
        sp = 0

        nilai_akhir = isi[-4]
        persen_terlambat = isi[-3]
        persen_deadline = isi[-2]
        nama = isi[0]
        bagian = isi[1]
        id_user = isi[-1]

        if nilai_akhir < 8:
            sp += 1
        if persen_terlambat > 20:
            sp += 1
        if persen_deadline > 5:
            sp += 1
        if sp > 0:
            hasil.append((nama, bagian, sp, mulai_sp, berakhir_sp, id_user))


    return hasil
