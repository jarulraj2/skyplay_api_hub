from django.urls import path
from .views import subscription_plan_details, subscription_request_watcho_omni,current_plan_details, verify_transaction,transaction_history,subscription_plan_details_with_duration,subscription_request_watchoplan

urlpatterns = [
    path("watcho/subscription-plan-details/", subscription_plan_details, name="subscription-plan-details"),
    path("watcho/subscription-request-watcho-omni/", subscription_request_watcho_omni, name="subscription-request-watcho-omni"),
        path("watcho/current-plan-details/", current_plan_details, name="current-plan-details"),
        path("watcho/verify-transaction/", verify_transaction, name="verify-transaction"),
         path("watcho/transaction-history/", transaction_history, name="transaction-history"),
             path("watcho/subscription-plan-details-with-duration/", subscription_plan_details_with_duration, name="subscription_plan_details-with-duration"),
             path('watcho/subscription/request-watchoplan/', subscription_request_watchoplan, name='subscription_request_watchoplan'),
]
