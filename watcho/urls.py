from django.urls import path
from .views import EncryptionDecryptionView,  EncryptionAPI, DecryptionAPI, SubscriptionPlanDetailsAPI


urlpatterns = [
    path('encryption/', EncryptionDecryptionView.as_view(), name='encryption_decryption_view'),
    path('api/encrypt/', EncryptionAPI.as_view(), name='encrypt'),
    path('api/decrypt/', DecryptionAPI.as_view(), name='decrypt'),
    path('api/subscription-plan-details/', SubscriptionPlanDetailsAPI.as_view(), name='subscription_plan_details'),
]
