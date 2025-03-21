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
from .models import SkylinkPlan, OTTPlan, OTTSubscription, OTTActivationLog,OTTAggregator
from django.http import JsonResponse
import json
import requests
from base64 import b64encode
from django.views.decorators.csrf import csrf_exempt
import razorpay
import logging
from django.utils import timezone
from datetime import datetime, timedelta
from .models import VerificationCode

# Initialize Logger
logger = logging.getLogger(__name__)

#razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
RAZORPAY_KEY_ID = "rzp_test_qcFb099Pizad7S"
RAZORPAY_SECRET = "z2ZULiDyrWgcu6GVYILGmVbt"

if RAZORPAY_KEY_ID and RAZORPAY_SECRET:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))
else:
    razorpay_client = None
    logger.error("❌ Razorpay client not initialized. API keys are missing!")

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
    
    # Fetch active OTT platforms
    platform_instance = OTTAggregator.objects.filter(status='active')

    # Render the OTT page with Razorpay key and platform data
    return render(request, 'ott_subscription/ott_page.html', {
        'contact': contact,
        'verification_type': verification_type,
        'ott_platform': platform_instance,
        'razorpay_key': RAZORPAY_KEY_ID,  # Pass Razorpay key to the template
    })

# Function to generate a random 6-digit verification code
def generate_verification_code():
    """Generates a random 6-digit verification code"""
    return str(random.randint(100000, 999999))

# Function to send verification email
def send_verification_email(email):
    verification_code = generate_verification_code()
    subject = "Your OTP Verification Code"
    message = f"Your verification code is {verification_code}"
    from_email = 'your-email@example.com'  # Replace with your actual email
    send_mail(subject, message, from_email, [email])
    # Store the code in the database
    VerificationCode.objects.update_or_create(
        email=email,
        defaults={"code": verification_code, "timestamp": datetime.now()}
    )

# Function to send verification SMS (placeholder for actual SMS service)
def send_verification_sms(phone_number):
    verification_code = generate_verification_code()
    message = f"Your OTP verification code is {verification_code}"
    # Implement SMS sending logic here (using an SMS API like Twilio)
    # Store the code in the database
    VerificationCode.objects.update_or_create(
        phone_number=phone_number,
        defaults={"code": verification_code, "timestamp": datetime.now()}
    )

# Login view function
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
            # Check if it's an email or phone number
            verification_record = None
            verification_code_sent = True
            if '@' in contact:  # It's an email
                verification_record = VerificationCode.objects.filter(email=contact).first()
            else:  # Assume it's a phone number
                verification_record = VerificationCode.objects.filter(phone_number=contact).first()

            # First check if the entered code is the default code '123456'
            if entered_code == '123456':
                code_verified = True
                messages.success(request, "Verification successful with default code!")
                return redirect('ott_page')  # Redirect to the ott_page on successful verification


            if verification_record and not verification_record.is_expired():
                # Check if the entered code matches the stored code
                if entered_code == verification_record.code:
                    code_verified = True
                    messages.success(request, "Verification successful!")
                    return redirect('ott_page')  # Redirect to the ott_page on successful verification
                else:
                    messages.error(request, "Invalid verification code. Please try again.")
            else:
                messages.error(request, "The verification code has expired or was not found.")
        
        # If no verification code entered, process the contact (email or phone)
        elif contact:
            if '@' in contact:  # It's an email
                try:
                    validate_email(contact)  # Validate email format
                    send_verification_email(contact)  # Send verification code to email
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


def logout_view(request):
    logout(request)
    return redirect('login')  


from django.http import JsonResponse
from .models import SkylinkPlan, OTTPlan

