from rest_framework import serializers
from .models import Donation, RecurringDonation
from programs.serializers import ProgramSerializer

class DonationSerializer(serializers.ModelSerializer):
    program_details = ProgramSerializer(source='program', read_only=True)
    
    class Meta:
        model = Donation
        fields = ['id', 'donor', 'donor_name', 'donor_email', 'donor_phone',
                  'amount', 'donation_type', 'payment_method', 'payment_status',
                  'transaction_id', 'currency', 'dedication', 'program',
                  'program_details', 'is_anonymous', 'notes', 'created_at']
        read_only_fields = ['created_at', 'updated_at', 'transaction_id']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

class CreateDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['donor_name', 'donor_email', 'donor_phone', 'amount',
                  'donation_type', 'payment_method', 'dedication', 'program',
                  'is_anonymous', 'currency']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['donor'] = request.user
        return super().create(validated_data)

class DonationSummarySerializer(serializers.Serializer):
    total_donations = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_donors = serializers.IntegerField()
    monthly_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    yearly_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    recent_donations = DonationSerializer(many=True)

class RecurringDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringDonation
        fields = '__all__'