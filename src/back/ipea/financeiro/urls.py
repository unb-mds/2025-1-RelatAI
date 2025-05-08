from django.urls import path
from . import views

urlpatterns = [
    path('selic/', views.selic, name='selic'),
    path('ipca/', views.ipca, name='ipca'),
    path('cambio/', views.cambio, name='cambio'),

]
