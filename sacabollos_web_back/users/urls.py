from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    
    # Profile management
    path('profile/', views.get_user_profile, name='profile'),
    path('profile/update/', views.update_user_profile, name='update_profile'),
    
    # User listing (admin)
    path('list/', views.UserListView.as_view(), name='user_list'),
]