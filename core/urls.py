from django.urls import path
from . import views

handler500 = 'core.views.custom_page_not_found_view'

urlpatterns = [
    path('', views.index_view, name = 'index'),
    path('signin_doctor/', views.signin_view_doctor, name='signin_doctor'),
    path('signout_doctor/', views.signout_view_doctor, name='signout_doctor'),
    path('signin_register/', views.signin_view_register, name='signin_register'),
    path('signout_register/', views.signout_view_register, name='signout_register'),
    path('appointment/', views.appointment_view, name = 'appointment'),
    path('dashboard/', views.dashboard_view, name = 'dashboard'),
    path('register/', views.register_dashboard, name = 'register'),
    path('contact/', views.contact_view, name = 'contact'),
    path('schedule/', views.schedule_view, name = 'schedule'),
    path('about/',views.about_view, name = 'about'),
    path('prescription/<int:pk>/', views.prescription_view, name = 'prescription'),
    path('prescription_download/<int:pk>/', views.presdown_view, name = 'presdown'),
    path('all_patient_view/', views.all_patient_view, name = 'all_patient_view'),
    path('ajax/save/medicine/', views.save_medicine, name = 'save_medicine'),
    path('ajax/save/test_suggetion/', views.save_test_suggetion, name = 'save_test_suggetion'),
    path('ajax/delete/medicine/', views.medicine_delete, name = 'delete_medicine'),
    path('ajax/delete/test_suggetion/', views.test_suggetion_delete, name = 'delete_test_suggetion'),
    path('ajax/delete/appointment/', views.appointment_delete, name = 'delete_appointment'),
    path('ajax/filter/appointment/', views.all_patient_filter, name = 'filter_appointment'),
    path('ajax/update/med_test/', views.med_test_update, name = 'update_mt'),
    path('ajax/autocomplete/medicine', views.auto_med, name = 'auto_med'),
    path('ajax/paying_status', views.paying_status, name = 'status'),
    path('ajax/check_status_view', views.check_status_view, name = 'check'),
    path('change/', views.change_pass, name = 'change'),
    path('updates/<int:pk>/', views.appointment_update, name = 'updates'),
]