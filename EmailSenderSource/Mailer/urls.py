from django.urls import path
from .views import *


urlpatterns = [
    path("add/", getEmails,name="getMail"),
    path("email/", index, name="mailDetail"),
]