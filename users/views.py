import random
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Temporary storage for verification codes (Replace with a database solution if needed)
VERIFICATION_CODES = {}

# ✅ Register User & Send 6-digit Code
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"error": "All fields (username, email, password) are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email is already registered"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False  # User is inactive until they verify their email
            )

            # Generate 6-digit verification code
            verification_code = str(random.randint(100000, 999999))
            VERIFICATION_CODES[email] = verification_code

            # Send email with the verification code
            subject = "Your Email Verification Code"
            message = f"Your verification code is: {verification_code}"
            
            send_mail(
                subject,
                message,
                'noreply@example.com',  # Replace with your email
                [email],
                fail_silently=False,
            )

            return Response({"message": "User registered successfully. Check your email for the verification code."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Failed to create user: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ Send Verification Code (Resend)
class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "No account found with this email"}, status=status.HTTP_404_NOT_FOUND)

        # Generate and send a new verification code
        verification_code = str(random.randint(100000, 999999))
        VERIFICATION_CODES[email] = verification_code

        subject = "Your Email Verification Code"
        message = f"Your new verification code is: {verification_code}"

        send_mail(
            subject,
            message,
            'noreply@example.com',
            [email],
            fail_silently=False,
        )

        return Response({"message": "A new verification code has been sent to your email"}, status=status.HTTP_200_OK)

# ✅ Verify Email with Code
class VerifyEmailCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        if not email or not code:
            return Response({"error": "Email and verification code are required"}, status=status.HTTP_400_BAD_REQUEST)

        if email not in VERIFICATION_CODES or VERIFICATION_CODES[email] != code:
            return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "No account found with this email"}, status=status.HTTP_404_NOT_FOUND)

        # Activate user
        user.is_active = True
        user.save()

        # Remove the used verification code
        del VERIFICATION_CODES[email]

        return Response({"message": "Email verified successfully. You can now log in."}, status=status.HTTP_200_OK)

# ✅ Login User
class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Both email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
