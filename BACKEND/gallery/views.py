from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import GalleryCategory, GalleryItem, GalleryAlbum
from .serializers import (
    GalleryCategorySerializer, GalleryItemSerializer,
    GalleryAlbumSerializer, GallerySummarySerializer
)
from .filters import GalleryItemFilter

class GalleryCategoryListView(generics.ListCreateAPIView):
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # For non-staff, only show categories with published items
        if not self.request.user.is_staff:
            queryset = queryset.filter(items__is_published=True).distinct()
        return queryset

class GalleryItemListView(generics.ListCreateAPIView):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = GalleryItemFilter
    search_fields = ['title', 'description', 'location', 'photographer']
    ordering_fields = ['created_at', 'title', 'date_taken']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # For non-staff, only show published items
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        return queryset
    
    def perform_create(self, serializer):
        # Set the uploader if authenticated
        if self.request.user.is_authenticated:
            serializer.save()
        else:
            serializer.save()

class GalleryItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class GalleryAlbumListView(generics.ListCreateAPIView):
    queryset = GalleryAlbum.objects.all()
    serializer_class = GalleryAlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # For non-staff, only show published albums
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        return queryset

class GalleryAlbumDetailView(generics.RetrieveAPIView):
    queryset = GalleryAlbum.objects.all()
    serializer_class = GalleryAlbumSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

class FeaturedGalleryItemsView(generics.ListAPIView):
    serializer_class = GalleryItemSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return GalleryItem.objects.filter(is_featured=True, is_published=True).order_by('-created_at')[:12]

class GallerySummaryView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Total items
        total_items = GalleryItem.objects.filter(is_published=True).count()
        
        # Total categories
        total_categories = GalleryCategory.objects.filter(
            items__is_published=True
        ).distinct().count()
        
        # Total albums
        total_albums = GalleryAlbum.objects.filter(is_published=True).count()
        
        # Featured items
        featured_items = GalleryItem.objects.filter(
            is_featured=True, is_published=True
        ).order_by('-created_at')[:8]
        
        # Recent items
        recent_items = GalleryItem.objects.filter(
            is_published=True
        ).order_by('-created_at')[:12]
        
        data = {
            'total_items': total_items,
            'total_categories': total_categories,
            'total_albums': total_albums,
            'featured_items': GalleryItemSerializer(featured_items, many=True, context={'request': request}).data,
            'recent_items': GalleryItemSerializer(recent_items, many=True, context={'request': request}).data,
        }
        
        serializer = GallerySummarySerializer(data)
        return Response(serializer.data)