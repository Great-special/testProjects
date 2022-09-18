from django.urls import path
from .views import *


urlpatterns = [
    path("", createMail, name='create-mail'),
    path("add/", getEmails,name="getMail-Address"),
    path("email/", index, name="express-mail"),
    path('list-mail/', listMail, name="list-mail"),
    path('list-mail/<int:pk>/', updateMail, name="mail-detail"),
    path('list-address/', listAddress, name="list-address"),
    path('list-address/<int:pk>/', updateAddress, name="address-detail"),
]