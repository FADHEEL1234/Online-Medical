from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    AdminNotificationViewSet,
    AnalyticsView,
    AssessmentQuestionViewSet,
    AssessmentResponseViewSet,
    AssessmentViewSet,
    CounselingSessionAdminViewSet,
    CounselingSessionViewSet,
    CounselorViewSet,
    CrisisContactViewSet,
    FavoriteQuoteViewSet,
    JournalEntryViewSet,
    MentalHealthSummaryView,
    MoodEntryViewSet,
    MotivationalQuoteViewSet,
    NotificationViewSet,
    SelfCarePlanItemViewSet,
    UserRegistrationView,
    AdminUserListView,
    DoctorListView,
    DoctorCreateView,
    DoctorDetailView,
    AppointmentListCreateView,
    AppointmentDetailView,
    UserAppointmentsView,
    AppointmentAdminListView,
    AppointmentAdminDetailView,
    WellnessCategoryViewSet,
    WellnessResourceViewSet,
)

router = DefaultRouter()
router.register(r'counselors', CounselorViewSet, basename='counselor')
router.register(r'counseling-sessions', CounselingSessionViewSet, basename='counseling-session')
router.register(r'admin/counseling-sessions', CounselingSessionAdminViewSet, basename='admin-counseling-session')
router.register(r'moods', MoodEntryViewSet, basename='mood')
router.register(r'assessments', AssessmentViewSet, basename='assessment')
router.register(r'assessment-questions', AssessmentQuestionViewSet, basename='assessment-question')
router.register(r'assessment-responses', AssessmentResponseViewSet, basename='assessment-response')
router.register(r'wellness-categories', WellnessCategoryViewSet, basename='wellness-category')
router.register(r'wellness-resources', WellnessResourceViewSet, basename='wellness-resource')
router.register(r'quotes', MotivationalQuoteViewSet, basename='quote')
router.register(r'favorite-quotes', FavoriteQuoteViewSet, basename='favorite-quote')
router.register(r'self-care', SelfCarePlanItemViewSet, basename='self-care')
router.register(r'journal', JournalEntryViewSet, basename='journal')
router.register(r'crisis-contacts', CrisisContactViewSet, basename='crisis-contact')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'admin/notifications', AdminNotificationViewSet, basename='admin-notification')

urlpatterns = [
    # User registration
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    
    # Doctors
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    # admin-only doctor endpoints
    path('doctors/create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    
    # Appointments for regular users
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('my-appointments/', UserAppointmentsView.as_view(), name='user-appointments'),
    
    # admin-only appointment endpoints
    path('admin/appointments/', AppointmentAdminListView.as_view(), name='admin-appointment-list'),
    path('admin/appointments/<int:pk>/', AppointmentAdminDetailView.as_view(), name='admin-appointment-detail'),
    path('mental-health/summary/', MentalHealthSummaryView.as_view(), name='mental-health-summary'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]

urlpatterns += router.urls
