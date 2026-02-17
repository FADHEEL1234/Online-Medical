from django.urls import path
from .views import (
    UserRegistrationView,
    DoctorListView,
    DoctorCreateView,
    DoctorDetailView,
    AppointmentListCreateView,
    AppointmentDetailView,
    UserAppointmentsView,
    AppointmentAdminListView,
    AppointmentAdminDetailView,
)

urlpatterns = [
    # User registration
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    
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
]
