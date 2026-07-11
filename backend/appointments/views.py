import random
from datetime import timedelta

from django.db.models import Avg, Count
from django.utils import timezone
from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import (
    Appointment,
    Assessment,
    AssessmentQuestion,
    AssessmentResponse,
    CounselingSession,
    Counselor,
    CrisisContact,
    Doctor,
    FavoriteQuote,
    JournalEntry,
    MoodEntry,
    MotivationalQuote,
    Notification,
    SelfCarePlanItem,
    WellnessCategory,
    WellnessResource,
)
from .serializers import (
    AssessmentQuestionSerializer,
    AssessmentResponseSerializer,
    AssessmentSerializer,
    CounselingSessionAdminSerializer,
    CounselingSessionSerializer,
    CounselorSerializer,
    CrisisContactSerializer,
    FavoriteQuoteSerializer,
    JournalEntrySerializer,
    MoodEntrySerializer,
    MotivationalQuoteSerializer,
    NotificationSerializer,
    SelfCarePlanItemSerializer,
    UserAdminSerializer,
    UserRegistrationSerializer, 
    WellnessCategorySerializer,
    WellnessResourceSerializer,
    DoctorSerializer, 
    AppointmentSerializer,
    AppointmentCreateSerializer,
    AppointmentAdminSerializer,
    CustomTokenObtainPairSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class UserOwnedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)


class AdminUserListView(generics.ListAPIView):
    """Admin view that lists registered users and their login activity."""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAdminUser]


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


class CounselorViewSet(viewsets.ModelViewSet):
    queryset = Counselor.objects.all()
    serializer_class = CounselorSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user and self.request.user.is_staff):
            queryset = queryset.filter(is_active=True)
        return queryset


class CounselingSessionViewSet(UserOwnedViewSet):
    serializer_class = CounselingSessionSerializer

    def get_queryset(self):
        return CounselingSession.objects.filter(user=self.request.user)


class CounselingSessionAdminViewSet(viewsets.ModelViewSet):
    queryset = CounselingSession.objects.all()
    serializer_class = CounselingSessionAdminSerializer
    permission_classes = [permissions.IsAdminUser]


class MoodEntryViewSet(UserOwnedViewSet):
    serializer_class = MoodEntrySerializer

    def get_queryset(self):
        queryset = MoodEntry.objects.filter(user=self.request.user)
        period = self.request.query_params.get('period')
        if period == 'week':
            queryset = queryset.filter(entry_date__gte=timezone.now().date() - timedelta(days=7))
        if period == 'month':
            queryset = queryset.filter(entry_date__gte=timezone.now().date() - timedelta(days=30))
        return queryset


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.prefetch_related('questions').all()
    serializer_class = AssessmentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user and self.request.user.is_staff):
            queryset = queryset.filter(is_active=True)
        return queryset


class AssessmentQuestionViewSet(viewsets.ModelViewSet):
    queryset = AssessmentQuestion.objects.all()
    serializer_class = AssessmentQuestionSerializer
    permission_classes = [permissions.IsAdminUser]


class AssessmentResponseViewSet(UserOwnedViewSet):
    serializer_class = AssessmentResponseSerializer

    def get_queryset(self):
        return AssessmentResponse.objects.filter(user=self.request.user)


class WellnessCategoryViewSet(viewsets.ModelViewSet):
    queryset = WellnessCategory.objects.all()
    serializer_class = WellnessCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class WellnessResourceViewSet(viewsets.ModelViewSet):
    queryset = WellnessResource.objects.select_related('category').all()
    serializer_class = WellnessResourceSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        resource_type = self.request.query_params.get('type')
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(summary__icontains=search)
        if category:
            queryset = queryset.filter(category_id=category)
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        return queryset.distinct()


class MotivationalQuoteViewSet(viewsets.ModelViewSet):
    queryset = MotivationalQuote.objects.all()
    serializer_class = MotivationalQuoteSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user and self.request.user.is_staff):
            queryset = queryset.filter(is_active=True)
        return queryset

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def random(self, request):
        quote_ids = list(self.get_queryset().values_list('id', flat=True))
        if not quote_ids:
            return Response({'detail': 'No quotes available'}, status=status.HTTP_404_NOT_FOUND)
        quote = MotivationalQuote.objects.get(id=random.choice(quote_ids))
        return Response(self.get_serializer(quote).data)


class FavoriteQuoteViewSet(UserOwnedViewSet):
    serializer_class = FavoriteQuoteSerializer

    def get_queryset(self):
        return FavoriteQuote.objects.filter(user=self.request.user).select_related('quote')


class SelfCarePlanItemViewSet(UserOwnedViewSet):
    serializer_class = SelfCarePlanItemSerializer

    def get_queryset(self):
        return SelfCarePlanItem.objects.filter(user=self.request.user)


class JournalEntryViewSet(UserOwnedViewSet):
    serializer_class = JournalEntrySerializer

    def get_queryset(self):
        queryset = JournalEntry.objects.filter(user=self.request.user)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(body__icontains=search)
        return queryset.distinct()


class CrisisContactViewSet(viewsets.ModelViewSet):
    queryset = CrisisContact.objects.all()
    serializer_class = CrisisContactSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user and self.request.user.is_staff):
            queryset = queryset.filter(is_active=True)
        return queryset


class NotificationViewSet(UserOwnedViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class AdminNotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]


class MentalHealthSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        moods = MoodEntry.objects.filter(user=request.user, entry_date__gte=today - timedelta(days=30))
        assessments = AssessmentResponse.objects.filter(user=request.user)[:5]
        sessions = CounselingSession.objects.filter(
            user=request.user,
            session_date__gte=timezone.now(),
        ).order_by('session_date')[:5]
        tips = [
            'Take a two-minute breathing pause between tasks.',
            'Drink water and step outside for natural light today.',
            'Write down one thing that felt manageable today.',
        ]
        return Response({
            'mood_summary': {
                'entries_30_days': moods.count(),
                'average_intensity': moods.aggregate(avg=Avg('intensity'))['avg'] or 0,
                'latest_mood': MoodEntrySerializer(moods.first()).data if moods.exists() else None,
            },
            'assessment_summary': AssessmentResponseSerializer(assessments, many=True).data,
            'upcoming_counseling_sessions': CounselingSessionSerializer(sessions, many=True).data,
            'wellness_tips': tips,
            'unread_notifications': Notification.objects.filter(user=request.user, is_read=False).count(),
        })


class AnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        mood_trends = MoodEntry.objects.filter(user=request.user).values('entry_date', 'mood', 'intensity').order_by('entry_date')
        assessment_trends = AssessmentResponse.objects.filter(user=request.user).values(
            'created_at', 'assessment__assessment_type', 'total_score'
        ).order_by('created_at')
        data = {
            'mood_trends': list(mood_trends),
            'assessment_trends': list(assessment_trends),
            'counseling_statistics': CounselingSession.objects.filter(user=request.user).values('status').annotate(count=Count('id')),
            'appointment_statistics': Appointment.objects.filter(user=request.user).values('status').annotate(count=Count('id')),
        }
        if request.user.is_staff:
            data['admin_totals'] = {
                'users': User.objects.count(),
                'doctors': Doctor.objects.count(),
                'appointments': Appointment.objects.count(),
                'counselors': Counselor.objects.count(),
                'counseling_sessions': CounselingSession.objects.count(),
                'mood_entries': MoodEntry.objects.count(),
                'assessment_responses': AssessmentResponse.objects.count(),
            }
        return Response(data)
