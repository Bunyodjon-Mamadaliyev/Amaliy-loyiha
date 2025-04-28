from django.urls import path
from .views import UserRegistrationView, CustomAuthTokenView, UserDetailView, LogoutView

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', CustomAuthTokenView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/user/', UserDetailView.as_view(), name='user-detail'),
]