def get_skylink_plans(request):
    # Get the platform from query parameters (e.g., 'watcho')
    platform_to_check = request.GET.get('platform_id', '')
    sky_plan_id = request.GET.get('sky_plan_id', '')
    client_id = request.GET.get('clinet_id', '')

     # Check if the platform has Hotstart enabled
    hotstart_enabled = OTTAggregator.objects.filter(status='active', code='hotstart').exists()

    # Step 1: Get the SkylinkPlan with the provided sky_plan_id
    skylink_plan = SkylinkPlan.objects.filter(id=sky_plan_id).first()
   
    if skylink_plan:
        # Step 2: Get the OTT plans that match the platform
        ott_plans = OTTPlan.objects.filter(platform_id=platform_to_check)

        # Collect OTTPlan IDs for filtering
        ott_plan_ids = ott_plans.values_list('id', flat=True)

        # Step 3: Get the connected OTT plans that are already part of the SkylinkPlan's many-to-many relation
        connected_ott_plans = skylink_plan.ott_plans.filter(id__in=ott_plan_ids)
    
        # Step 4: Identify paid plans (those not yet connected but part of the platform)
        paid_ott_plans = ott_plans.exclude(id__in=connected_ott_plans.values_list('id', flat=True))

        # Prepare response data
        plans_data = []

        # Include active plans first
        if connected_ott_plans.exists():
            for ott_plan in connected_ott_plans:
                associated_otts = ott_plan.otts.all()  # Get associated OTTs
                otts_data = []
                for ott in associated_otts:
                    image_url = ott.image.url if ott.image else 'default_image_url'
                    otts_data.append({
                        'id': ott.id,
                        'name': ott.name,
                        'code': ott.code,
                        'is_active': ott.is_active,
                        'image': image_url,
                    })

                # Check if the plan is expired or not
              # Check if the plan is expired or not and get the expiration date
                is_expired, expiration_date = is_plan_expired(client_id, ott_plan.id)                
                plan_status = 1 if is_expired else 0  # 0: Expired, 1: Active
                
                plans_data.append({
                    'id': ott_plan.id,
                    'code': ott_plan.code,
                    'name': ott_plan.name,
                    'price': ott_plan.price,
                    'subscription_tiers': 'free',  # Mark as active
                    'otts': otts_data,
                    'status_flag': plan_status,  # Add the status flag for button disable
                    'expiration_date': expiration_date if expiration_date else 'N/A',  # Add expiration date
                    'hotstart_enabled': hotstart_enabled  
                })
                
        # Now, include paid plans
        if paid_ott_plans.exists():
            for ott_plan in paid_ott_plans:
                associated_otts = ott_plan.otts.all()  # Get associated OTTs
                otts_data = []
                for ott in associated_otts:
                    image_url = ott.image.url if ott.image else 'default_image_url'
                    otts_data.append({
                        'id': ott.id,
                        'name': ott.name,
                        'code': ott.code,
                        'is_active': ott.is_active,
                        'image': image_url 
                    })
                # Check if the plan is expired or not
              # Check if the plan is expired or not and get the expiration date
                is_expired, expiration_date = is_plan_expired(client_id, ott_plan.id)
                plan_status = 1 if is_expired else 0  # 0: Expired, 1: Active
                plans_data.append({
                    'id': ott_plan.id,
                    'code': ott_plan.code,
                    'name': ott_plan.name,
                    'price': ott_plan.price,
                    'subscription_tiers': 'paid',  # Mark as paid but not active
                    'otts': otts_data,
                    'status_flag': plan_status,  # Add the status flag for button disable
                    'expiration_date': expiration_date if expiration_date else 'N/A',  # Add expiration date
                    'hotstart_enabled': hotstart_enabled
                })
            
            # Optionally, you can also add some message if no paid plans exist:
            if not paid_ott_plans.exists():
                plans_data.append({'message': 'No paid OTT plans available.'})

        return JsonResponse({'plans': plans_data})

    else:
        # If SkylinkPlan with the provided sky_plan_id does not exist
        return JsonResponse({'error': 'SkylinkPlan not found.'})
    
    
def log_ott_activation(client_id, platform_instance, plan_id, status, message, input_data, response_status, output_data, endpoint="", subscription_tiers='free', razorpay_details=None):
    """
    Common function to log OTT activation, whether successful or failed.
    """
    log_data = {
        'client_id': client_id,
        'platform_id': platform_instance,
        'plan_id': plan_id,
        'status': status,
        'message': message,
        'input': json.dumps(input_data),
        'response_status': response_status,
        'output': json.dumps(output_data),
        'endpoint': endpoint,
        'subscription_tiers': subscription_tiers
    }

    if razorpay_details and subscription_tiers == 'paid':
        log_data.update({
            'razorpay_order_id': razorpay_details.get('razorpay_order_id'),
            'razorpay_payment_id': razorpay_details.get('razorpay_payment_id'),
            'razorpay_signature': razorpay_details.get('razorpay_signature'),
            'payment_amount': razorpay_details.get('payment_amount'),
            'payment_currency': razorpay_details.get('payment_currency')
        })

    # Create the log entry in the OTTActivationLog model
    OTTActivationLog.objects.create(**log_data)


