from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Gallery Categories'
    
    def __str__(self):
        return self.name

class GalleryItem(models.Model):
    TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    item_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='image')
    
    # For images
    image = models.ImageField(upload_to='gallery/images/', blank=True, null=True)
    
    # For videos
    video_url = models.URLField(blank=True, null=True, help_text="YouTube or Vimeo URL")
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True)
    
    # Metadata
    photographer = models.CharField(max_length=255, blank=True, null=True)
    date_taken = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    # Display settings
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Gallery Item')
        verbose_name_plural = _('Gallery Items')
    
    def __str__(self):
        return self.title
    
    @property
    def thumbnail_url(self):
        if self.item_type == 'image' and self.image:
            return self.image.url
        elif self.item_type == 'video' and self.video_url:
            # Generate thumbnail from video URL (you might want to use a service for this)
            return f"https://img.youtube.com/vi/{self.extract_youtube_id()}/hqdefault.jpg"
        return None
    
    def extract_youtube_id(self):
        if 'youtube.com' in self.video_url or 'youtu.be' in self.video_url:
            import re
            pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)'
            match = re.search(pattern, self.video_url)
            return match.group(1) if match else None
        return None

class GalleryAlbum(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='gallery/albums/', blank=True, null=True)
    items = models.ManyToManyField(GalleryItem, related_name='albums', blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def item_count(self):
        return self.items.count()