from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from donations.models import Donation
from volunteers.models import Volunteer
from contact.models import ContactMessage
from programs.models import Program
from students.models import Student

def dashboard_stats(request):
    if not request.path.startswith('/admin/'):
        return {}

    today = timezone.now().date()
    this_month_start = today.replace(day=1)
    
    # Active Volunteers count
    active_volunteers = Volunteer.objects.filter(status__in=['active', 'approved']).count()
    
    # Monthly Donations total
    monthly_donations = Donation.objects.filter(
        status='completed',
        created_at__date__gte=this_month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # New Messages count
    new_messages = ContactMessage.objects.filter(status='new').count()
    
    # Upcoming Events (Programs with status 'upcoming' or 'active')
    upcoming_events = Program.objects.filter(status__in=['upcoming', 'active']).count()

    # Total Students
    total_students = Student.objects.count()
    
    # Recent 5 donations
    recent_donations = Donation.objects.filter(status='completed').order_by('-created_at')[:5]
    
    return {
        'dashboard_stats': {
            'active_volunteers': active_volunteers,
            'monthly_donations': monthly_donations,
            'new_messages': new_messages,
            'upcoming_events': upcoming_events,
            'total_students': total_students,
            'recent_donations': recent_donations,
            'now': timezone.now(),
        }
    }
