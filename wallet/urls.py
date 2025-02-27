from django.urls import path
from .views import wallet_view, add_money, verify_payment,  payment_success, payment_error
app_name = "wallet" 
urlpatterns = [
    path("", wallet_view, name="wallet_view"),
    path("add_money/", add_money, name="add_money"),
    path("verify_payment/", verify_payment, name="verify_payment"),
    path("success/", payment_success, name="payment_success"),
    path("error/", payment_error, name="payment_error"),
]
