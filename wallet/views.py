import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Wallet, WalletTransaction
from django.views.decorators.csrf import csrf_exempt
import logging
import json
import sys
from decimal import Decimal 

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

@login_required
def wallet_view(request):
    
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    user_id = request.user.id  
    # Fetch the wallet transactions for the logged-in user
    transactions = WalletTransaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'wallet/wallet.html', {'wallet': wallet, 'razorpay_key': RAZORPAY_KEY_ID, 'user_id': user_id ,  'transactions': transactions})


@csrf_exempt
def add_money(request):
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



@login_required
@csrf_exempt
def verify_payment(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        logger.info(f"🔍 Payment Verification Data: {data}")

        # Extract payment details
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")

        if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
            raise ValueError("Missing required payment details")

        result = razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

        # Fetch the order details from Razorpay
        order_details = razorpay_client.order.fetch(razorpay_order_id)
        amount = order_details.get("amount", 0) / 100  # Convert paise to INR

        if amount == 0:
            raise ValueError("Invalid order amount fetched from Razorpay")

        # Update Wallet balance
        wallet, created = Wallet.objects.get_or_create(user_id=request.user)
        wallet.balance += Decimal(amount)  # Ensure the amount is in Decimal format
        wallet.save()

        # Create a new WalletTransaction record
        transaction = WalletTransaction(
            user=request.user,
            amount=amount,
            transaction_type='credit',  # 'credit' because the wallet balance is increasing
            balance_after_transaction=wallet.balance,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            razorpay_order_id=razorpay_order_id,
            payment_verified=True
        )

        try:
            transaction.save()
            logger.info(f"Transaction saved successfully: {transaction}")
        except Exception as e:
            logger.error(f"Error saving transaction: {str(e)}")
            return JsonResponse({"error": "Error saving transaction record"}, status=500)

        # Return success response
        return JsonResponse({"message": "Payment verified and wallet updated successfully."}, status=200)

    except razorpay.errors.SignatureVerificationError as e:
        logger.error(f"Razorpay Signature Verification Failed: {str(e)}")
        return JsonResponse({"error": "Payment signature verification failed."}, status=400)
    
    except ValueError as e:
        logger.error(f"Validation Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=400)
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")


# ✅ Success and Error Pages
def payment_success(request):
    return render(request, "wallet/success.html")

def payment_error(request):
    return render(request, "wallet/error.html")