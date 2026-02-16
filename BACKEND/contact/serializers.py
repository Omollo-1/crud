from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import ContactMessage, NewsletterSubscriber, SiteConfiguration

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'subject', 'category',
                  'message', 'status', 'replied_at', 'reply_message',
                  'submitted_at', 'updated_at']
        read_only_fields = ['status', 'replied_at', 'reply_message', 
                           'submitted_at', 'updated_at']
    
    def validate_email(self, value):
        try:
            validate_email(value)
            return value
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")

class CreateContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'category', 'message']
    
    def create(self, validated_data):
        request = self.context.get('request')
        message = ContactMessage.objects.create(**validated_data)
        
        # Capture request metadata
        if request:
            message.ip_address = request.META.get('REMOTE_ADDR')
            message.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            message.save()
        
        # Send notification email
        from .tasks import send_contact_notification_email
        try:
            send_contact_notification_email.delay(message.id)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send contact notification email: {e}")
        
        return message

class ReplyContactMessageSerializer(serializers.Serializer):
    reply_message = serializers.CharField(required=True)

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'name', 'is_active', 'subscribed_at']
        read_only_fields = ['is_active', 'subscribed_at']

class SubscribeNewsletterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=False, allow_blank=True)
    source = serializers.CharField(required=False, allow_blank=True)
    
    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        
        # Check if already subscribed and active
        if NewsletterSubscriber.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        
        return value
    
    def create(self, validated_data):
        email = validated_data['email']
        name = validated_data.get('name', '')
        source = validated_data.get('source', 'website')
        
        # If email exists but unsubscribed, reactivate it
        subscriber, created = NewsletterSubscriber.objects.update_or_create(
            email=email,
            defaults={
                'name': name,
                'source': source,
                'is_active': True,
                'unsubscribed_at': None
            }
        )
        
        # Send welcome email
        from .tasks import send_newsletter_welcome_email
        try:
            send_newsletter_welcome_email.delay(subscriber.id)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send newsletter welcome email: {e}")
        
        return subscriber

class SiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'
        read_only_fields = ['updated_at']

class ContactSummarySerializer(serializers.Serializer):
    total_messages = serializers.IntegerField()
    new_messages = serializers.IntegerField()
    total_subscribers = serializers.IntegerField()
    active_subscribers = serializers.IntegerField()
    recent_messages = ContactMessageSerializer(many=True)