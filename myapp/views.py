from django.shortcuts import render
from .models import Demand, Geography

# Create your views here.

def index_page(request):
    return render(request, 'index.html')


def demand_page(request):
    analitics = Demand.objects.all()
    return render(request, 'demand.html', {"analitic": analitics})


def geography_page(request):
    analitics1 = Geography.objects.order_by('med_salary')
    analitics2 = Geography.objects.order_by('vac_count')
    return render(request, 'geography.html', {"sal_analitic": analitics1, "vac_analitic": analitics2})