from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login/', views.login_view, name='login'),
    #path('verify_email/', views.verify_email_view, name='verify_email'),
    #path('verify_phone/', views.verify_phone_view, name='verify_phone'),
    path('ott_page/', views.ott_page, name='ott_page'),  # Example OTT page
    path('logout/', views.logout_view, name='logout'),
    path('get-skylink-plans/', views.get_skylink_plans, name='get_skylink_plans'),
    path('api/ott_activation/', views.ott_activation, name='ott_activation'),

        # URL to create a Razorpay order
    path('create-ott-order/', views.create_razorpay_order, name='create-razorpay-order'),    
    # URL to confirm payment after the user makes the payment
    path('verify_payment/', views.confirm_payment, name='confirm-payment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
