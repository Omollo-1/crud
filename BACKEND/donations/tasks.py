from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Donation

@shared_task
def send_donation_confirmation_email(donation_id):
    try:
        donation = Donation.objects.get(id=donation_id)
        
        subject = f"Thank you for your donation to Chartitze!"
        
        html_message = render_to_string('emails/donation_confirmation.html', {
            'donation': donation,
            'site_url': settings.SITE_URL
        })
        
        text_message = render_to_string('emails/donation_confirmation.txt', {
            'donation': donation,
            'site_url': settings.SITE_URL
        })
        
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[donation.donor_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Also notify admin for large donations
        if donation.amount >= 1000:  # $1000 or more
            send_mail(
                subject=f"Large donation received: ${donation.amount}",
                message=f"A large donation of ${donation.amount} was received from {donation.donor_name}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
            
    except Donation.DoesNotExist:
        pass