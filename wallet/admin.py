from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Wallet, WalletTransaction
from django.shortcuts import redirect
from django.contrib import messages
from decimal import Decimal  # Import Decimal

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')

    def get_queryset(self, request):
        """Allow operators to see only their wallets"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Admins see all wallets
        return qs.filter(user=request.user)  # Operators see only their wallet
    
    def changelist_view(self, request, extra_context=None):
        """Redirect operators to /wallet/ when they click 'Wallets' menu"""
        if not request.user.is_superuser:
            from django.shortcuts import redirect
            return redirect('/wallet/')
        return super().changelist_view(request, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        """Instead of creating a new wallet, update the existing wallet balance"""
        if not request.user.is_superuser:
            return redirect('/wallet/')

        if request.method == "POST":
            user_id = request.POST.get("user")  # Get the user from the form
            amount = request.POST.get("balance")  # Get the entered balance
            
            if not user_id or not amount:
                messages.error(request, "User and Amount are required.")
                return redirect(request.path)

            try:
                wallet = Wallet.objects.get(user_id=user_id)
                wallet.balance += Decimal(amount)  # ✅ Convert to Decimal before adding
                wallet.save()
                messages.success(request, f"₹{amount} added to the wallet successfully!")
                return redirect('/admin/wallet/wallet/')  # Redirect back to the admin panel
            except Wallet.DoesNotExist:
                messages.error(request, "User does not have a wallet. Please create one manually.")

        return super().add_view(request, form_url, extra_context)

admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransaction)
# ✅ Success and Error Pages

