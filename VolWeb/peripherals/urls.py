from django.urls import path
from investigations.views import investigations
from . import views

urlpatterns = [
    path('new-devices', views.new_devices, name='new-devices'),
    path('peripherals', views.peripherals, name='peripherals'),
    path('register-peripheral', views.register_peripheral, name='register-peripheral'),
    path('auto-investigate/<str:storage_device_serial_id>', views.auto_investigate, name='auto-investigate'),

    path('investigations/', investigations, name='investigations'),
]
