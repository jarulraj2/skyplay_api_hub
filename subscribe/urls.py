from django.urls import path, re_path
from . import views

urlpatterns = [
    path("create_order/", views.create_order, name="create_order"),
    path("verify_payment/", views.verify_payment, name="verify_payment"),
    path("success/", views.payment_success, name="payment_success"),
    path("error/", views.payment_error, name="payment_error"),

    # Define the main payment URL
    #path('<int:clientId>/<str:endDate>/<int:deviceId>/<int:channelId>/<int:amount>/', views.payment_view, name='payment'),
    path('<str:encoded_data>/', views.payment_view, name='payment'),
    # Define other necessary routes for the payment flow
 
    #path('test/', views.test_view, name='test_view'),

   # path('b64decode/<str:encoded_data>/', views.b64decode, name='b64decode'),

   
]
