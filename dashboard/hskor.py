from .models import TugasProyek, TugasRutin, IsiTugasRutin
from django.contrib.auth.models import User

def hitungskor(user_id):
    pemilik = User.objects.get(id=user_id)
    tp = TugasProyek.objects.filter(pemilik_tugas=pemilik)
    tr = TugasRutin.objects.filter(pemilik_tugas=pemilik)

    total_skor_rutin = 0
    total_rutin = 0
    for rutin in tr:
    	isi_tr = IsiTugasRutin.objects.filter(tugas_rutin = rutin)
    	for isi in isi_tr:
    		if isi.ketuntasan == True:
                    total_rutin += 1
                    total_skor_rutin += isi.penilaian
                
    total_proyek = 0
    total_skor_proyek = 0
    for tugas_proyek in tp:
    	if tugas_proyek.ketuntasan == True:
            total_skor_proyek += tugas_proyek.penilaian
            total_proyek += 1

    total_tugas_tuntas = total_rutin + total_proyek
    if total_tugas_tuntas == 0:
        return [0, 0]

    hasil = (total_skor_proyek + total_skor_rutin) / total_tugas_tuntas
    hasil = str(hasil)
    hasil = hasil.split('.')
    hasil = hasil[0] + '.' + hasil[1][:2]
    hasil = float(hasil)

    return [hasil, total_tugas_tuntas]