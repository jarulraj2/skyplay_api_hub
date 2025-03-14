import razorpay
import json
import logging
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from razorpay.errors import BadRequestError, SignatureVerificationError
import requests
from django.utils.timezone import now
from .models import PaymentLog
import urllib.parse
import base64
import sys
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from channels.models import Channel  
from skyplay_api.views import set_subscribe_to_channel
from subscribe.models import Activation  # Import Activation model

# Setup logging
logger = logging.getLogger(__name__)

# ✅ Initialize Razorpay client (Replace with your actual keys)
RAZORPAY_KEY_ID = "rzp_test_qcFb099Pizad7S"
RAZORPAY_SECRET = "z2ZULiDyrWgcu6GVYILGmVbt"

if RAZORPAY_KEY_ID and RAZORPAY_SECRET:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))
else:
    razorpay_client = None
    logger.error("❌ Razorpay client not initialized. API keys are missing!")

# ✅ Fetch Client Name
def get_client_name(client_id):
    url = f"http://api.skyplay.in/clients/{client_id}"
    headers = {"Accept": "application/json", "Token": "84a0103ea1780372cbc410e49114633e"}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get("names", [{}])[0].get("name", "Unknown Client")
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ API request failed: {str(e)}")
        return "API Error"

# ✅ Fetch Channel Name
def get_channel_name(channel_id):
    url = f"http://api.skyplay.in/channels/{channel_id}"
    headers = {"Accept": "application/json", "Token": "84a0103ea1780372cbc410e49114633e"}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get("channels", [{}])[0].get("name", "Unknown Channel")
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ API request failed: {str(e)}")
        return "API Error"

# ✅ Payment Page
#def payment_view(request, clientId, endDate, deviceId, channelId, amount):
# def payment_view(request, encoded_data):
   
#         # First, URL decode the input
#     decoded_data = urllib.parse.unquote(encoded_data)
#     print("URL Decoded Data:", decoded_data)  # Debugging

#     # Fix padding and decode Base64
#     decoded_data = decode_base64(decoded_data)
#     if decoded_data is None:
#         return HttpResponse("Invalid Base64 encoding", status=400)

#     # Split and validate data
#     parts = decoded_data.split('|')
#     if len(parts) != 5:
#         return HttpResponse(f"Expected 5 values, got {len(parts)}", status=400)

#     # Assign values
#     clientId, endDate, deviceId, channelId, amount = parts
#     clientId, deviceId, channelId, amount = map(int, [clientId, deviceId, channelId, amount])

#     print(f"Parsed Data: clientId={clientId}, endDate={endDate}, deviceId={deviceId}, channelId={channelId}, amount={amount}")

#     clientId = int(clientId)
#     endDate = str(endDate)  # Explicitly setting it as string (optional, since it's already a string)
#     deviceId = int(deviceId)
#     channelId = int(channelId)
#     amount = int(amount)
#     try:
#         endDate = datetime.strptime(endDate, "%Y-%m-%d").date()
#     except ValueError:
#         return JsonResponse({"error": "Invalid date format"}, status=400)
    


#     # ✅ Validate Client
#     client_name = get_client_name(clientId)
#     # if not client_name:
#     #     return HttpResponseNotFound("❌ Client not found")

#     # ✅ Validate Channel
#     channel_name = get_channel_name(channelId)
#     # if not channel_name:
#     #     return HttpResponseNotFound("❌ Channel not found")

#     context = {
#         "clientId": clientId,
#         "clientName":client_name,
#         "endDate": endDate,
#         "deviceId": deviceId,
#         "channelId": channelId,
#         "channelName": channel_name,
#         "amount": amount,
#     }
#     return render(request, "payment.html", context)




# ✅ Payment Page
def payment_view(request):

    # Access query parameters from the URL
    channel_name = request.GET.get('channelName', None)
    clientId = request.GET.get('clientId', None)
    deviceId = request.GET.get('deviceId', None)
    channelId = request.GET.get('channelId', None)
    packs = request.GET.get('packs', None)


   # Calculate the end date (current date + 30 days)
    current_date = datetime.now()
    endDate = current_date + timedelta(days=30)

    channel = Channel.objects.filter(channel_id=channelId).first()  

    if channel:
        amount = channel.price
    else:
        amount = 1  # Default price when the channel does not exist

    print(f"Parsed Data: clientId={clientId}, endDate={endDate}, deviceId={deviceId}, channelId={channelId}, amount={amount}")

    clientId = int(clientId)
    #endDate = str(endDate)  # Explicitly setting it as string (optional, since it's already a string)
    deviceId = int(deviceId)
    channelId = int(channelId)
    amount = int(amount)
    try:
        # Format the endDate to string if needed (optional)
        endDate_str = endDate.strftime("%Y-%m-%d")  # Format as string for displaying
    except ValueError:
        return JsonResponse({"error": "Invalid date format"}, status=400)
    


    # ✅ Validate Client
    client_name = get_client_name(clientId)
    # if not client_name:
    #     return HttpResponseNotFound("❌ Client not found")

    # ✅ Validate Channel
    #channel_name = get_channel_name(channelId)
    # if not channel_name:
    #     return HttpResponseNotFound("❌ Channel not found")

    context = {
        "clientId": clientId,
        "clientName":client_name,
        "endDate": endDate,
        "deviceId": deviceId,
        "channelId": channelId,
        "channelName": channel_name,
        "amount": amount,
    }
    return render(request, "payment.html", context)


