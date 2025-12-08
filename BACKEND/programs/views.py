from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from .models import Program, ProgramUpdate, ProgramBeneficiary
from .serializers import (
    ProgramSerializer, ProgramUpdateSerializer,
    ProgramBeneficiarySerializer, ProgramSummarySerializer
)
from .filters import ProgramFilter

class ProgramListView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProgramFilter
    search_fields = ['title', 'short_description', 'description', 'location']
    ordering_fields = ['created_at', 'title', 'target_amount']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Only show active programs to non-staff users
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='active')
        return queryset

class ProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class ProgramBySlugView(generics.RetrieveAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

class ProgramUpdateListView(generics.ListCreateAPIView):
    serializer_class = ProgramUpdateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        program_id = self.kwargs.get('program_id')
        return ProgramUpdate.objects.filter(program_id=program_id)
    
    def perform_create(self, serializer):
        program_id = self.kwargs.get('program_id')
        program = Program.objects.get(id=program_id)
        serializer.save(program=program)

class ProgramBeneficiaryListView(generics.ListCreateAPIView):
    serializer_class = ProgramBeneficiarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        program_id = self.kwargs.get('program_id')
        return ProgramBeneficiary.objects.filter(program_id=program_id, is_active=True)
    
    def perform_create(self, serializer):
        program_id = self.kwargs.get('program_id')
        program = Program.objects.get(id=program_id)
        serializer.save(program=program)

class ProgramSummaryView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Total programs
        total_programs = Program.objects.count()
        
        # Active programs
        active_programs = Program.objects.filter(status='active').count()
        
        # Total beneficiaries across all programs
        total_beneficiaries = Program.objects.aggregate(
            total=Sum('beneficiaries_count')
        )['total'] or 0
        
        # Total funding needed and received
        total_funding_needed = Program.objects.filter(status='active').aggregate(
            total=Sum('target_amount')
        )['total'] or 0
        
        total_funding_received = Program.objects.filter(status='active').aggregate(
            total=Sum('current_amount')
        )['total'] or 0
        
        # Recent programs
        recent_programs = Program.objects.filter(status='active').order_by('-created_at')[:6]
        
        data = {
            'total_programs': total_programs,
            'active_programs': active_programs,
            'total_beneficiaries': total_beneficiaries,
            'total_funding_needed': total_funding_needed,
            'total_funding_received': total_funding_received,
            'recent_programs': ProgramSerializer(recent_programs, many=True).data
        }
        
        serializer = ProgramSummarySerializer(data)
        return Response(serializer.data)

class ProgramCategoryListView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        categories = dict(Program.CATEGORY_CHOICES)
        category_data = []
        
        for category_id, category_name in categories.items():
            count = Program.objects.filter(category=category_id, status='active').count()
            if count > 0:
                category_data.append({
                    'id': category_id,
                    'name': category_name,
                    'count': count
                })
        
        return Response(category_data)