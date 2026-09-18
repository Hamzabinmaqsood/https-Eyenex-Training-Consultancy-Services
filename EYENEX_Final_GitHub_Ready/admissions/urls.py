from django.urls import path

from . import views

app_name = 'admissions'

urlpatterns = [
    path('admissions/', views.admissions, name='admissions'),
    path('apply/', views.apply, name='apply'),
    path('courses/<slug:slug>/appointment/', views.course_appointment, name='course_appointment'),
    path('staff/payment-receipts/<int:pk>/', views.payment_receipt, name='payment_receipt'),
]
