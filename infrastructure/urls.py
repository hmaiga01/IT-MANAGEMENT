from django.urls import path
from . import views



urlpatterns = [
   path('', views.homepage, name='homepage'), 
   path('personnel/', views.personnel, name='personnel'),
   path('administration_infra', views.administration, name='administration'),
   path('utilisateur', views.Utilisateur.as_view(), name="liste_utilisateurs"),
   path('create_user', views.create_user, name='create_user'),
   path('machine_create/', views.machine_create, name='machine_create'),
   path('machine_update/<int:machine_id>/', views.machine_update, name='modifier_machine'),
   path('machine_detail/<int:machine_id>/', views.machine_detail, name='machine_detail'),
   path('machine_delete/<int:machine_id>/', views.machine_delete, name='supprimer_machine')
]