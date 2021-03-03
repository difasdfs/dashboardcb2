from django.contrib.auth.models import User
from .models import TugasProyek, TugasRutin, IsiTugasRutin

def hitungskor(user_id):
	pemilik = User.objects.get(id=user_id)
	tp = TugasProyek.objects.filter(pemilik_tugas=pemilik)
	tr = TugasRutin.objects.filter(pemilik_tugas=pemilik)
	
	total_skor_rutin = 0
	for rutin in tr:
		isi_tr = IsiTugasRutin.objects.filter(tugas_rutin = rutin)
		for isi in isi_tr:
			if isi.status == 'Tuntas':
			    total_skor_rutin += isi.penilaian		

	total_skor_proyek = 0
	for tugas_proyek in tp:
		if tugas_proyek.status == 'Tuntas':
			total_skor_proyek += tugas_proyek.penilaian
	
	return total_skor_proyek + total_skor_rutin