from django.urls import path
from . import views

urlpatterns = [
    path('ipca/', views.exibir_ipca, name='exibir_ipca'),
    path('igpm/', views.exibir_igpm, name='exibir_igpm'),
    path('inpc/', views.exibir_igpm, name='exibir_inpc'),
    path('cambio/', views.exibir_igpm, name='exibir_cambio'),
    path('juros/', views.exibir_igpm, name='exibir_taxa_de_juros'),

]
