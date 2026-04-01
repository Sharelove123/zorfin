from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

from .serializers import (
    UserRegistrationSerializer, 
    UserProfileSerializer, 
    UserListSerializer,
    RoleUpdateSerializer,
    StatusUpdateSerializer
)
from .permissions import IsAdminUser

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    Register a new user. The new user will be assigned the 'viewer' role by default.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update the profile of the currently authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """
    List all users. Admin only.
    """
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [IsAdminUser]
    serializer_class = UserListSerializer


class RoleUpdateView(generics.UpdateAPIView):
    """
    Update a user's role. Admin only.
    """
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = RoleUpdateSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class StatusUpdateView(generics.UpdateAPIView):
    """
    Update a user's active status (activate/deactivate). Admin only.
    """
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = StatusUpdateSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
