# views.py
from django.shortcuts import render
from django.views import View
from .utils import encrypt, decrypt  # Assuming you have these functions in utils.py
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EncryptionSerializer, DecryptionSerializer, SubscriptionPlanDetailsSerializer
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
import requests
import base64
from requests.auth import HTTPBasicAuth
from base64 import b64encode

class EncryptionDecryptionView(View):
    def get(self, request):
        return render(request, 'admin/watcho/enc_dec.html')  # Render an initial empty form

    def post(self, request):
        plain_text = request.POST.get('plain_text')
        encrypted_text = request.POST.get('encrypted_text')
        result_text = None
        action = None

        # Handle encryption
        if plain_text:
            pass_phrase = 'Pas$Phra$e-38429048'  # Use a secure passphrase
            encrypted_text = encrypt(plain_text, pass_phrase)
            result_text = encrypted_text
            action = 'Encrypt'

        # Handle decryption
        elif encrypted_text:
            pass_phrase = 'Pas$Phra$e-38429048'  # Same passphrase used for encryption
            decrypted_text = decrypt(encrypted_text, pass_phrase)
            result_text = decrypted_text
            action = 'Decrypt'

        # Return the template with the result of encryption or decryption
        return render(request, 'admin/watcho/enc_dec.html', {
            'plain_text': plain_text,
            'encrypted_text': encrypted_text,
            'result_text': result_text,
            'action': action
        })

# Encryption API View
class EncryptionAPI(APIView):
    @csrf_exempt
    @swagger_auto_schema(request_body=EncryptionSerializer)
    def post(self, request):
        # Pass request data to serializer for validation
        serializer = EncryptionSerializer(data=request.data)
        if serializer.is_valid():
            plain_text = serializer.validated_data.get('plain_text')

            # Now plain_text is already a dictionary, no need to decode it
            if isinstance(plain_text, dict):
                pass_phrase = 'p2s5v8y/B?E(H+Kb'  # Use your passphrase securely
                encrypted_text = encrypt(json.dumps(plain_text), pass_phrase)  # Encrypt the dictionary as a string
                
                return Response({"encrypted_text": encrypted_text}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "plain_text must be a valid JSON object."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DecryptionAPI(APIView):
    @csrf_exempt
    @swagger_auto_schema(request_body=DecryptionSerializer)
    def post(self, request):
        serializer = DecryptionSerializer(data=request.data)
        if serializer.is_valid():
            encrypted_text = serializer.validated_data.get('encrypted_text')
            pass_phrase = 'p2s5v8y/B?E(H+Kb'
            decrypted_text = decrypt(encrypted_text, pass_phrase)
            return Response({"decrypted_text": decrypted_text}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SubscriptionPlanDetailsAPI(APIView):
    def get(self, request):
        # Your API username and password
        username = '152'
        password = 'W@tCh0!$p@54321'

        # Encode the username and password into Base64
        auth_string = f"{username}:{password}"
        base64_auth = b64encode(auth_string.encode('utf-8')).decode('utf-8')

        # API URL
        url = "https://beta2-publicapis.dishtv.in/api/WatchoOne/SubscriptionPlanDetails/"

        # Prepare headers with the Authorization header
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {base64_auth}'  # Add the Authorization header with Base64 encoded username and password
        }

        # Prepare the payload (same as the data you're sending in Postman)
        payload = {
            "InputData": "Tx6oLLb1SBxTAhShSb2t7T1jviEaHPhH4kC2B6OKjb8FMd4uvahsOeubCrvvxgdp7kBWCh19Jfb1Fl/HlPc1xxeskUcP+P+KuW9UlzZSbtg="
        }

        # Make the POST request to the external API using Basic Authentication
        try:
            # Send the request with Basic Authentication
            response = requests.post(
                url,
                json=payload,  # This automatically serializes the payload to JSON
                headers=headers  # This sends the Authorization header
            )           

            # Check the response status
            if response.status_code == 200:
                return Response({
                    "message": "Successfully fetched subscription plans",
                    "response": response.json()  # Parse the JSON response from the external API
                }, status=status.HTTP_200_OK)
            elif response.status_code == 401:
                # Handle Unauthorized error specifically
                return Response({
                    "error": "Unauthorized access",
                    "details": response.text
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # Handle other HTTP errors
                return Response({
                    "error": "Failed to fetch subscription plans",
                    "details": response.text
                }, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            # Catch any exceptions and log them
            return Response({
                "error": "Request failed",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
