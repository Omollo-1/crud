from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class Program(models.Model):
    CATEGORY_CHOICES = (
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('nutrition', 'Nutrition'),
        ('mentorship', 'Mentorship'),
        ('recreation', 'Recreation'),
        ('shelter', 'Shelter'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    short_description = models.TextField(max_length=500)
    description = RichTextField()
    image = models.ImageField(upload_to='programs/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='programs/banners/', blank=True, null=True)
    
    # Program details
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Metrics
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    beneficiaries_count = models.PositiveIntegerField(default=0)
    volunteers_needed = models.PositiveIntegerField(default=0)
    
    # Features
    features = models.JSONField(default=list, help_text="List of program features")
    
    # SEO
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Program')
        verbose_name_plural = _('Programs')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def progress_percentage(self):
        if self.target_amount and self.target_amount > 0:
            return min(100, (self.current_amount / self.target_amount) * 100)
        return 0
    
    @property
    def duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

class ProgramUpdate(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to='program_updates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Update for {self.program.title}: {self.title}"

class ProgramBeneficiary(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='beneficiaries')
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='beneficiaries/', blank=True, null=True)
    story = RichTextField(blank=True, null=True)
    joined_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.program.title}"