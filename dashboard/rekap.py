from .models import TugasProyek, TugasRutin, IsiTugasRutin, PeriodeSp
from django.contrib.auth.models import User

def query_rekap(periode_sp, id_user):

    periode = PeriodeSp.objects.get(pk=periode_sp)
    awal = periode.awal_periode
    akhir = periode.akhir_periode

    pemilik_tgs = User.objects.get(pk=id_user)

    total_tugas = 0    
    total_tuntas = 0
    total_terlambat = 0
    total_deadline = 0

    akumulasi_nilai = 0
    tugas_yang_dinilai = 0

    nilai_akhir = 0
    persen_terlambat = 0
    persen_deadline = 0

    # TUGAS PROYEK
    tp = TugasProyek.objects.filter(pemilik_tugas=pemilik_tgs, deadline__range=[awal, akhir])
    total_tugas += len(tp)
    total_tuntas += len(tp.filter(status="Tuntas"))
    total_terlambat += len(tp.filter(status="Terlambat"))
    total_deadline += len(tp.filter(status="Deadline"))
    
    for tgs in tp:
        if tgs.penilaian != None:
            akumulasi_nilai += tgs.penilaian
            tugas_yang_dinilai += 1

    # TUGAS RUTIN
    tr = TugasRutin.objects.filter(pemilik_tugas=pemilik_tgs)
    for t in tr:
        isi_tr = IsiTugasRutin.objects.filter(tugas_rutin=t, deadline__range=[awal, akhir])
        total_tugas += len(isi_tr)
        total_tuntas += len(isi_tr.filter(status="Tuntas"))
        total_terlambat += len(isi_tr.filter(status="Terlambat"))
        total_deadline += len(isi_tr.filter(status="Deadline"))
        for tgs in isi_tr:
            if tgs.penilaian != None:
                akumulasi_nilai += tgs.penilaian
                tugas_yang_dinilai += 1

    if tugas_yang_dinilai == 0:
        nilai_akhir = 0
    else:
        nilai_akhir = akumulasi_nilai / tugas_yang_dinilai
        nilai_akhir = "{:.2f}".format(nilai_akhir)
        nilai_akhir = float(nilai_akhir)

    if total_tugas == 0:
        persen_terlambat = 0
        persen_deadline = 0
    else:
        persen_terlambat = ngeformat_persen(total_terlambat, total_tugas)
        persen_deadline = ngeformat_persen(total_deadline, total_tugas)

    hasil = [total_tugas, total_tuntas, total_terlambat, total_deadline, nilai_akhir, persen_terlambat, persen_deadline]

    return hasil

def ngeformat_persen(pembilang, penyebut):

    pembagian = 100*(pembilang/penyebut)
    pembagian = "{:.2f}".format(pembagian)
    pembagian = float(pembagian)

    return pembagian