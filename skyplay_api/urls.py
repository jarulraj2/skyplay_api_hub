from django.urls import path
from . import views

urlpatterns = [
    # Path for getting client name by client_id
    path('get_client_name/<int:client_id>/', views.get_client_name, name='get_client_name'),

    # Path for getting channel name by channel_id
    path('get_channel_name/<int:channel_id>/', views.get_channel_name, name='get_channel_name'),

    # Path for subscribing to a channel
    path('set_subscribe_to_channel/<int:client_id>/<str:end_date>/<int:device_id>/<int:channel_id>/', views.set_subscribe_to_channel, name='set_subscribe_to_channel'),
]
