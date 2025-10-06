from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import UserProfile
from .serializers import (
    UserRegistrationSerializer, 
    UserProfileSerializer, 
    UserLoginSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user with both User and UserProfile data
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user_profile = serializer.save()
        
        # Create authentication token
        token, created = Token.objects.get_or_create(user=user_profile.user)
        
        # Return user profile data with token
        profile_serializer = UserProfileSerializer(user_profile)
        
        return Response({
            'message': 'User registered successfully',
            'user': profile_serializer.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login user and return authentication token
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            user_profile = UserProfile.objects.get(user=user)
            profile_serializer = UserProfileSerializer(user_profile)
            
            return Response({
                'message': 'Login successful',
                'user': profile_serializer.data,
                'token': token.key
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Get current user's profile
    """
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'User profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """
    Update user profile (both User and UserProfile fields)
    """
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user = request.user
        
        # Update User model fields
        if 'email' in request.data:
            # Check email uniqueness
            if User.objects.filter(email=request.data['email']).exclude(id=user.id).exists():
                return Response({
                    'error': 'Email already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
            user.email = request.data['email']
        
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        
        user.save()
        
        # Update UserProfile fields
        if 'phone' in request.data:
            user_profile.phone = request.data['phone']
        
        if 'role' in request.data and request.data['role'] in dict(UserProfile.ROLE_CHOICES):
            user_profile.role = request.data['role']
        
        user_profile.save()
        
        serializer = UserProfileSerializer(user_profile)
        return Response({
            'message': 'Profile updated successfully',
            'user': serializer.data
        })
        
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'User profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


class UserListView(generics.ListAPIView):
    """
    List all users (admin only)
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Only allow admins to see all users
        if self.request.user.userprofile.role == 'admin':
            return UserProfile.objects.all()
        else:
            # Regular users can only see their own profile
            return UserProfile.objects.filter(user=self.request.user)
