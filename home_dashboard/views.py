from django.shortcuts import render
from django.http import HttpResponse
from home_dashboard import logika_query_tren_penjualan

# Create your views here.
def index(request):

    print(logika_query_tren_penjualan.main(7))

    return HttpResponse('<h1>Hello World</h1>')