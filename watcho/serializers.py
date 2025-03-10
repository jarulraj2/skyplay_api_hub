from rest_framework import serializers

class EncryptionSerializer(serializers.Serializer):
    # Using JSONField for 'plain_text' to allow it to be a JSON object (a dictionary or list)
    plain_text = serializers.JSONField(required=True, help_text="The plain text to encrypt")

class DecryptionSerializer(serializers.Serializer):
    # 'encrypted_text' will be a string (Base64 encoded)
    encrypted_text = serializers.CharField(required=True, help_text="The encrypted text to decrypt")

# Serializer for the SubscriptionPlanDetails API input
class SubscriptionPlanDetailsSerializer(serializers.Serializer):
    InputData = serializers.CharField(help_text="Encrypted data to be sent to the external API")
