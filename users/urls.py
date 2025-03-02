from django.urls import path, include
from .views import (
    RegisterUserView, 
    LoginUserView, 
    VerifyEmailCodeView
)

urlpatterns = [
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # Handles registration
    path('api/auth/', include('dj_rest_auth.urls')),  # Handles login/logout/password reset

    # Keep your custom views
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('verify-email/', VerifyEmailCodeView.as_view(), name='verify_email'),
]
