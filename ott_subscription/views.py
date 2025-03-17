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
from .models import SkylinkPlan, OTTPlan, OTTSubscription, OTTActivationLog
from django.http import JsonResponse
import json
import requests

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
    contact = ""
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
                # For each OTTPlan, fetch the associated OTTs
                associated_otts = ott_plan.otts.all()  # This fetches the related OTTS
                
                # Prepare a list of OTT details
                otts_data = []
                for ott in associated_otts:
                    image_url = ott.image.url if ott.image else 'default_image_url'  # Replace 'default_image_url' with an actual default image if needed
                    otts_data.append({
                        'id': ott.id,
                        'name': ott.name,
                        'code': ott.code,
                        'is_active': ott.is_active,
                        'image': image_url 
                    })

                # Append OTTPlan data along with its associated OTTs
                plans_data.append({
                    'id': ott_plan.id,
                    'code': ott_plan.code,
                    'name': ott_plan.name,
                    'platform': ott_plan.platform,
                    'otts': otts_data  # List of OTTs associated with this plan
                })
        else:
            plans_data = {'message': f"No matching OTT plans found for platform {platform_to_check}."}

        return JsonResponse({'plans': plans_data})

    else:
        # If SkylinkPlan with id=1 does not exist
        return JsonResponse({'error': 'SkylinkPlan with id=1 not found.'})
    




def ott_activation(request):
    try:
        # Get the data from the request body
        data = json.loads(request.body)
        client_id = data.get('client_id')
        platform_id = data.get('platform_id')
        plan_id = data.get('plan_id')

        # Process the subscription (add your subscription logic)
        # Assuming you have a Subscription model where you save this data
        subscription = OTTSubscription.objects.create(
            client_id=client_id,
            platform_id=platform_id,
            plan_id=plan_id,
        )
        """
        Returns platform-specific data or performs a platform-specific action.
        """

        if platform_id == 'watcho':
            platform_data = fetch_watcho_data(request)
        elif platform_id == 'play_box':
            platform_data = fetch_playbox_data(request)
        elif platform_id == 'hotstar':
            platform_data = fetch_hotstar_data(request)
        elif platform_id == 'ottplay':
            platform_data = fetch_ottplay_data(request)
        elif platform_id == 'tatabinge':
            platform_data = fetch_tatabinge_data(request)
        else:
            # If platform_id is invalid, return an error or handle the case
            platform_data = None

        
        # Log the OTT activation in the OTTActivationLog
        OTTActivationLog.objects.create(
            client_id=client_id,
            platform_id=platform_id,
            plan_id=plan_id,
            status='Success',  # Assuming the activation was successful
            message='Activation successful',
        )

        # Return a success response
        return JsonResponse({"success": True, "message": "Subscription activated successfully!"})

    except Exception as e:
        # Log the failure if an exception occurs
        OTTActivationLog.objects.create(
            client_id=client_id,
            platform_id=platform_id,
            plan_id=plan_id,
            status='Failure',
            message=str(e),
        )

        return JsonResponse({"success": False, "message": str(e)})
    
    

def fetch_watcho_data(request):
 # The API endpoint
    url = "https://beta2-publicapis.dishtv.in/api/WatchoOne/SubscriptionRequestWatchoplan"
    
    # The headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": "••••••"  # Replace with the actual authorization token
    }
    
    # The data you want to send in the request
    data = {
        "InputData": "rkm1KdqGcA8KsYuZElhieCcEeA2VUQg5Kw3+Cw++kogzYmoyPyhEZP85eIZD1Zi+6McbhfD6sBt4JJz4PM1Bp120bgQDEAnBh/eGi9IaX6IS+pG4HdXPd8SPf6H5KxFrHQG5r+ckdthKQP4dH+kYACHi+OFgUgyf74C1LlQ7LsGcrwaVmUxh5ejHG4Xw+rAbmce6SZIK+A+Xq/Hz4MC7nLlvVJc2Um7Y"
    }

    try:
        # Ensure UTF-8 encoding
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')

        # Make the POST request to the external API
        response = requests.post(url, headers=headers, data=json_data)

        # Check if the request was successful
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        else:
            return JsonResponse({'error': 'Request failed', 'status_code': response.status_code}, status=response.status_code)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def fetch_playbox_data(request):
    # The API URL from the request
    api_url = "https://8fjpx02rmk.execute-api.ap-south-1.amazonaws.com/prod/v3/assignPack"

    # Define the headers
    headers = {
        'x-api-key': 'spfFnjetet705D8sngf7H7kojE04oYkn7DNECvDv',
        'Content-Type': 'application/json',
    }

    # Prepare the JSON payload
    data = {
        "phone": "9715121791",  # Make sure phone number is valid as per API specs
        "partnerKey": "8588f445e9a912e828597d43702aa89aaceacbe149db175366ca95bab1e31ebb85e191e7484116fc2de11b9d9247b5f03786ed689c53716a5a0cdc4280019887",  # Double-check partner key
        "packCode": "4517369",
    }

    try:
        # Make the POST request to the API
        response = requests.post(api_url, json=data, headers=headers)

        print("Status Code:", response.status_code)
        print("Response Content:", response.text)  # Print out the entire response body

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the response JSON as a Django JsonResponse
            return JsonResponse(response.json())
        else:
            # If something went wrong, return an error message
            return JsonResponse({'error': 'Failed to fetch packs', 'status_code': response.status_code})
    except requests.exceptions.RequestException as e:
        # If an error occurs while making the request, return an error message
        return JsonResponse({'error': str(e)})
    


def fetch_ottplay_data(request):
    # The URL of the API you want to send the POST request to
    api_url = 'https://stg-partners.ottplay.com/api/v4.0/subscriber/action'
    
    # The payload to be sent in the request body (data)
    payload = {
        "mode": "CREATE_ACTIVATE",
        "oper_code": "10276",
        "login_id": "skylink_testISP",
        "phone": "9715121790",
        "email": "arul@gmail.com",
        "first_name": "Jon",
        "last_name": "Doe",
        "address": "subscriber address",
        "plan_code": "ottplay_monthly_test",
        "use_alt_lco_code": 0,
        "partner_reference_id": "",
        "zone": "",
        "service_number": "",
        "state_code": "",
        "subscription_type": "",
        "subscription_id": ""
    }
    
    # Headers to be included in the request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'fRGcemrfodXg5OBXh6JDJ79MNab7QSbOxlnAlmL8VvRdCNSVBdfiHmSzwvcQ24pDOPtBD2rPu8LrU0S1gOlGZ2iegAPpEKXuvIb9b3ctf3dAQStqGuNRfZYZHEwpzontQQhrmd0EixJ1378ss7sBRonQfceHO6Jyj6La8EODIymMyqhNWURo9zlUZIDjgn19rJCfNVn42nL7OA4zSqTgsA1uyy8nVx7C89l8imSpYvs8E70uqeUzAfo3w9EUpP1',  # Replace with actual authorization token
    }

    # Send the POST request with the JSON payload and headers
    response = requests.post(api_url, json=payload, headers=headers)
    print(response)
    # Check the response status code
    if response.status_code == 200:
        # Successfully received a response from the API
        # You can return the JSON response or any data you need
        return JsonResponse(response.json(), status=200)
    else:
        # Handle error if the response is not successful
        return JsonResponse({'error': 'Failed to make the API call', 'details': response.text}, status=response.status_code)


def fetch_tatabinge_data(request):
    # Your logic to fetch data for 'tatabinge' platform
    return {"platform": "tatabinge", "data": "TataBinge specific data"}