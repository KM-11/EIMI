from django.contrib import admin
from django.urls import path,include
from .models import Muestra
from . import views


urlpatterns = [
    path('',views.index),
    path('general_samples_view', views.samples_detail, name="general_sample_names"),
     path('<str:muestra_hash>/', views.sample_detail, name='sample_detail'),
    path('familias/<int:familia_id>/', views.family_detail, name='family_detail')
]
