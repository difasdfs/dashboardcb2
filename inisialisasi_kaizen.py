from dashboard.models import Complaint, KaizenTimOutlet

def main():
    complaint = Complaint.objects.all()

    for c in complaint:
        kto = KaizenTimOutlet(
            complaint = c,
            solusi_sekarang = '',
            kronologis_kejadian = '',
            analisis_akar_masalah  = '',
            action_plan_kaizen = ''
        )
        kto.save()