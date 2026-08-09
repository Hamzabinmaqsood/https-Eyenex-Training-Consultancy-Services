from django.urls import path

from . import views

app_name = 'admissions'

urlpatterns = [
    path('admissions/', views.admissions, name='admissions'),
    path('apply/', views.apply, name='apply'),
]
