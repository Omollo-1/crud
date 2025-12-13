from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import ContactMessage, NewsletterSubscriber, SiteConfiguration
from .serializers import (
    ContactMessageSerializer, CreateContactMessageSerializer,
    ReplyContactMessageSerializer, NewsletterSubscriberSerializer,
    SubscribeNewsletterSerializer, SiteConfigurationSerializer,
    ContactSummarySerializer
)
from .filters import ContactMessageFilter

class ContactMessageListView(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] # ORIGINAL
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()] # Only admin can list messages

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ContactMessageFilter
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['submitted_at', 'status']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateContactMessageSerializer
        return ContactMessageSerializer
    
    def get_queryset(self):
        queryset = ContactMessage.objects.all()
        # Only staff can see all messages
        if not self.request.user.is_staff:
            queryset = queryset.none()
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        
        # Return success response
        return Response({
            'message': 'Your message has been sent successfully. We will get back to you soon.',
            'data': ContactMessageSerializer(message).data
        }, status=status.HTTP_201_CREATED)

class ContactMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Mark as read when retrieved by admin
        if instance.status == 'new':
            instance.mark_as_read()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ReplyContactMessageView(generics.UpdateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ReplyContactMessageSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        message = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Send reply
        from .tasks import send_contact_reply_email
        send_contact_reply_email.delay(
            message.id, 
            serializer.validated_data['reply_message'],
            request.user.id
        )
        
        return Response({
            'message': 'Reply sent successfully',
            'data': ContactMessageSerializer(message).data
        })

class NewsletterSubscribeView(generics.CreateAPIView):
    serializer_class = SubscribeNewsletterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscriber = serializer.save()
        
        return Response({
            'message': 'Successfully subscribed to our newsletter!',
            'data': NewsletterSubscriberSerializer(subscriber).data
        }, status=status.HTTP_201_CREATED)

class NewsletterUnsubscribeView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subscriber = NewsletterSubscriber.objects.get(email=email, is_active=True)
            subscriber.unsubscribe()
            return Response({'message': 'Successfully unsubscribed from newsletter'})
        except NewsletterSubscriber.DoesNotExist:
            return Response({'error': 'Email not found or already unsubscribed'}, 
                           status=status.HTTP_404_NOT_FOUND)

class NewsletterSubscriberListView(generics.ListAPIView):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'name']

class SiteConfigurationView(generics.RetrieveUpdateAPIView):
    queryset = SiteConfiguration.objects.all()
    serializer_class = SiteConfigurationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        return SiteConfiguration.load()
    
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class ContactSummaryView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        # Total messages
        total_messages = ContactMessage.objects.count()
        
        # New messages
        new_messages = ContactMessage.objects.filter(status='new').count()
        
        # Total subscribers
        total_subscribers = NewsletterSubscriber.objects.count()
        
        # Active subscribers
        active_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()
        
        # Recent messages
        recent_messages = ContactMessage.objects.all().order_by('-submitted_at')[:10]
        
        data = {
            'total_messages': total_messages,
            'new_messages': new_messages,
            'total_subscribers': total_subscribers,
            'active_subscribers': active_subscribers,
            'recent_messages': ContactMessageSerializer(recent_messages, many=True).data
        }
        
        serializer = ContactSummarySerializer(data)
        return Response(serializer.data)