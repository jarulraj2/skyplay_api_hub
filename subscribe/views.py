import razorpay
import json
import logging
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from razorpay.errors import BadRequestError, SignatureVerificationError
from datetime import datetime
import requests
from django.utils.timezone import now
from .models import PaymentLog


# Setup logging
logger = logging.getLogger(__name__)

# ✅ Initialize Razorpay client (Replace with your actual keys)
RAZORPAY_KEY_ID = "YOUR_RAZORPAY_KEY_ID"
RAZORPAY_SECRET = "YOUR_RAZORPAY_SECRET"

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
def payment_view(request, clientId, endDate, deviceId, channelId):
    try:
        endDate = datetime.strptime(endDate, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Invalid date format"}, status=400)

    context = {
        "clientId": clientId,
        "clientName": get_client_name(clientId),
        "endDate": endDate,
        "deviceId": deviceId,
        "channelId": channelId,
        "channelName": get_channel_name(channelId)
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
        pack_or_channel_id = data.get("pack_or_channel_id", "Unknown")
        amount = int(data.get("amount", 0)) * 100
        currency = data.get("currency", "INR")

        if amount <= 0:
            return JsonResponse({"error": "Invalid amount"}, status=400)

        order = razorpay_client.order.create({
            "amount": amount,
            "currency": currency,
            "payment_capture": 1
        })

        request.session["razorpay_order_id"] = order["id"]

        # ✅ Log Payment Request & Response
        PaymentLog.objects.create(
            client_id=client_id,
            client_name=client_name,
            device_id=device_id,
            pack_or_channel_id=pack_or_channel_id,
            amount=amount / 100,  # Convert back to normal amount
            currency=currency,
            request_data=data,
            response_data=order
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
        pack_or_channel_id = data.get("pack_or_channel_id", "Unknown")
        amount = data.get("amount", 0)
        currency = data.get("currency", "INR")

        required_fields = ["razorpay_order_id", "razorpay_payment_id", "razorpay_signature"]

        if not all(data.get(field) for field in required_fields):
            logger.error("❌ Missing payment details")
            return JsonResponse({"error": "Missing payment details"}, status=400)

        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })

        # ✅ Log Payment Verification Request & Response
        PaymentLog.objects.create(
            client_id=client_id,
            client_name=client_name,
            device_id=device_id,
            pack_or_channel_id=pack_or_channel_id,
            amount=amount,
            currency=currency,
            request_data=data,
            response_data={"success": "Payment verified successfully"}
        )

        return JsonResponse({"success": "Payment verified successfully"})

    except SignatureVerificationError:
        logger.error("❌ Payment signature verification failed")
        return JsonResponse({"error": "Payment verification failed"}, status=400)
    
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f"❌ Error: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not razorpay_client:
        logger.error("❌ Razorpay client not initialized")
        return JsonResponse({"error": "Razorpay client not initialized"}, status=500)

    try:
        data = json.loads(request.body)
        client_id = data.get("client_id", "Unknown")
        client_name = data.get("client_name", "Unknown")
        required_fields = ["razorpay_order_id", "razorpay_payment_id", "razorpay_signature"]

        if not all(data.get(field) for field in required_fields):
            logger.error("❌ Missing payment details")
            return JsonResponse({"error": "Missing payment details"}, status=400)

        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })

        # ✅ Log Payment Verification Request & Response
        PaymentLog.objects.create(
            client_id=client_id,
            client_name=client_name,
            request_data=data,
            response_data={"success": "Payment verified successfully"}
        )

        return JsonResponse({"success": "Payment verified successfully"})

    except SignatureVerificationError:
        logger.error("❌ Payment signature verification failed")
        return JsonResponse({"error": "Payment verification failed"}, status=400)
    
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f"❌ Error: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)
    

# ✅ Success and Error Pages
def payment_success(request):
    return render(request, "success.html")

def payment_error(request):
    return render(request, "error.html")