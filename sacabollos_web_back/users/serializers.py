from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration that handles both User and UserProfile creation
    """
    # User model fields
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    
    # UserProfile fields
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='chapista')
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 
                'role', 'phone']
    
    def validate(self, attrs):
        """
        Validate that passwords match and username/email are unique
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Check if username already exists
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username already exists")
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already exists")
        
        return attrs
    
    def create(self, validated_data):
        """
        Create both User and UserProfile instances
        """
        # Remove password_confirm as it's not needed for creation
        validated_data.pop('password_confirm')
        
        # Extract UserProfile specific fields
        role = validated_data.pop('role', 'chapista')
        phone = validated_data.pop('phone', '')
        
        # Create User instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create UserProfile instance
        user_profile = UserProfile.objects.create(
            user=user,
            role=role,
            phone=phone
        )
        
        return user_profile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for reading user profile data
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 
                'is_verified', 'created_at', 'updated_at']


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