# ✅ Create Order
@csrf_exempt
def create_order(request):
 
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not razorpay_client:
        logger.error("❌ Razorpay client not initialized")
        return JsonResponse({"error": "Razorpay client not initialized"}, status=500)
  
    try:
        data = json.loads(request.body)
        client_id = data.get("client_id", "Unknown")
        client_name = data.get("client_name", "Unknown")
        device_id = data.get("device_id", "Unknown")
        channel_id = data.get("channel_id", "Unknown")
        amount = int(data.get("amount", 0)) * 100
        currency = data.get("currency", "INR")

        if amount <= 0:
            return JsonResponse({"error": "Invalid amount"}, status=400)

        order = razorpay_client.order.create({
            "amount": amount,
            "currency": currency,
            "payment_capture": 1,
            'notes': {
                'company_name': 'SkyPlay APIs'  # You can add the company name here if needed
            },
        })

        request.session["razorpay_order_id"] = order["id"]

        # ✅ Log Payment Request & Response
        PaymentLog.objects.create(
            client_id=client_id,
            client_name=client_name,
            device_id=device_id,
            pack_or_channel_id=channel_id,
            amount=amount / 100,  # Convert back to normal amount
            currency=currency,
            order_id=order["id"],
            request_data=data,
            response_data=order,
            status="ORDER_CREATED",
            final_status="PENDING"
        )

        return JsonResponse({
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"]
        })
    
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON Decode Error: {str(e)}")
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    except BadRequestError as e:
        logger.error(f"❌ Razorpay API Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=400)
    
    except Exception as e:
        logger.error(f"❌ Unexpected Error: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)

# ✅ Verify Payment
@csrf_exempt
def verify_payment(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not razorpay_client:
        logger.error("❌ Razorpay client not initialized")
        return JsonResponse({"error": "Razorpay client not initialized"}, status=500)

    try:
        data = json.loads(request.body)
        client_id = data.get("client_id", "Unknown")
        client_name = data.get("client_name", "Unknown")
        device_id = data.get("device_id", "Unknown")
        channel_id = data.get("channel_id", "Unknown")
        amount = data.get("amount", 0)
        currency = data.get("currency", "INR")
        end_date = data.get("end_date", "Unknown")

        required_fields = ["razorpay_order_id", "razorpay_payment_id", "razorpay_signature"]

        if not all(data.get(field) for field in required_fields):
            logger.error("❌ Missing payment details")
            return JsonResponse({"error": "Missing payment details"}, status=400)

        result =  razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })
      
        # need to call the channel activate api 
        # ✅ Update or Create Payment Log
        payment_log, created = PaymentLog.objects.update_or_create(
            order_id=data["razorpay_order_id"],  # Lookup field
            defaults={               
                "varified_resonse": data,  # ✅ Store verification response
                "status": "PAYMENT_VERIFIED",
                "final_status": "SUCCESS",
            }
        )




        # Parse the date string to a datetime object
        endDate_obj = datetime.fromisoformat(end_date)  # Convert the ISO format to datetime

        # Now format it into the desired format (YYYY-MM-DD)
        end_date = endDate_obj.strftime('%Y-%m-%d')  # This gives '2025-04-09'

        # Proceed with the API request or whatever logic you need
        print(f"Formatted endDate: {end_date}")



        # Call the set_subscribe_to_channel function
        set_subscribe_to_channel(request, client_id, end_date, device_id, channel_id)

        activation = Activation.objects.create(
            client_id=client_id,
            channel_id=channel_id,
            end_date=end_date,
            device_id=device_id
        )

        return JsonResponse({"success": "Payment verified successfully"})

    except SignatureVerificationError:
        logger.error("❌ Payment signature verification failed")
        # ✅ Update Payment Log for Failed Verification
        PaymentLog.objects.update_or_create(
            order_id=data.get("razorpay_order_id", ""),
            defaults={"status": "SIGNATURE_VERIFICATION_FAILED", "final_status": "FAILED"}
        )
        return JsonResponse({"error": "Payment verification failed"}, status=400)
    
    except BadRequestError as e:
        logger.error(f"❌ Razorpay API Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=400)

    except Exception as e:
        logger.error(f"❌ Unexpected Error: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)

   
    

# ✅ Success and Error Pages
def payment_success(request):
    return render(request, "success.html")

def payment_error(request):
    return render(request, "error.html")




def activation(request):
    # Get the values from the URL query string
    name = request.GET.get('name', None)  # Name parameter (e.g., 'America HD / test')
    client_id = request.GET.get('clientId', None)  # Client ID
    device_id = request.GET.get('deviceId', None)  # Device ID
    channel_id = request.GET.get('channelId', None)  # Channel ID

    # Pass all these values to the template for display
    return render(request, 'activation.html', {
        'name': name,
        'client_id': client_id,
        'device_id': device_id,
        'channel_id': channel_id
    })


