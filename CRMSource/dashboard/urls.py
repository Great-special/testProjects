from django.urls import path
from . import views
from .views import LandingPageView




urlpatterns = [
    # path('', views.home, name='dashboard'),
    path('', LandingPageView.as_view(), name='dashboard'),
]
