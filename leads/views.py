from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import *
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.views impor generic  -------- generic.TemplateView so on 
from agents.mixins import OrganiserAndLoginRequiredMixin



class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")



class LandingPageView(TemplateView):
    template_name = "leads/landing.html"
    

def landing_page(request):
    return render(request, "leads/landing.html")






class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context


# def lead_list(request):
#     lead = Lead.objects.all()
#     context = {
#         "leads": lead
#         }
#     return render(request, "leads/lead_list.html", context)



class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
    



# def lead_detail(request, pk):
#     lead = Lead.objects.get(id=pk)
#     context = {
#         "lead": lead
#         }
#     return render(request, "leads/lead_detail.html", context)



class LeadCreateView(OrganiserAndLoginRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        #send email
        #send text message
        #assign user to lead
        send_mail(
            subject = "A lead has been created",
            message = "Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


    # def get_success_url(self):
    #     return "/leads"

# def lead_create(request):
#     form = LeadModelForm()
#     if request.method == "POST":
#         # print("Receiving a POST request")
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")
#     context = {
#         "form": form
#         }
#     return render(request, "leads/lead_create.html", context)



class LeadUpdateView(OrganiserAndLoginRequiredMixin, UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)



# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadModelForm(instance = lead)  #the single instance of the model we want to update
#     if request.method == "POST":
#         form = LeadModelForm(request.POST,instance = lead)
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")
#     context = {
#         "lead": lead,
#         "form": form
#         }
#     return render(request, "leads/lead_update.html", context)




class LeadDeleteView(OrganiserAndLoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)



# def lead_delete(request, pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect("/leads")

# def lead_create(request):
    # form = LeadForm()
    # if request.method == "POST":
    #     print("Receiving a POST request")
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         # print("Form is valid")
    #         # print(form.cleaned_data)
    #         first_name = form.cleaned_data["first_name"]
    #         last_name = form.cleaned_data["last_name"]
    #         age = form.cleaned_data["age"]
    #         agent = Agent.objects.first()
    #         Lead.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age=age,
    #             agent=agent
    #         )
    #         # print("Lead has been created")
    #         return redirect("/leads")
#     context = {
#         "form": form
#         }
#     return render(request, "leads/lead_create.html", context)



# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         print("Receiving a POST request")
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             # print("Form is valid")
#             # print(form.cleaned_data)
#             first_name = form.cleaned_data["first_name"]
#             last_name = form.cleaned_data["last_name"]
#             age = form.cleaned_data["age"]
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             # print("Lead has been created")
#             return redirect("/leads")
#     context = {
#         "lead": lead,
#         "form": form
#         }
#     return render(request, "leads/lead_update.html", context)