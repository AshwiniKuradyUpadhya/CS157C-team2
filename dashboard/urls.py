from django.urls import path

from . import views

urlpatterns = [
    path('info', views.info, name='info'),
    path('maintenance', views.maintenance, name='maintenance'),
    path('floorplans', views.floorplans, name='floorplans'),
    path('gallery', views.gallery, name='gallery'),
    path('amenities', views.amenities, name='amenities'),
    path('faq', views.faq, name='faq'),
    path('pay', views.pay, name='pay'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('reslogin', views.reslogin, name='reslogin'),
    path('employeelogin', views.employeelogin, name = 'employeelogin'),
    path('resident_register', views.resident_register, name = 'resident_register'),
    path('employee_register', views.employee_register, name = 'employee_register'),
    path('', views.index, name='index'),
    path('userpage/', views.userpage, name='userpage'),
]