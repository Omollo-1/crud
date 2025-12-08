from rest_framework import serializers
from .models import Volunteer, VolunteerAssignment
from users.serializers import UserSerializer

class VolunteerSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Volunteer
        fields = ['id', 'user', 'user_details', 'name', 'email', 'phone', 'age', 
                  'occupation', 'address', 'skills', 'interests', 'availability',
                  'preferred_time', 'commitment_level', 'motivation',
                  'emergency_contact_name', 'emergency_contact_phone', 
                  'emergency_contact_relation', 'status', 'application_date',
                  'start_date', 'end_date', 'has_background_check',
                  'background_check_date', 'notes', 'created_at']
        read_only_fields = ['application_date', 'created_at', 'updated_at']

class CreateVolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'phone', 'age', 'occupation', 'address',
                  'skills', 'interests', 'availability', 'preferred_time',
                  'commitment_level', 'motivation', 'emergency_contact_name',
                  'emergency_contact_phone', 'emergency_contact_relation']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)

class VolunteerStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Volunteer.STATUS_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True)

class VolunteerAssignmentSerializer(serializers.ModelSerializer):
    volunteer_name = serializers.CharField(source='volunteer.name', read_only=True)
    program_title = serializers.CharField(source='program.title', read_only=True)
    
    class Meta:
        model = VolunteerAssignment
        fields = '__all__'

class VolunteerSummarySerializer(serializers.Serializer):
    total_volunteers = serializers.IntegerField()
    active_volunteers = serializers.IntegerField()
    pending_applications = serializers.IntegerField()
    recent_volunteers = VolunteerSerializer(many=True)