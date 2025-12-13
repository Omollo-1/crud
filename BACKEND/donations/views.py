from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, Count
from .models import Donation, Donor, Campaign
from .serializers import (
    DonationSerializer, 
    DonorSerializer, 
    CampaignSerializer
)

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.AllowAny]  # Allow public donations
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_donations = Donation.objects.aggregate(
            total_amount=Sum('amount'),
            total_count=Count('id')
        )
        
        recent_donations = Donation.objects.all()[:10]
        recent_serializer = DonationSerializer(recent_donations, many=True)
        
        return Response({
            'total_amount': total_donations['total_amount'] or 0,
            'total_count': total_donations['total_count'] or 0,
            'recent_donations': recent_serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status_stats = Donation.objects.values('status').annotate(
            count=Count('id'),
            amount=Sum('amount')
        )
        return Response(status_stats)


class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [permissions.AllowAny]  # Allow public access
    
    @action(detail=False, methods=['get'])
    def top_donors(self, request):
        top_donors = Donor.objects.order_by('-total_donated')[:10]
        serializer = DonorSerializer(top_donors, many=True)
        return Response(serializer.data)


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.AllowAny]  # Allow public access
    
    @action(detail=True, methods=['post'])
    def donate(self, request, pk=None):
        campaign = self.get_object()
        amount = request.data.get('amount')
        
        if amount:
            campaign.current_amount += float(amount)
            campaign.save()
            
            # Create donation record
            donation = Donation.objects.create(
                donor_name=request.data.get('donor_name'),
                donor_email=request.data.get('donor_email'),
                amount=amount,
                payment_method=request.data.get('payment_method', 'mpesa'),
                status='pending'
            )
            
            return Response({
                'message': 'Donation initiated successfully',
                'campaign': CampaignSerializer(campaign).data,
                'donation': DonationSerializer(donation).data
            })
        
        return Response(
            {'error': 'Amount is required'},
            status=status.HTTP_400_BAD_REQUEST
        )


# Dashboard Stats View
from volunteers.models import Volunteer
from contact.models import ContactMessage
from rest_framework import generics, status

class DashboardStatsView(generics.GenericAPIView):
    def get(self, request):
        # Total donations
        total_stats = Donation.objects.aggregate(
            total_amount=Sum('amount'),
            total_count=Count('id')
        )
        
        # Recent donations
        recent_donations = Donation.objects.select_related().order_by('-created_at')[:5]
        
        # Campaign progress
        campaigns = Campaign.objects.all()
        
        # Status breakdown
        status_stats = Donation.objects.values('status').annotate(
            count=Count('id'),
            amount=Sum('amount')
        )
        
        # Top donors
        top_donors = Donor.objects.order_by('-total_donated')[:5]

        # Volunteer Stats
        active_volunteers = Volunteer.objects.filter(status='active').count()
        new_volunteers = Volunteer.objects.filter(status='pending').count()
        recent_volunteers = Volunteer.objects.order_by('-created_at')[:5]

        # Message Stats
        new_messages = ContactMessage.objects.filter(status='new').count()
        recent_messages = ContactMessage.objects.order_by('-submitted_at')[:5]

        # Combine recent activity (simplistic approach: just return separate lists, easy for frontend)
        # Or I can conform to the exact structure the frontend expects.
        # Frontend currently expects:
        # data.overview { active_volunteers, monthly_donations, new_messages, active_programs }
        # data.recent_activity: [{type: 'donation', ...}, {type: 'volunteer', ...}, {type: 'message', ...}]
        
        # Let's build the recent_activity list manually
        recent_activity = []
        
        for d in recent_donations:
            recent_activity.append({
                'type': 'donation',
                'date': d.created_at.strftime('%Y-%m-%d'),
                'donor_name': d.donor_name,
                'amount': float(d.amount),
                'status': d.status
            })
            
        for v in recent_volunteers:
            recent_activity.append({
                'type': 'volunteer',
                'date': v.created_at.strftime('%Y-%m-%d'),
                'name': v.name,
                'email': v.email,
                'status': v.status
            })
            
        for m in recent_messages:
            recent_activity.append({
                'type': 'message',
                'date': m.submitted_at.strftime('%Y-%m-%d'),
                'name': m.name,
                'email': m.email,
                'subject': m.subject,
                'status': m.status
            })
            
        # Sort combined activity by date (descending)
        recent_activity.sort(key=lambda x: x['date'], reverse=True)
        
        return Response({
            'overview': {
                'active_volunteers': active_volunteers,
                'monthly_donations': total_stats['total_amount'] or 0, # Total for now, can be refined to monthly
                'new_messages': new_messages,
                'active_programs': campaigns.count(), # Using campaigns as programs proxy
                'pending_volunteers': new_volunteers
            },
            'recent_activity': recent_activity[:15], # Return top 15 combined
            'total_donations': {
                'amount': total_stats['total_amount'] or 0,
                'count': total_stats['total_count'] or 0
            },
            'campaigns': CampaignSerializer(campaigns, many=True).data,
            'status_breakdown': list(status_stats),
            'top_donors': DonorSerializer(top_donors, many=True).data
        })