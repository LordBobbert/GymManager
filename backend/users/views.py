from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, TrainerProfile, ClientProfile
from .serializers import UserSerializer, TrainerProfileSerializer, ClientProfileSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only Admins can manage users

class TrainerProfileViewSet(viewsets.ModelViewSet):
    queryset = TrainerProfile.objects.all()
    serializer_class = TrainerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'trainer':
            return TrainerProfile.objects.filter(user=self.request.user)
        elif self.request.user.is_staff:
            return TrainerProfile.objects.all()
        return None

class ClientProfileViewSet(viewsets.ModelViewSet):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'client':
            return ClientProfile.objects.filter(user=self.request.user)
        elif self.request.user.role == 'trainer':
            return ClientProfile.objects.filter(trainer__user=self.request.user)
        elif self.request.user.is_staff:
            return ClientProfile.objects.all()
        return None

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer