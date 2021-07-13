from django.urls import path

from . import views

urlpatterns = [
    path('info', views.info, name='info'),
    path('maintanence', views.maintanence, name='maintanence'),
    path('maintenance', views.maintenance, name='maintenance'),
    path('floorplans', views.floorplans, name='floorplans'),
    path('gallery', views.gallery, name='gallery'),
    path('amenities', views.amenities, name='amenities'),
    path('faq', views.faq, name='faq'),
    path('pay', views.pay, name='pay'),
    path('portal', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    path('', views.index, name='index')

]