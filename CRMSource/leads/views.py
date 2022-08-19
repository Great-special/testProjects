from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import  LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from . models import Lead
from .forms import LeadForm
from users.mixin import OrganisorLoginRequiredMixin
# Create your views here.



"""
    Class based views are views that performs specify task.
    And they follow CRUD+L = create read/retrieve, update, delete and list
    To use the class based views in the urls path add the method ClassViewName.as_view()
    when working with class based views the context which is not given by me, is by default set to object_list.
    Or to use your own name set the context_object_name to your varible
    
    The class view is above why the function based is below.
"""

class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'leads/lead_section.html'
    context_object_name = "leads"
    
    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.all()
            
        if user.is_manager:
            queryset = queryset.filter(manager__team_lead=self.request.user)
        return queryset


# def leads_list(request):
#     leads = Lead.objects.all()
#     context = {
#         'leads': leads,
#     }
#     return render(request, 'leads/lead_section.html', context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_details.html'
    context_object_name = "lead"
    
    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.all()
            
        if user.is_manager:
            queryset = queryset.filter(manager__team_lead=self.request.user)
        return queryset
    
# def lead_detail(request, id):
#     lead = Lead.objects.get(id=id)
    
#     context = {
#         'lead': lead,
#     }
#     return render(request, 'leads/lead_details.html', context)


class LeadCreateView(OrganisorLoginRequiredMixin, CreateView):
    template_name = 'leads/create_lead.html'
    form_class = LeadForm
    
    def get_success_url(self):
        return reverse("leads:lead-section")
    
    def form_valid(self, form):
        # Setting the lead owner to the loggedin user
        lead_owner = form.save(commit=False)
        lead_owner.owner = self.request.user
        lead_owner.save()
        
        # TO send Mail
        send_mail(
            subject = "A lead Has Been Created",
            message = "Go To The Site To See The Lead",
            from_email = "test@test.com",
            recipient_list = ["test2@test.com"]
        )
        
        return super(LeadCreateView, self).form_valid(form)
    

# def lead_create(request):
#     form = LeadForm()
    
#     if request.method == 'POST':
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/leads')
    
#     context = {
#         'form': form
#     }
#     return render(request, "leads/create_lead.html", context)


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'leads/update_lead.html'
    form_class = LeadForm
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(manager__team_lead=self.request.user)
    
    
    def get_success_url(self):
        return reverse("leads:lead-section")


# def lead_update(request, id):
    
#     lead = Lead.objects.get(id=id)
#     form = LeadForm(instance=lead)
    
#     if request.method == 'POST':
#         form = LeadForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect('/leads')
        
#     context = {
#         'lead': lead,
#         'form': form,
#     }
#     template_name = 'leads/update_lead.html'
#     return render( request, template_name, context)


class LeadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'leads/delete_lead.html'
    
    context_object_name = 'item'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(manager__team_lead=self.request.user)
    
    
    def get_success_url(self):
        return reverse("leads:lead-section")


# def lead_delete(request, id):
#     lead = Lead.objects.get(id=id)
#     if request.POST:
#         lead.delete()
#         return redirect('/leads')
    
#     context = {
#         'item':lead
#     }
#     return render(request, 'leads/delete_lead.html', context)