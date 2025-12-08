from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from donations.models import Donation
from volunteers.models import Volunteer
from programs.models import Program
from gallery.models import GalleryItem
from contact.models import ContactMessage, NewsletterSubscriber

class DashboardSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to access this resource."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Time periods
        today = timezone.now().date()
        this_month_start = today.replace(day=1)
        last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
        this_year_start = today.replace(month=1, day=1)
        
        # Donations summary
        total_donations = Donation.objects.filter(payment_status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        monthly_donations = Donation.objects.filter(
            payment_status='completed',
            created_at__date__gte=this_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        last_month_donations = Donation.objects.filter(
            payment_status='completed',
            created_at__date__gte=last_month_start,
            created_at__date__lt=this_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        yearly_donations = Donation.objects.filter(
            payment_status='completed',
            created_at__date__gte=this_year_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Volunteers summary
        total_volunteers = Volunteer.objects.count()
        active_volunteers = Volunteer.objects.filter(status__in=['active', 'approved']).count()
        pending_volunteers = Volunteer.objects.filter(status='pending').count()
        
        # Programs summary
        total_programs = Program.objects.count()
        active_programs = Program.objects.filter(status='active').count()
        total_beneficiaries = Program.objects.aggregate(
            total=Sum('beneficiaries_count')
        )['total'] or 0
        
        # Gallery summary
        total_gallery_items = GalleryItem.objects.filter(is_published=True).count()
        
        # Contact summary
        total_messages = ContactMessage.objects.count()
        new_messages = ContactMessage.objects.filter(status='new').count()
        total_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()
        
        # Recent activity
        recent_donations = Donation.objects.filter(payment_status='completed').order_by('-created_at')[:5]
        recent_volunteers = Volunteer.objects.filter(status__in=['active', 'approved']).order_by('-application_date')[:5]
        recent_messages = ContactMessage.objects.all().order_by('-submitted_at')[:5]
        
        # Format recent data
        recent_donations_data = [
            {
                'id': d.id,
                'donor_name': d.donor_name,
                'amount': float(d.amount),
                'date': d.created_at.strftime('%Y-%m-%d'),
                'type': 'donation'
            }
            for d in recent_donations
        ]
        
        recent_volunteers_data = [
            {
                'id': v.id,
                'name': v.name,
                'email': v.email,
                'status': v.get_status_display(),
                'date': v.application_date.strftime('%Y-%m-%d'),
                'type': 'volunteer'
            }
            for v in recent_volunteers
        ]
        
        recent_messages_data = [
            {
                'id': m.id,
                'name': m.name,
                'email': m.email,
                'subject': m.subject,
                'status': m.get_status_display(),
                'date': m.submitted_at.strftime('%Y-%m-%d'),
                'type': 'message'
            }
            for m in recent_messages
        ]
        
        # Combine recent activity
        recent_activity = recent_donations_data + recent_volunteers_data + recent_messages_data
        recent_activity.sort(key=lambda x: x['date'], reverse=True)
        recent_activity = recent_activity[:10]
        
        # Monthly donation trend (last 6 months)
        monthly_trend = []
        for i in range(5, -1, -1):
            month_start = (this_month_start - timedelta(days=30*i)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            monthly_total = Donation.objects.filter(
                payment_status='completed',
                created_at__date__gte=month_start,
                created_at__date__lte=month_end
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            monthly_trend.append({
                'month': month_start.strftime('%b %Y'),
                'total': float(monthly_total)
            })
        
        data = {
            'overview': {
                'total_donations': float(total_donations),
                'monthly_donations': float(monthly_donations),
                'last_month_donations': float(last_month_donations),
                'yearly_donations': float(yearly_donations),
                'total_volunteers': total_volunteers,
                'active_volunteers': active_volunteers,
                'pending_volunteers': pending_volunteers,
                'total_programs': total_programs,
                'active_programs': active_programs,
                'total_beneficiaries': total_beneficiaries,
                'total_gallery_items': total_gallery_items,
                'total_messages': total_messages,
                'new_messages': new_messages,
                'total_subscribers': total_subscribers,
            },
            'recent_activity': recent_activity,
            'monthly_trend': monthly_trend,
            'charts': {
                'donation_distribution': self.get_donation_distribution(),
                'program_funding': self.get_program_funding_data(),
                'volunteer_status': self.get_volunteer_status_data(),
            }
        }
        
        return Response(data)
    
    def get_donation_distribution(self):
        # Get donations by payment method
        distribution = Donation.objects.filter(payment_status='completed').values(
            'payment_method'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        return [
            {
                'method': item['payment_method'],
                'total': float(item['total'] or 0),
                'count': item['count']
            }
            for item in distribution
        ]
    
    def get_program_funding_data(self):
        programs = Program.objects.filter(status='active').annotate(
            progress_percentage=(
                (Sum('current_amount') / Sum('target_amount')) * 100 
                if Sum('target_amount') > 0 else 0
            )
        ).values('title', 'target_amount', 'current_amount')[:10]
        
        return [
            {
                'program': item['title'],
                'target': float(item['target_amount'] or 0),
                'current': float(item['current_amount'] or 0),
                'progress': float(item['progress_percentage'] or 0)
            }
            for item in programs
        ]
    
    def get_volunteer_status_data(self):
        status_counts = Volunteer.objects.values('status').annotate(
            count=Count('id')
        )
        
        status_map = dict(Volunteer.STATUS_CHOICES)
        
        return [
            {
                'status': status_map.get(item['status'], item['status']),
                'count': item['count']
            }
            for item in status_counts
        ]

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to access this resource."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        last_week = today - timedelta(days=7)
        last_month = today - timedelta(days=30)
        
        stats = {
            'donations': {
                'today': Donation.objects.filter(
                    payment_status='completed',
                    created_at__date=today
                ).aggregate(total=Sum('amount'))['total'] or 0,
                'yesterday': Donation.objects.filter(
                    payment_status='completed',
                    created_at__date=yesterday
                ).aggregate(total=Sum('amount'))['total'] or 0,
                'last_week': Donation.objects.filter(
                    payment_status='completed',
                    created_at__date__gte=last_week
                ).aggregate(total=Sum('amount'))['total'] or 0,
                'last_month': Donation.objects.filter(
                    payment_status='completed',
                    created_at__date__gte=last_month
                ).aggregate(total=Sum('amount'))['total'] or 0,
            },
            'volunteers': {
                'today': Volunteer.objects.filter(application_date=today).count(),
                'yesterday': Volunteer.objects.filter(application_date=yesterday).count(),
                'last_week': Volunteer.objects.filter(application_date__gte=last_week).count(),
                'last_month': Volunteer.objects.filter(application_date__gte=last_month).count(),
            },
            'messages': {
                'today': ContactMessage.objects.filter(submitted_at__date=today).count(),
                'yesterday': ContactMessage.objects.filter(submitted_at__date=yesterday).count(),
                'last_week': ContactMessage.objects.filter(submitted_at__date__gte=last_week).count(),
                'last_month': ContactMessage.objects.filter(submitted_at__date__gte=last_month).count(),
            }
        }
        
        # Convert Decimal to float for JSON serialization
        for category in stats:
            if isinstance(stats[category], dict):
                for period in stats[category]:
                    if hasattr(stats[category][period], '__float__'):
                        stats[category][period] = float(stats[category][period])
        
        return Response(stats)