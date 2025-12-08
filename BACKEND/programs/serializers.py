from rest_framework import serializers
from .models import Program, ProgramUpdate, ProgramBeneficiary

class ProgramSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    duration = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Program
        fields = ['id', 'title', 'slug', 'category', 'short_description', 
                  'description', 'image', 'banner_image', 'start_date', 
                  'end_date', 'location', 'status', 'target_amount', 
                  'current_amount', 'beneficiaries_count', 'volunteers_needed',
                  'features', 'progress_percentage', 'duration', 'is_active',
                  'meta_title', 'meta_description', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

class ProgramUpdateSerializer(serializers.ModelSerializer):
    program_title = serializers.CharField(source='program.title', read_only=True)
    
    class Meta:
        model = ProgramUpdate
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ProgramBeneficiarySerializer(serializers.ModelSerializer):
    program_title = serializers.CharField(source='program.title', read_only=True)
    
    class Meta:
        model = ProgramBeneficiary
        fields = '__all__'
        read_only_fields = ['created_at']

class ProgramSummarySerializer(serializers.Serializer):
    total_programs = serializers.IntegerField()
    active_programs = serializers.IntegerField()
    total_beneficiaries = serializers.IntegerField()
    total_funding_needed = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_funding_received = serializers.DecimalField(max_digits=12, decimal_places=2)
    recent_programs = ProgramSerializer(many=True)