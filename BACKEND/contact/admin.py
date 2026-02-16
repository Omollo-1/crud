from django.contrib import admin
from django.utils.html import format_html
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage, NewsletterSubscriber, SiteConfiguration

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'category', 'status', 'submitted_at', 'reply_actions')
    list_filter = ('status', 'category', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('submitted_at', 'updated_at', 'ip_address', 'user_agent')
    actions = ['mark_as_read', 'send_email_reply', 'send_sms_reply']

    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'phone', 'subject', 'category', 'message', 'status')
        }),
        ('Reply Information', {
            'fields': ('reply_message', 'replied_at', 'replied_by')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def reply_actions(self, obj):
        return format_html(
            '<a class="button" href="mailto:{}?subject=Re: {}" style="background-color: #e63946; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none;">Email</a> '
            '<a class="button" href="#" onclick="alert(\'SMS functionality coming soon!\')" style="background-color: #264653; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none; margin-left: 5px;">SMS</a>',
            obj.email, obj.subject
        )
    reply_actions.short_description = 'Reply Options'

    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
    mark_as_read.short_description = "Mark selected messages as read"

    def send_email_reply(self, request, queryset):
        # This is a bulk action that could be refined to show a form
        for message in queryset:
            if message.reply_message:
                send_mail(
                    f"Re: {message.subject}",
                    message.reply_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [message.email],
                    fail_silently=False,
                )
                message.status = 'replied'
                message.save()
    send_email_reply.short_description = "Send Email Reply (uses current reply message)"

    def send_sms_reply(self, request, queryset):
        # Placeholder for SMS functionality
        for message in queryset:
            if message.phone and message.reply_message:
                # Log the SMS (simulating sending)
                print(f"Sending SMS to {message.phone}: {message.reply_message}")
                message.status = 'replied'
                message.save()
    send_sms_reply.short_description = "Send SMS Reply (uses current reply message)"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email', 'name')

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'admin_email', 'updated_at')
    
    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
