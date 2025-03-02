from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth import views as auth_views
from users.views import RegisterUserView, LoginUserView, VerifyEmailCodeView

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin Panel

    # ✅ Authentication URLs (dj_rest_auth)
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # ✅ User Registration & Verification
    path('api/auth/register/', RegisterUserView.as_view(), name='register'),
    path('api/auth/verify-email/', VerifyEmailCodeView.as_view(), name='verify_email'),

    # ✅ User Login
    path('api/auth/login/', LoginUserView.as_view(), name='login'),

    # ✅ Include user-defined app URLs
    path('api/users/', include('users.urls')),  # Routes for the users app
    path('api/jobs/', include('jobs.urls')),  # Routes for the jobs app

    # ✅ Password reset using Django's built-in auth views
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), 
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),

    # ✅ REST API Password reset (for frontend use)
    path('api/auth/password/reset/', PasswordResetView.as_view(), name='api_password_reset'),
    path('api/auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='api_password_reset_confirm'),
]
