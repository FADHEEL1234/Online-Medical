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
    # days of week when the doctor is available. Stored as comma-separated weekday numbers (0=Monday)
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    available_days = models.CharField(max_length=32, default='0,1,2,3,4', help_text='Comma separated weekdays as numbers 0=Monday')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

    class Meta:
        ordering = ['name']

    @property
    def available_days_list(self):
        if not self.available_days:
            return []
        try:
            return [int(x) for x in self.available_days.split(',') if x != '']
        except ValueError:
            return []

    @available_days_list.setter
    def available_days_list(self, values):
        # Expect an iterable of ints or strings; normalize and store comma-separated
        vals = [str(int(v)) for v in values]
        self.available_days = ','.join(vals)


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
