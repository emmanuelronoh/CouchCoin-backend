from rest_framework import serializers
from .models import Job  # Ensure this import is correct

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
