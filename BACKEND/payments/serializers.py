from rest_framework import serializers
from .models import MpesaPayment


class MpesaPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaPayment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'merchant_request_id', 
                           'checkout_request_id', 'result_code', 'result_desc',
                           'mpesa_receipt_number', 'transaction_date']


class STKPushRequestSerializer(serializers.Serializer):
    """Serializer for initiating STK Push"""
    phone_number = serializers.CharField(max_length=15, help_text="Format: 254XXXXXXXXX or 07XXXXXXXX")
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1)
    donation_id = serializers.IntegerField(required=False, help_text="Link to existing donation")
    account_reference = serializers.CharField(max_length=100, default="Donation")
    transaction_desc = serializers.CharField(max_length=100, default="Charitize Donation")
    
    def validate_phone_number(self, value):
        """Validate and format phone number"""
        # Remove any spaces or special characters
        phone = value.replace(' ', '').replace('-', '').replace('+', '')
        
        # Convert 07XXXXXXXX to 2547XXXXXXXX
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        
        # Ensure it starts with 254
        if not phone.startswith('254'):
            raise serializers.ValidationError("Phone number must start with 254 or 0")
        
        # Validate length (254 + 9 digits = 12 digits)
        if len(phone) != 12:
            raise serializers.ValidationError("Invalid phone number length")
        
        return phone
