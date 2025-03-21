from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ott_subscription'  # ✅ Add this to define the namespace
urlpatterns = [
    path('login/', views.login_view, name='login'),
    #path('verify_email/', views.verify_email_view, name='verify_email'),
    #path('verify_phone/', views.verify_phone_view, name='verify_phone'),
    path('platforms/', views.platforms_view, name='platforms'),  # Example OTT page
    path('logout/', views.logout_view, name='logout'),
    path('get-skylink-plans/', views.get_skylink_plans, name='get_skylink_plans'),
    path('api/ott_activation/', views.ott_activation, name='ott_activation'),

        # URL to create a Razorpay order
    path('create-ott-order/', views.create_razorpay_order, name='create-razorpay-order'),    
    # URL to confirm payment after the user makes the payment
    path('verify_payment/', views.confirm_payment, name='confirm-payment'),
    path('transactions/', views.transactions_view, name='transactions_view'),
    path('api/transactions/', views.get_transactions, name='api_transactions'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/dashboard-data/', views.get_dashboard_data, name='dashboard-data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
