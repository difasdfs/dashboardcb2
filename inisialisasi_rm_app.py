from rm_app.models import Cabang

cabang = ['Antapani', 'Jatinangor', 'Metro Margahayu', 'Sukapura', 'Sukabirus', 'Unjani', 'Cisitu', 'Sukajadi']

def initnya():
    for cbng in cabang:
        c = Cabang(nama_cabang=cbng)
        c.save()