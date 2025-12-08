

# Create your views here.
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Donation, RecurringDonation
from .serializers import (
    DonationSerializer, CreateDonationSerializer,
    DonationSummarySerializer, RecurringDonationSerializer
)
from .filters import DonationFilter
from .tasks import send_donation_confirmation_email

class DonationListView(generics.ListCreateAPIView):
    queryset = Donation.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DonationFilter
    search_fields = ['donor_name', 'donor_email', 'transaction_id']
    ordering_fields = ['amount', 'created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateDonationSerializer
        return DonationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            # Non-staff users can only see their own donations or anonymous donations
            queryset = queryset.filter(
                Q(donor=self.request.user) if self.request.user.is_authenticated else Q()
            )
        return queryset
    
    def perform_create(self, serializer):
        donation = serializer.save()
        # Send confirmation email asynchronously
        send_donation_confirmation_email.delay(donation.id)

class DonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class MyDonationsView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Donation.objects.filter(donor=self.request.user).order_by('-created_at')

class UpdatePaymentStatusView(generics.UpdateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        donation = self.get_object()
        new_status = request.data.get('payment_status')
        transaction_id = request.data.get('transaction_id')
        
        if new_status == 'completed':
            donation.mark_as_completed(transaction_id)
        elif new_status == 'failed':
            donation.mark_as_failed()
        else:
            donation.payment_status = new_status
            donation.save()
        
        serializer = self.get_serializer(donation)
        return Response(serializer.data)

class DonationSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        # Total donations
        total_donations = Donation.objects.filter(
            payment_status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Total unique donors
        total_donors = Donation.objects.filter(
            payment_status='completed'
        ).values('donor_email').distinct().count()
        
        # Monthly total (current month)
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_total = Donation.objects.filter(
            payment_status='completed',
            created_at__gte=current_month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Yearly total (current year)
        current_year = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        yearly_total = Donation.objects.filter(
            payment_status='completed',
            created_at__gte=current_year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Recent donations
        recent_donations = Donation.objects.filter(
            payment_status='completed'
        ).order_by('-created_at')[:10]
        
        data = {
            'total_donations': total_donations,
            'total_donors': total_donors,
            'monthly_total': monthly_total,
            'yearly_total': yearly_total,
            'recent_donations': DonationSerializer(recent_donations, many=True).data
        }
        
        serializer = DonationSummarySerializer(data)
        return Response(serializer.data)

class RecurringDonationListView(generics.ListCreateAPIView):
    queryset = RecurringDonation.objects.all()
    serializer_class = RecurringDonationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(donor=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

class RecurringDonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecurringDonation.objects.all()
    serializer_class = RecurringDonationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(donor=self.request.user)