from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.



class LandingPageView(TemplateView):
    template_name= 'landing.html'



def home(request):
    
    template_name = 'landing.html'
    return render(request, template_name)