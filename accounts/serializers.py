from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserSkill

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'first_name', 'last_name',
            'phone', 'location', 'preferred_language'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        return attrs

class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = ['id', 'name', 'level', 'years_of_experience', 'is_verified', 'created_at']
        read_only_fields = ['id', 'is_verified', 'created_at']

class UserProfileSerializer(serializers.ModelSerializer):
    user_skills = UserSkillSerializer(many=True, read_only=True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name', 'avatar',
            'bio', 'phone', 'date_of_birth', 'location', 'website',
            'points_balance', 'total_earned_points', 'total_spent_points',
            'rating', 'total_reviews', 'is_verified', 'is_premium',
            'preferred_language', 'user_skills', 'created_at', 'last_active'
        ]
        read_only_fields = [
            'id', 'email', 'points_balance', 'total_earned_points',
            'total_spent_points', 'rating', 'total_reviews', 'is_verified',
            'is_premium', 'created_at', 'last_active'
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'avatar', 'bio', 'phone',
            'date_of_birth', 'location', 'website', 'preferred_language',
            'email_notifications', 'push_notifications'
        ]
