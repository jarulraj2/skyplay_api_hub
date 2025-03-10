# admin.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.views import View
from .utils import encrypt, decrypt
from .models import Encryption  # Ensure Encryption model is imported

# Custom Encryption and Decryption View for Admin
class EncryptionDecryptionAdminView(View):
    def get(self, request):
        return render(request, 'admin/watcho/enc_dec.html')  # Render the same page for both encrypt and decrypt

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

        return render(request, 'admin/watcho/enc_dec.html', {
            'plain_text': plain_text,
            'encrypted_text': encrypted_text,
            'result_text': result_text,
            'action': action
        })

# Register the custom view for the Django Admin interface
class EncryptionAdmin(admin.ModelAdmin):
    change_list_template = "admin/watcho/enc_link.html"  # Your link template if any

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(EncryptionDecryptionAdminView.as_view()), name='encryption_decryption_view'),  # Set the URL path here to '/'
        ]
        return custom_urls + urls

# Register your model with the custom admin
admin.site.register(Encryption, EncryptionAdmin)
