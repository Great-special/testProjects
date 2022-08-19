from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('',views.LeadListView.as_view(), name='lead-section'),
    # path('',views.leads_list, name='lead-section'),
    
    path('create_lead/',views.LeadCreateView.as_view(), name='create'),
    # path('create_lead/',views.lead_create, name='create'),
    
    path('<int:pk>/update/', views.LeadUpdateView.as_view(), name='update'),
    # path('<int:id>/update/', views.lead_update, name='update'),
    
    path('<int:pk>/', views.LeadDetailView.as_view(), name='lead-detail'),
    # path('<int:id>/',views.lead_detail, name='lead-detail'),
    
    path('delete/<str:pk>/', views.LeadDeleteView.as_view(), name='delete'),
    # path('delete/<str:id>/', views.lead_delete, name='delete'),
]
 