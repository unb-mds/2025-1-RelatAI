from django.urls import path
from . import views

urlpatterns = [
    path('ipca/', views.exibir_ipca, name='exibir_ipca'),
    path('igpm/', views.exibir_igpm, name='exibir_igpm'),

]
