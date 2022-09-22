from django.urls import path
from .views import *


urlpatterns = [
    path("email/", createMail, name='create-mail'),
    path("add/", getEmails,name="getMail-Address"),
    path("", index, name="express-mail"),
    path('list-mail/', listMail, name="list-mail"),
    path('list-mail/<int:pk>/', updateMail, name="mail-detail"),
    path('list-address/', listAddress, name="list-address"),
    path('list-address/<int:pk>/', updateAddress, name="address-detail"),
    path('list-address/<int:pk>/', updateAddress, name="delete-address"),
    path('register/', userRegister, name="register"),
    path('login/', userLogin, name="login"),
    path('logout/', userLogout, name="logout"),
]