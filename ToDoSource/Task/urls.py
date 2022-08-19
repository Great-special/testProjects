from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"), 
    path("create/", views.add, name = "create"), 
    path("update/<str:id>/", views.update_task, name = "update"),
    path("delete/<str:id>", views.delete_task, name='delete') 
]