from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['email','username','password']
        extra_kwargs = {"password": {"write_only": True}} 

    def validate_password(self, input):
        if len(input) < 8:
            raise serializers.ValidationError("Password is too short")
        return input
    def create(self, validated_data):
        """✅ Create user"""
        return User.objects.create_user(**validated_data)
