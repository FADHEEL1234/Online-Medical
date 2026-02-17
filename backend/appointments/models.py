from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    """Model representing a doctor in the system."""
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    # availability window (stored as times)
    available_from = models.TimeField(default='09:00', help_text='Doctor available from this time')
    available_to = models.TimeField(default='17:00', help_text='Doctor available until this time')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

    class Meta:
        ordering = ['name']


class Appointment(models.Model):
    """Model representing an appointment booking."""
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment {self.id} - {self.user.username} with Dr. {self.doctor.name}"

    class Meta:
        ordering = ['-created_at']
