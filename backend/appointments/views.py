from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Doctor, Appointment
from .serializers import (
    UserRegistrationSerializer, 
    DoctorSerializer, 
    AppointmentSerializer,
    AppointmentCreateSerializer,
    AppointmentAdminSerializer,
    CustomTokenObtainPairSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Return JWT tokens and the username on login."""
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    """API view for user registration."""
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)


class DoctorListView(generics.ListAPIView):
    """API view to list all doctors."""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]


class DoctorCreateView(generics.CreateAPIView):
    """API view for staff to create a new doctor."""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAdminUser]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve / update / delete a doctor (admin only)."""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAdminUser]


class AppointmentListCreateView(generics.ListCreateAPIView):
    """API view to list and create appointments for regular users."""
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentSerializer

    def get_queryset(self):
        # Return only the logged-in user's appointments
        return Appointment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the logged-in user
        serializer.save(user=self.request.user)


class AppointmentAdminListView(generics.ListAPIView):
    """Admin view that lists every appointment in the system."""
    queryset = Appointment.objects.all()
    serializer_class = AppointmentAdminSerializer
    permission_classes = [permissions.IsAdminUser]


class AppointmentAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin can retrieve or update any appointment (e.g. change status)."""
    queryset = Appointment.objects.all()
    serializer_class = AppointmentAdminSerializer
    permission_classes = [permissions.IsAdminUser]


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete an appointment."""
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow users to access their own appointments
        return Appointment.objects.filter(user=self.request.user)


class UserAppointmentsView(APIView):
    """API view to get current user's all appointments."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.filter(user=request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
