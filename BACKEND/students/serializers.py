from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id', 'full_name', 'profile_photo', 'date_of_birth', 
            'date_joined', 'student_class', 'interests', 'talents', 
            'health_status', 'core_values', 'programs_enrolled',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'full_name', 'profile_photo', 'date_of_birth', 
            'student_class', 'interests', 'talents', 
            'health_status', 'core_values'
        ]
