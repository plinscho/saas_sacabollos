"""
Example usage of the user registration and management system

This file demonstrates how to use the sign-up mechanism and manipulate user data
"""

# Example API Usage:

# 1. REGISTER A NEW USER
"""
POST /api/users/register/
Content-Type: application/json

{
    "username": "john_chapista",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "chapista",
    "phone": "+1234567890"
}

Response:
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "john_chapista",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "chapista",
        "phone": "+1234567890",
        "is_verified": false,
        "created_at": "2025-10-06T10:30:00Z",
        "updated_at": "2025-10-06T10:30:00Z"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
"""

# 2. LOGIN USER
"""
POST /api/users/login/
Content-Type: application/json

{
    "username": "john_chapista",
    "password": "securepassword123"
}

Response:
{
    "message": "Login successful",
    "user": { ... user data ... },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
"""

# 3. GET USER PROFILE (Authenticated)
"""
GET /api/users/profile/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

Response:
{
    "id": 1,
    "username": "john_chapista",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "chapista",
    "phone": "+1234567890",
    "is_verified": false,
    "created_at": "2025-10-06T10:30:00Z",
    "updated_at": "2025-10-06T10:30:00Z"
}
"""

# 4. UPDATE USER PROFILE (Authenticated)
"""
PUT /api/users/profile/update/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json

{
    "email": "newemail@example.com",
    "first_name": "Johnny",
    "phone": "+9876543210"
}

Response:
{
    "message": "Profile updated successfully",
    "user": { ... updated user data ... }
}
"""


# Python Code Examples using the utility functions:

from users.utils import (
    create_user_with_profile,
    update_user_email,
    get_user_by_email,
    get_users_by_role,
    verify_user,
    change_user_role,
    get_user_full_data
)
from users.models import UserProfile
from django.core.exceptions import ValidationError

def example_user_creation():
    """Example of creating users programmatically"""
    
    # Create a chapista user
    chapista_profile = create_user_with_profile(
        username="maria_chapista",
        email="maria@example.com",
        password="securepass123",
        role="chapista",
        phone="+1111111111",
        first_name="Maria",
        last_name="Garcia"
    )
    
    # Create a company user
    company_profile = create_user_with_profile(
        username="autofix_company",
        email="contact@autofix.com",
        password="companypass123",
        role="company",
        phone="+2222222222",
        first_name="AutoFix",
        last_name="Company"
    )
    
    return chapista_profile, company_profile


def example_user_manipulation():
    """Example of manipulating user data"""
    
    # Get user by email
    user = get_user_by_email("maria@example.com")
    if user:
        # Get full user data
        full_data = get_user_full_data(user)
        print("User data:", full_data)
        
        # Update email
        try:
            update_user_email(user, "maria.new@example.com")
            print("Email updated successfully")
        except ValidationError as e:
            print(f"Email update failed: {e}")
        
        # Verify user
        profile = user.userprofile
        verify_user(profile)
        print("User verified")
        
        # Change role
        try:
            change_user_role(profile, "admin")
            print("Role changed to admin")
        except ValidationError as e:
            print(f"Role change failed: {e}")


def example_queries():
    """Example queries for user data"""
    
    # Get all chapistas
    chapistas = get_users_by_role("chapista")
    print(f"Found {chapistas.count()} chapistas")
    
    # Get all companies
    companies = get_users_by_role("company")
    print(f"Found {companies.count()} companies")
    
    # Get verified users
    verified_users = UserProfile.objects.filter(is_verified=True)
    print(f"Found {verified_users.count()} verified users")
    
    # Access user data through the relationship
    for profile in UserProfile.objects.all():
        print(f"User: {profile.user.username}")
        print(f"Email: {profile.user.email}")
        print(f"Role: {profile.role}")
        print(f"Phone: {profile.phone}")
        print(f"Verified: {profile.is_verified}")
        print("---")


# Frontend Integration Examples:

def frontend_registration_example():
    """
    Example JavaScript code for frontend registration
    """
    return """
    // Register new user
    const registerUser = async (userData) => {
        try {
            const response = await fetch('/api/users/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Store token for authenticated requests
                localStorage.setItem('authToken', data.token);
                localStorage.setItem('userData', JSON.stringify(data.user));
                return { success: true, data };
            } else {
                return { success: false, errors: data };
            }
        } catch (error) {
            return { success: false, error: error.message };
        }
    };
    
    // Usage
    const userData = {
        username: 'testuser',
        email: 'test@example.com',
        password: 'securepass123',
        password_confirm: 'securepass123',
        first_name: 'Test',
        last_name: 'User',
        role: 'chapista',
        phone: '+1234567890'
    };
    
    registerUser(userData).then(result => {
        if (result.success) {
            console.log('User registered:', result.data);
            // Redirect to dashboard or show success message
        } else {
            console.log('Registration failed:', result.errors);
            // Show error messages to user
        }
    });
    """


def frontend_authenticated_request_example():
    """
    Example JavaScript code for making authenticated requests
    """
    return """
    // Make authenticated API requests
    const makeAuthenticatedRequest = async (url, options = {}) => {
        const token = localStorage.getItem('authToken');
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        };
        
        const finalOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };
        
        return fetch(url, finalOptions);
    };
    
    // Get user profile
    const getUserProfile = async () => {
        try {
            const response = await makeAuthenticatedRequest('/api/users/profile/');
            return await response.json();
        } catch (error) {
            console.error('Failed to get profile:', error);
        }
    };
    
    // Update profile
    const updateProfile = async (updateData) => {
        try {
            const response = await makeAuthenticatedRequest('/api/users/profile/update/', {
                method: 'PUT',
                body: JSON.stringify(updateData)
            });
            return await response.json();
        } catch (error) {
            console.error('Failed to update profile:', error);
        }
    };
    """


if __name__ == "__main__":
    print("User Registration and Management System")
    print("=" * 50)
    print()
    print("This system provides:")
    print("1. User registration with custom profile fields")
    print("2. Authentication using tokens")
    print("3. Profile management endpoints")
    print("4. Utility functions for programmatic user management")
    print()
    print("Check the API endpoints and code examples above!")