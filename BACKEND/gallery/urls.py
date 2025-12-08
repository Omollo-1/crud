from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.GalleryCategoryListView.as_view(), name='gallery_categories'),
    path('items/', views.GalleryItemListView.as_view(), name='gallery_items'),
    path('items/<int:pk>/', views.GalleryItemDetailView.as_view(), name='gallery_item_detail'),
    path('albums/', views.GalleryAlbumListView.as_view(), name='gallery_albums'),
    path('albums/<slug:slug>/', views.GalleryAlbumDetailView.as_view(), name='gallery_album_detail'),
    path('featured/', views.FeaturedGalleryItemsView.as_view(), name='featured_gallery_items'),
    path('summary/', views.GallerySummaryView.as_view(), name='gallery_summary'),
]