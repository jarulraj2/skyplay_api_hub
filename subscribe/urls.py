from django.urls import path, re_path
from . import views

urlpatterns = [
    #path('activation/', views.activation, name='activation'),
    path('activation/', views.payment_view, name='payment_view'),
    path("create_order/", views.create_order, name="create_order"),
    path("verify_payment/", views.verify_payment, name="verify_payment"),
    path("success/", views.payment_success, name="payment_success"),
    path("error/", views.payment_error, name="payment_error"),
   # path('<int:clientId>/<str:endDate>/<int:deviceId>/<int:channelId>/<int:amount>/', views.payment_view, name='payment'),

    #path('activation/?<int:clientId>/<int:deviceId>/<int:channelId>/<str:channelName>/<str:packs>/', views.payment_view, name='payment'),
    # Define the main payment URL
    #path('<int:clientId>/<str:endDate>/<int:deviceId>/<int:channelId>/<int:amount>/', views.payment_view, name='payment'),
    #path('<str:encoded_data>/', views.payment_view, name='payment'),
    # Define other necessary routes for the payment flow
 
    #path('test/', views.test_view, name='test_view'),

   # path('b64decode/<str:encoded_data>/', views.b64decode, name='b64decode'),

   
]
