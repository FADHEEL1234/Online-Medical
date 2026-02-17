from django.contrib import admin
from .models import Doctor, Appointment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'specialization', 'email', 'phone', 'created_at']
    search_fields = ['name', 'specialization', 'email']
    list_filter = ['specialization']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'doctor', 'appointment_date', 'status', 'created_at']
    search_fields = ['user__username', 'doctor__name']
    list_filter = ['status', 'appointment_date', 'created_at']
    date_hierarchy = 'appointment_date'
