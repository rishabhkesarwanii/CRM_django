from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def lead_list(request):
    lead = Lead.objects.all()

    context = {
        "leads": lead
        }

    return render(request, "leads/lead_list.html", context)


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)

    context = {
        "lead": lead
        }

    return render(request, "leads/lead_detail.html", context)