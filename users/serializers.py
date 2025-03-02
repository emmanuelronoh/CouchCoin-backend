# users/serializers.py
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    username = None  # Remove the username field

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['email'] = self.validated_data.get('email', '')
        data['password1'] = self.validated_data.get('password1', '')
        data['password2'] = self.validated_data.get('password2', '')
        return data