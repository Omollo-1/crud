from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Volunteer, VolunteerAssignment
from .serializers import (
    VolunteerSerializer, CreateVolunteerSerializer,
    VolunteerStatusUpdateSerializer, VolunteerAssignmentSerializer,
    VolunteerSummarySerializer
)
from .filters import VolunteerFilter
from .tasks import send_volunteer_confirmation_email

class VolunteerListView(generics.ListCreateAPIView):
    queryset = Volunteer.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VolunteerFilter
    search_fields = ['name', 'email', 'phone', 'skills']
    ordering_fields = ['application_date', 'name', 'age']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateVolunteerSerializer
        return VolunteerSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            # Non-staff can only see approved volunteers or their own application
            queryset = queryset.filter(
                Q(status__in=['approved', 'active']) |
                Q(user=self.request.user) if self.request.user.is_authenticated else Q()
            )
        return queryset
    
    def perform_create(self, serializer):
        volunteer = serializer.save()
        # Send confirmation email asynchronously
        send_volunteer_confirmation_email.delay(volunteer.id)

class VolunteerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class MyVolunteerApplicationView(generics.RetrieveAPIView):
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return Volunteer.objects.get(user=self.request.user)
        except Volunteer.DoesNotExist:
            return None
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({"detail": "No volunteer application found."}, 
                           status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UpdateVolunteerStatusView(generics.UpdateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        volunteer = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        volunteer.status = serializer.validated_data['status']
        if serializer.validated_data.get('notes'):
            volunteer.notes = serializer.validated_data['notes']
        volunteer.save()
        
        # Send status update email
        send_volunteer_status_update_email.delay(volunteer.id, volunteer.status)
        
        return Response(VolunteerSerializer(volunteer).data)

class VolunteerSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        # Total volunteers
        total_volunteers = Volunteer.objects.count()
        
        # Active volunteers
        active_volunteers = Volunteer.objects.filter(status__in=['active', 'approved']).count()
        
        # Pending applications
        pending_applications = Volunteer.objects.filter(status='pending').count()
        
        # Recent volunteers
        recent_volunteers = Volunteer.objects.filter(status__in=['active', 'approved']).order_by('-application_date')[:10]
        
        data = {
            'total_volunteers': total_volunteers,
            'active_volunteers': active_volunteers,
            'pending_applications': pending_applications,
            'recent_volunteers': VolunteerSerializer(recent_volunteers, many=True).data
        }
        
        serializer = VolunteerSummarySerializer(data)
        return Response(serializer.data)

class VolunteerAssignmentListView(generics.ListCreateAPIView):
    queryset = VolunteerAssignment.objects.all()
    serializer_class = VolunteerAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            # Volunteers can only see their own assignments
            queryset = queryset.filter(volunteer__user=self.request.user)
        return queryset

class VolunteerAssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VolunteerAssignment.objects.all()
    serializer_class = VolunteerAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(volunteer__user=self.request.user)