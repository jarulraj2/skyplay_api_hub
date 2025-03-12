from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from django.contrib import messages
from twilio.rest import Client
import random
from django.contrib.auth import logout
import re
from django.shortcuts import render, redirect  # <-- Add this import
from .models import SkylinkPlan, OTTPlan
from django.http import JsonResponse

def ott_page(request):
    # Retrieve user contact info from session
    email = request.session.get('email', None)
    phone_number = request.session.get('phone_number', None)

    # Check if the user is authenticated (i.e., they have verified their contact)
    if email:
        contact = email
        verification_type = 'email'
    elif phone_number:
        contact = phone_number
        verification_type = 'phone'
    else:
        # If no contact info is available in session, redirect to login page
        return redirect('login')  # Make sure you have a name for your login view in urls.py

    return render(request, 'ott_subscription/ott_page.html', {
        'contact': contact,
        'verification_type': verification_type
    })

# Function to send verification code to email
def send_verification_email(email):
    verification_code = "123456"  # Default verification code
    subject = "Your OTP Verification Code"
    message = f"Your verification code is {verification_code}"
    from_email = settings.EMAIL_HOST_USER  # Replace with your email
    send_mail(subject, message, from_email, [email])

# Function to send verification code to phone number via Twilio
def send_verification_sms(phone_number):
    verification_code = "123456"  # Default verification code
    # Set up Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your verification code is {verification_code}",
        from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio phone number
        to=phone_number
    )

# Function to send verification code to email
def send_verification_email(email):
    verification_code = "123456"  # Default verification code
    subject = "Your OTP Verification Code"
    message = f"Your verification code is {verification_code}"
    from_email = settings.EMAIL_HOST_USER  # Replace with your email
    send_mail(subject, message, from_email, [email])

# Function to send verification code to phone number via Twilio
def send_verification_sms(phone_number):
    verification_code = "123456"  # Default verification code
    # Set up Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your verification code is {verification_code}",
        from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio phone number
        to=phone_number
    )

def login_view(request):
    verification_code_sent = False
    code_verified = False
    contact = None
    verification_type = None  # Either 'email' or 'phone'
    
    if request.method == 'POST':
        contact = request.POST.get('contact')  # This could be email or phone number
        entered_code = request.POST.get('verification_code')  # Verification code entered by the user
        
        # Handle verification code submission
        if entered_code:
            if entered_code == request.session.get('verification_code'):
                code_verified = True
                messages.success(request, "Verification successful!")
                return redirect('ott_page')  # Redirect to the ott_page on successful verification
            else:
                messages.error(request, "Invalid verification code. Please try again.")
                # Even on failure, we want to show the verification section again
                verification_code_sent = True
                verification_type = request.session.get('verification_type')  # keep track of email or phone number
    
        # If no verification code entered, process the contact (email or phone)
        elif '@' in contact:  # It's an email
            try:
                validate_email(contact)  # Validate email format
                send_verification_email(contact)  # Send verification code to email
                request.session['verification_code'] = '123456'  # Store the verification code in session
                request.session['email'] = contact
                request.session['verification_type'] = 'email'
                verification_code_sent = True
                verification_type = 'email'  # Indicate that this is an email verification
                messages.success(request, "A verification code has been sent to your email.")
            except ValidationError:
                messages.error(request, "Invalid email address.")
        
        else:  # Assume it's a phone number
            # Validate phone number format using regex (e.g., for international phone numbers)
            phone_regex = r'^\+?[1-9]\d{1,14}$'  # E.164 format
            if re.match(phone_regex, contact):
                send_verification_sms(contact)  # Send verification code to phone number
                request.session['verification_code'] = '123456'  # Store the verification code in session
                request.session['phone_number'] = contact
                request.session['verification_type'] = 'phone'
                verification_code_sent = True
                verification_type = 'phone'  # Indicate that this is a phone verification
                messages.success(request, "A verification code has been sent to your phone.")
            else:
                messages.error(request, "Invalid phone number format.")
    
    return render(request, 'ott_subscription/login.html', {
        'verification_code_sent': verification_code_sent,
        'code_verified': code_verified,
        'contact': contact,
        'verification_type': verification_type
    })

# Verification view to verify the code entered by the user
def verify_email_view(request):
    if request.method == 'POST':

        print("call2")
        entered_code = request.POST.get('verification_code')

        # Check if entered code matches the session stored code for email
        if entered_code == request.session.get('verification_code'):
            messages.success(request, "Email verified successfully!")
            return redirect('ott_page')  # Redirect to the OTT page

        else:
            messages.error(request, "Invalid verification code. Please try again.")
    
    return render(request, 'ott_subscription/verify_email.html')

# Verification view to verify the code entered by the user for phone number
def verify_phone_view(request):
    if request.method == 'POST':
        entered_code = request.POST.get('verification_code')

        # Check if entered code matches the session stored code for phone number
        if entered_code == request.session.get('verification_code'):
            messages.success(request, "Phone number verified successfully!")
            return redirect('ott_page')  # Redirect to the OTT page

        else:
            messages.error(request, "Invalid verification code. Please try again.")
    
    return render(request, 'ott_subscription/verify_phone.html')


def logout_view(request):
    logout(request)
    return redirect('login')  

def get_skylink_plans(request):
    # Get the platform from query parameters (e.g., 'watcho')
    platform_to_check = request.GET.get('platform_id', '')

    # Step 1: Get the SkylinkPlan with id=1
    skylink_plan = SkylinkPlan.objects.filter(id=1).first()

    if skylink_plan:
        # Step 2: Get the OTT plans that match the platform
        ott_plans = OTTPlan.objects.filter(platform=platform_to_check)
        
        # Collect OTTPlan IDs for filtering
        ott_plan_ids = ott_plans.values_list('id', flat=True)
        
        # Step 3: Check which of the OTTPlans in the SkylinkPlan are part of the many-to-many relation
        # Filter out the matching OTTPlan instances that are connected to SkylinkPlan
        connected_ott_plans = skylink_plan.ott_plans.filter(id__in=ott_plan_ids)

        # Step 4: Prepare data to return
        plans_data = []
        
        if connected_ott_plans.exists():
            for ott_plan in connected_ott_plans:
                plans_data.append({
                    'id': ott_plan.id,
                    'code': ott_plan.code,
                    'name': ott_plan.name,
                    'platform': ott_plan.platform
                })
        else:
            plans_data = {'message': f"No matching OTT plans found for platform {platform_to_check}."}

        return JsonResponse({'plans': plans_data})

    else:
        # If SkylinkPlan with id=1 does not exist
        return JsonResponse({'error': 'SkylinkPlan with id=1 not found.'})