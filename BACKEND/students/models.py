from django.db import models
from django.utils import timezone
from programs.models import Program

class Student(models.Model):
    full_name = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)
    date_of_birth = models.DateField()
    date_joined = models.DateField(default=timezone.now)
    student_class = models.CharField(max_length=100, help_text="Current class/grade")
    
    # Interests and Talents
    interests = models.TextField(blank=True, null=True)
    talents = models.TextField(blank=True, null=True)
    
    # Health and Values
    health_status = models.TextField(blank=True, null=True, help_text="General health condition and allergies")
    core_values = models.TextField(blank=True, null=True)
    
    # Enrollment
    programs_enrolled = models.ManyToManyField(Program, related_name='students', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_joined']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

class Transcript(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='transcripts')
    title = models.CharField(max_length=255, help_text="e.g., Year 2025 Term 1 Report")
    file = models.FileField(upload_to='students/transcripts/')
    description = models.TextField(blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.student.full_name}"
