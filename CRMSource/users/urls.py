from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.LoginUserView.as_view(), name='user-login'),
    path('logout/', views.LogoutUserView.as_view(), name='user-logout'),
    
    path('add_user/', views.ManagerUserRegistrationView.as_view(), name='user-add'),
    path("manager/", views.ManagerListView.as_view(), name="manager-section"),
    path("manager/<int:pk>/", views.ManagerListView.as_view(), name="manager-detail"),

    path('team/', views.TeamListView.as_view(), name='team-section'),
    path('create_team/', views.CreateTeamView.as_view(), name='create-team'),
    path('team/<int:pk>/', views.TeamDetailsView.as_view(), name='team-detail'),
    path('team/<int:pk>/update/', views.UpdateTeamView.as_view(), name='team-update'),
    path("team/<int:pk>/delete", views.DeleteTeamView.as_view(), name="team-delete")
    ]