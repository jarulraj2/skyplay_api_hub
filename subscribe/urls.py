from django.urls import path
from .views import payment_view, create_order, verify_payment, payment_success, payment_error

urlpatterns = [
    path("<int:clientId>/<str:endDate>/<int:deviceId>/<int:channelId>/<int:amount>", payment_view, name="payment"),
    path("create_order/", create_order, name="create_order"),
    path("verify_payment/", verify_payment, name="verify_payment"),
    path("success/", payment_success, name="payment_success"),
    path("error/", payment_error, name="payment_error"),
]
