from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import LeadForm


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

def lead_create(request):
    form = LeadForm()

    if request.method == "POST":

        print("Receiving a POST request")
        form = LeadForm(request.POST)

        if form.is_valid():
            # print("Form is valid")
            # print(form.cleaned_data)
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            age = form.cleaned_data["age"]
            agent = Agent.objects.first()
            Lead.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,
                agent=agent
            )

            # print("Lead has been created")
            return redirect("/leads")


    context = {
        "form": form
        }
    
    return render(request, "leads/lead_create.html", context)