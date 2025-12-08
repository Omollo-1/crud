from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import ContactMessage, NewsletterSubscriber

@shared_task
def send_contact_notification_email(message_id):
    try:
        message = ContactMessage.objects.get(id=message_id)
        
        subject = f"New Contact Message: {message.subject}"
        
        html_message = render_to_string('emails/contact_notification.html', {
            'message': message,
            'site_url': settings.SITE_URL
        })
        
        text_message = render_to_string('emails/contact_notification.txt', {
            'message': message,
            'site_url': settings.SITE_URL
        })
        
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        
    except ContactMessage.DoesNotExist:
        pass

@shared_task
def send_contact_reply_email(message_id, reply_text, user_id):
    try:
        from users.models import User
        
        message = ContactMessage.objects.get(id=message_id)
        user = User.objects.get(id=user_id) if user_id else None
        
        subject = f"Re: {message.subject}"
        
        html_message = render_to_string('emails/contact_reply.html', {
            'message': message,
            'reply_text': reply_text,
            'user': user,
            'site_url': settings.SITE_URL
        })
        
        text_message = render_to_string('emails/contact_reply.txt', {
            'message': message,
            'reply_text': reply_text,
            'user': user,
            'site_url': settings.SITE_URL
        })
        
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[message.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Update message status
        message.reply(reply_text, user)
        
    except (ContactMessage.DoesNotExist, User.DoesNotExist):
        pass

@shared_task
def send_newsletter_welcome_email(subscriber_id):
    try:
        subscriber = NewsletterSubscriber.objects.get(id=subscriber_id)
        
        subject = "Welcome to Chartitze Newsletter!"
        
        html_message = render_to_string('emails/newsletter_welcome.html', {
            'subscriber': subscriber,
            'site_url': settings.SITE_URL
        })
        
        text_message = render_to_string('emails/newsletter_welcome.txt', {
            'subscriber': subscriber,
            'site_url': settings.SITE_URL
        })
        
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscriber.email],
            html_message=html_message,
            fail_silently=False,
        )
        
    except NewsletterSubscriber.DoesNotExist:
        pass