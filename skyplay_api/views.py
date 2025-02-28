import requests
import logging
from django.http import JsonResponse
from .models import APILog
import json
import requests

# Set up logger for error handling
logger = logging.getLogger(__name__)

# ✅ Fetch Client Name
def get_client_name(request, client_id):
    url = f"http://api.skyplay.in/clients/{client_id}"
    headers = {"Accept": "application/json", "Token": "84a0103ea1780372cbc410e49114633e"}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        # Assuming the response has "names" and you want the first one.
        client_name = data.get("names", [{}])[0].get("name", "Unknown Client")
        return JsonResponse({"client_name": client_name})
    
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ API request failed: {str(e)}")
        return JsonResponse({"error": "API Error"}, status=500)

# ✅ Fetch Channel Name
def get_channel_name(request, channel_id):
    url = f"http://api.skyplay.in/channels/{channel_id}"
    headers = {"Accept": "application/json", "Token": "84a0103ea1780372cbc410e49114633e"}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        # Assuming the response has "channels" and you want the first one.
        channel_name = data.get("channels", [{}])[0].get("name", "Unknown Channel")
        return JsonResponse({"channel_name": channel_name})
    
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ API request failed: {str(e)}")
        return JsonResponse({"error": "API Error"}, status=500)


def set_subscribe_to_channel(request, client_id, end_date, device_id, channel_id):
    url = f"http://api.skyplay.in/subscribeToChannel/{client_id}/{end_date}/{device_id}/{channel_id}"
    headers = {
        "Accept": "application/json",
        "Token": "84a0103ea1780372cbc410e49114633e",
        "Content-Type": "application/json"
    }
    payload = {}

    request_data = {
        "client_id": client_id,
        "end_date": end_date,
        "device_id": device_id,
        "channel_id": channel_id,
    }

    user = request.user if request.user.is_authenticated else None  # Capture logged-in user

    try:
        response = requests.patch(url, json=payload, headers=headers)
        response_data = response.json()
        
        status_code = response.status_code

        if response_data.get("result") == "ok":
            response_message = {"status": "success", "message": "Subscription successful"}
        else:
            response_message = {"status": "error", "message": response_data.get("errorText", "Unknown error")}

        # Save API log with user info
        APILog.objects.create(
            user=user,
            endpoint=url,
            request_data=json.dumps(request_data),
            response_data=json.dumps(response_data),
            status_code=status_code
        )

        logger.info(f"✅ API Request by {user}: {url} | Response: {response_message}")

        return JsonResponse(response_message, status=status_code)

    except requests.exceptions.RequestException as e:
        error_message = f"❌ API request failed: {str(e)}"
        logger.error(error_message)

        # Log error to database
        APILog.objects.create(
            user=user,
            endpoint=url,
            request_data=json.dumps(request_data),
            response_data=json.dumps({"error": str(e)}),
            status_code=500
        )

        return JsonResponse({"status": "error", "message": "API request failed"}, status=500)