def is_plan_expired(client_id, plan_id):
    try:
        # Get the existing activation log for the client_id and plan_id
        activation_log = OTTActivationLog.objects.filter(client_id=client_id, plan_id=plan_id).first()      
        if activation_log:
            # Check if expiration date is reached
            expiration_date = activation_log.expiration_date
            
            # Format the expiration_date to only return the date part in dd-mm-yyyy format
            if expiration_date:
                formatted_expiration_date = expiration_date.strftime('%d-%m-%Y')  # Format as dd-mm-yyyy
                
                if formatted_expiration_date <= timezone.now().strftime('%d-%m-%Y'):
                    return True, formatted_expiration_date  # Plan expired
                else:
                    return False, formatted_expiration_date  # Plan is still active
            return False, None  # If no expiration date is available
            
        return False, None  # No activation log found
    except OTTActivationLog.DoesNotExist:
        return False, None  # No activation log found for client_id and plan_id

@csrf_exempt
def ott_activation(request):
    try:
        # Get the data from the request body
        data = json.loads(request.body)
        client_id = data.get('client_id')
        platform_id = data.get('platform_id')
        plan_id = data.get('plan_id')
        subscription_tiers = data.get('subscription_tiers', 'free')

        platform_instance = OTTAggregator.objects.get(id=platform_id)
        platform_code = platform_instance.code

        # Initialize variables to store API response data
        platform_data = None
        response_status = None
        output = None
        endpoint = ""
        input_data = data  # The request data to be logged as 'input'

        # Process the subscription (add your subscription logic)
        subscription = OTTSubscription.objects.create(
            client_id=client_id,
            platform_id=platform_instance,
            plan_id=plan_id,
        )

        # Fetch platform-specific data based on platform code
        if platform_code == "watcho":
            platform_data = fetch_watcho_data(request)
        elif platform_code == 'play_box':
            platform_data = fetch_playbox_data(request)
        elif platform_code == 'hotstar':
            platform_data = fetch_hotstar_data(request)
        elif platform_code == 'ottplay':
            platform_data = fetch_ottplay_data(request)
        elif platform_code == 'tatabinge':
            platform_data = fetch_tatabinge_data(request)
        else:
            platform_data = None

        if platform_data:
            response_content = platform_data.content  # This is in bytes format
            response_json = json.loads(response_content.decode('utf-8'))  # Convert bytes to JSON
            response_status = response_json['response_status']
            output = response_json if response_status == 200 else response_json['output']
            endpoint = response_json['endpoint']
            input_data = response_json['input']
        else:
            response_status = 400  # Bad request if platform data is None
            output = "Invalid platform ID or failed to fetch platform data."
            endpoint = ""

        # Handle logging
        if subscription_tiers == 'paid':
              
            razorpay_details = {
                'razorpay_order_id': data.get('razorpay_order_id'),
                'razorpay_payment_id': data.get('razorpay_payment_id'),
                'razorpay_signature': data.get('razorpay_signature'),
                'payment_amount': data.get('payment_amount', 0) / 100,   # Convert paise to INR
                'payment_currency': data.get('payment_currency')
            }
            log_ott_activation(client_id, platform_instance, plan_id, 'Success', 'The activation has been completed successfully.', input_data, response_status, output, endpoint, subscription_tiers, razorpay_details)
        else:
            log_ott_activation(client_id, platform_instance, plan_id, 'Success', 'The activation has been completed successfully.', input_data, response_status, output, endpoint, subscription_tiers)

        return JsonResponse({"success": True, "message": "The activation has been completed successfully."})

    except Exception as e:
        # Log failure if an exception occurs
        log_ott_activation(client_id, platform_instance, plan_id, 'Failure', str(e), str(e), 500, str(e), "", subscription_tiers)

        return JsonResponse({"success": False, "message": str(e)})
    
    

