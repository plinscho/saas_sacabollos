"""
Utility functions for user management and profile operations
"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import UserProfile


def create_user_with_profile(username, email, password, role='chapista', phone='', **kwargs):
    """
    Create a user with an associated profile in a single transaction
    
    Args:
        username (str): Username for the user
        email (str): Email address
        password (str): Password (will be hashed)
        role (str): User role (chapista, company, admin)
        phone (str): Phone number (optional)
        **kwargs: Additional User model fields (first_name, last_name, etc.)
    
    Returns:
        UserProfile: Created user profile instance
    
    Raises:
        ValidationError: If username or email already exists
    """
    with transaction.atomic():
        # Check for existing username/email
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"Username '{username}' already exists")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"Email '{email}' already exists")
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
        
        # Create profile
        profile = UserProfile.objects.create(
            user=user,
            role=role,
            phone=phone
        )
        
        return profile


def update_user_email(user, new_email):
    """
    Update user email with uniqueness validation
    
    Args:
        user (User): User instance to update
        new_email (str): New email address
    
    Returns:
        bool: True if successful
    
    Raises:
        ValidationError: If email already exists
    """
    if User.objects.filter(email=new_email).exclude(id=user.id).exists():
        raise ValidationError(f"Email '{new_email}' already exists")
    
    user.email = new_email
    user.save()
    return True


def get_user_by_email(email):
    """
    Get user by email address
    
    Args:
        email (str): Email address to search for
    
    Returns:
        User or None: User instance if found, None otherwise
    """
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def get_users_by_role(role):
    """
    Get all users with a specific role
    
    Args:
        role (str): Role to filter by
    
    Returns:
        QuerySet: UserProfile queryset filtered by role
    """
    return UserProfile.objects.filter(role=role)


def verify_user(user_profile):
    """
    Mark a user as verified
    
    Args:
        user_profile (UserProfile): UserProfile to verify
    
    Returns:
        UserProfile: Updated profile
    """
    user_profile.is_verified = True
    user_profile.save()
    return user_profile


def change_user_role(user_profile, new_role):
    """
    Change user role with validation
    
    Args:
        user_profile (UserProfile): Profile to update
        new_role (str): New role value
    
    Returns:
        UserProfile: Updated profile
    
    Raises:
        ValidationError: If role is invalid
    """
    valid_roles = [choice[0] for choice in UserProfile.ROLE_CHOICES]
    
    if new_role not in valid_roles:
        raise ValidationError(f"Invalid role '{new_role}'. Valid roles: {valid_roles}")
    
    user_profile.role = new_role
    user_profile.save()
    return user_profile


def get_user_full_data(user):
    """
    Get complete user data including profile information
    
    Args:
        user (User): User instance
    
    Returns:
        dict: Complete user data
    """
    try:
        profile = user.userprofile
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'is_active': user.is_active,
            'profile': {
                'role': profile.role,
                'phone': profile.phone,
                'is_verified': profile.is_verified,
                'created_at': profile.created_at,
                'updated_at': profile.updated_at,
            }
        }
    except UserProfile.DoesNotExist:
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'is_active': user.is_active,
            'profile': None
        }


def search_users(query):
    """
    Search users by username, email, first_name, or last_name
    
    Args:
        query (str): Search query
    
    Returns:
        QuerySet: Matching UserProfile instances
    """
    return UserProfile.objects.filter(
        user__username__icontains=query
    ).union(
        UserProfile.objects.filter(user__email__icontains=query)
    ).union(
        UserProfile.objects.filter(user__first_name__icontains=query)
    ).union(
        UserProfile.objects.filter(user__last_name__icontains=query)
    )


def delete_user_and_profile(user):
    """
    Delete user and associated profile
    
    Args:
        user (User): User to delete
    
    Returns:
        bool: True if successful
    """
    with transaction.atomic():
        # Profile will be deleted automatically due to CASCADE
        user.delete()
        return True