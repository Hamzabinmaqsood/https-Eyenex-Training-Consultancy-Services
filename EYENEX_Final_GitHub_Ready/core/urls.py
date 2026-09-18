from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('ielts/', views.ielts, name='ielts'),
    path('study-abroad/', views.study_abroad, name='study_abroad'),
    path('leadership-training/', views.leadership, name='leadership'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms, name='terms'),
]
