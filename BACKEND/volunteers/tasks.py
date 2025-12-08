from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Volunteer

@shared_task
def send_volunteer_confirmation_email(volunteer_id):
    try:
        volunteer = Volunteer.objects.get(id=volunteer_id)
        
        subject = f"Thank you for your volunteer application to Chartitze!"
        
        html_message = render_to_string('emails/volunteer_confirmation.html', {
            'volunteer': volunteer,
            'site_url': settings.SITE_URL
        })
        
        text_message = render_to_string('emails/volunteer_confirmation.txt', {
            'volunteer': volunteer,
            'site_url': settings.SITE_URL
        })
        
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[volunteer.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Notify admin about new application
        send_mail(
            subject=f"New Volunteer Application: {volunteer.name}",
            message=f"A new volunteer application was received from {volunteer.name}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )
        
    except Volunteer.DoesNotExist:
        pass

@shared_task
def send_volunteer_status_update_email(volunteer_id, status):
    try:
        volunteer = Volunteer.objects.get(id=volunteer_id)
        
        status_display = dict(Volunteer.STATUS_CHOICES).get(status, status)
        
        subject = f"Update on your Chartitze volunteer application"
        
        html_message = render_to_string('emails/volunteer_status_update.html', {
            'volunteer': volunteer,
            'status': status_display,
            'site_url': settings.SITE_URL
        })
        
        text_message = render_to_string('emails/volunteer_status_update.txt', {
            'volunteer': volunteer,
            'status': status_display,
            'site_url': settings.SITE_URL
        })
        
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[volunteer.email],
            html_message=html_message,
            fail_silently=False,
        )
        
    except Volunteer.DoesNotExist:
        pass