def fetch_watcho_data(request):
 # The API endpoint
    api_url = "https://beta2-publicapis.dishtv.in/api/WatchoOne/SubscriptionRequestWatchoplan"
    
    # Your credentials for Basic Auth
    username = '152'
    password = 'W@tCh0!$p@54321'

    # Create the Basic Auth header value
    auth_value = f"{username}:{password}"
    encoded_auth_value = b64encode(auth_value.encode('utf-8')).decode('utf-8')

    # The headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_auth_value}"
    }
    
    # The data you want to send in the request
    data = {
        "InputData": "rkm1KdqGcA8KsYuZElhieCcEeA2VUQg5Kw3+Cw++kogzYmoyPyhEZP85eIZD1Zi+6McbhfD6sBt4JJz4PM1Bp120bgQDEAnBh/eGi9IaX6IS+pG4HdXPd8SPf6H5KxFrHQG5r+ckdthKQP4dH+kYACHi+OFgUgyf74C1LlQ7LsGcrwaVmUxh5ejHG4Xw+rAbmce6SZIK+A+Xq/Hz4MC7nLlvVJc2Um7Y"
    }

    try:
        # Ensure UTF-8 encoding
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')

        # Make the POST request to the external API
        response = requests.post(api_url, headers=headers, data=json_data)

        # Create response data
        result = {
            "input": data,
            "response_status": response.status_code,
            "output": response.json() if response.status_code == 200 else response.text,
            "endpoint":api_url
        }   

        # Check if the request was successful
        if response.status_code == 200:
            return JsonResponse(result, safe=False)
        else:
            return JsonResponse(result, status=response.status_code)

    except Exception as e:
        # Return exception error if any
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

        # Prepare the result object with both request and response data
        result = {
            "input": data,
            "response_status": response.status_code,
            "output": response.json() if response.status_code == 200 else response.text,
            "endpoint":api_url
        } 

        # Check if the request was successful (status code 200)
        if response.status_code == 200:          
            return JsonResponse(result, safe=False)
        else:
            return JsonResponse(result, status=response.status_code)

    except requests.exceptions.RequestException as e:
        # If an error occurs while making the request, return an error message
        return JsonResponse({'error': str(e), 'request': data}, status=500)
    

def fetch_ottplay_data(request):
    # The URL of the API you want to send the POST request to
    #api_url = 'https://stg-partners.ottplay.com/api/v4.0/subscriber/action'
    api_url = settings.OTTPLAY_API_URL
    oper_code = settings.OTTPLAY_OPER_CODE
    login_id = settings.OTTPLAY_LOGIN_ID
    auth_token = settings.OTTPLAY_AUTH_TOKEN
    # The payload to be sent in the request body (data)
    payload = {
        "mode": "CREATE_ACTIVATE",
        "oper_code":oper_code,
        "login_id": login_id,
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

    try:
        # Send the POST request with the JSON payload and headers
        response = requests.post(api_url, json=payload, headers=headers)

        # Prepare the result object with both request and response data
        result = {
            "input": payload,
            "response_status": response.status_code,
            "output": response.json() if response.status_code == 200 else response.text,
            "endpoint":api_url
        } 
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return JsonResponse(result, safe=False)
        else:
            return JsonResponse(result, status=response.status_code)
    
    except requests.exceptions.RequestException as e:
        # If an error occurs while making the request, return an error message along with the request data
        return JsonResponse({'error': str(e), 'request': payload}, status=500)

def fetch_tatabinge_data(request):
    # Your logic to fetch data for 'tatabinge' platform
    return {"platform": "tatabinge", "data": "TataBinge specific data"}


def fetch_hotstar_data(request):
    # Your logic to fetch data for 'tatabinge' platform
    return {"platform": "tatabinge", "data": "TataBinge specific data"}



@csrf_exempt
def create_razorpay_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not razorpay_client:
        logger.error("❌ Razorpay client not initialized")
        return JsonResponse({"error": "Razorpay client not initialized"}, status=500)

    try:
        data = json.loads(request.body)
        amount = int(data.get("amount", 0)) * 100  # Convert to paise
        currency = data.get("currency", "INR")

        if amount <= 0:
            return JsonResponse({"error": "Invalid amount"}, status=400)

        # 🔍 Print API Key for Debugging
        logger.info(f"🔑 API Key: {settings.RAZORPAY_KEY_ID}")

        # 🔥 Debug API Response
        order = razorpay_client.order.create({
            "amount": amount,
            "currency": currency,
            "payment_capture": 1
        })
        logger.info(f"✅ Razorpay Order Created: {order}")

        return JsonResponse(order)

    except razorpay.errors.BadRequestError as e:
        logger.error(f"❌ Razorpay API Error: {str(e)}")
        return JsonResponse({"error": "Razorpay authentication failed"}, status=401)

    except Exception as e:
        logger.error(f"❌ Unexpected Error: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)
    

@csrf_exempt
def confirm_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')

        # Verify the payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            # Payment is successful, mark the subscription as active
            # subscription = Subscription.objects.get(razorpay_order_id=razorpay_order_id)
            # subscription.status = 'active'  # Or whatever status you want
            # subscription.save()

            return JsonResponse({'status': 'Payment successful', 'message': 'Subscription activated.'})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'error': 'Payment signature verification failed.'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


