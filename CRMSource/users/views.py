from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms
from .mixin import OrganisorLoginRequiredMixin
from django.core.mail import send_mail

# Create your views here.


class UserRegistrationView(generic.CreateView):
    template_name = 'users/register.html'
    form_class = forms.UserModelForm
    
    def get_success_url(self):
        return reverse('user-login')


class LoginUserView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse('dashboard')
    
    
class LogoutUserView(LogoutView):
    template_name = 'users/logout.html'
   

class UserDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "users/user_details.html"
    queryset = models.User.objects.all()
    context_object_name = "user"


class TeamListView(OrganisorLoginRequiredMixin, generic.ListView):
    template_name = 'team/team_list.html'
    
    def  get_queryset(self):
        team_lead = self.request.user
        return models.Team.objects.filter(team_lead=team_lead)
    
  
class ManagerUserRegistrationView(OrganisorLoginRequiredMixin, generic.CreateView):
    template_name = 'users/register.html'
    form_class = forms.ManagerModelForm  
    
    def form_valid(self, form):
        # Checking if user is a manager and setting the organisor to fault
        user_ = form.save(commit=False)
        if user_.is_manager:
            user_.is_organisor = False
        user_.save()
        
        send_mail(subject="CRM Registration Invite", 
                  message="You were add as a manager on the CRM", 
                  from_email = "gig@gig.com", 
                  recipient_list=[user_.email]
                  )
        
        return super(ManagerUserRegistrationView, self).form_valid(form) 
    
    def get_success_url(self):
        return reverse('manager-section')


class ManagerListView(OrganisorLoginRequiredMixin, generic.ListView):
    template_name = 'users/managers.html'
    context_object_name = "manager"    
   
    def get_queryset(self):

        return models.User.objects.filter(is_manager=True)
    
    
    
    
class CreateTeamView(OrganisorLoginRequiredMixin, generic.CreateView):
    template_name = 'team/create_team.html'
    form_class = forms.TeamModelForm
    
    def get_success_url(self):
        return reverse('team-section')


class TeamDetailsView(OrganisorLoginRequiredMixin, generic.DetailView):
    template_name = 'team/team_detail.html'
    context_object_name = "team"    
   
    def get_queryset(self):
        team_lead = self.request.user
        return models.Team.objects.filter(team_lead=team_lead)
    
    
class UpdateTeamView(OrganisorLoginRequiredMixin, generic.UpdateView):
    template_name = 'team/update_team.html'
    form_class = forms.TeamModelForm
    queryset = models.Team.objects.all()
        
    def get_success_url(self):
        return reverse('team-section')

class DeleteTeamView(OrganisorLoginRequiredMixin, generic.DeleteView):
    template_name = "team/delete_team.html"
    context_object_name = "team"
    
    
    def get_queryset(self):
        team_lead = self.request.user
        return models.Team.objects.filter(team_lead=team_lead)
    
    def get_success_url(self):
        return reverse('team-section')