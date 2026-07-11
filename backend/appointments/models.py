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


class Counselor(models.Model):
    """Mental health counselor profile and availability."""
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    available_from = models.TimeField(default='09:00')
    available_to = models.TimeField(default='17:00')
    available_days = models.CharField(max_length=32, default='0,1,2,3,4')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.specialization}"

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
        self.available_days = ','.join(str(int(v)) for v in values)


class CounselingSession(models.Model):
    STATUS_CHOICES = Appointment.STATUS_CHOICES

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counseling_sessions')
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='sessions')
    session_date = models.DateTimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Session {self.id} - {self.user.username} with {self.counselor.name}"


class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('neutral', 'Neutral'),
        ('good', 'Good'),
        ('great', 'Great'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    intensity = models.PositiveSmallIntegerField(default=5)
    notes = models.TextField(blank=True)
    entry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-entry_date', '-created_at']
        unique_together = ('user', 'entry_date')

    def __str__(self):
        return f"{self.user.username} - {self.entry_date} - {self.mood}"


class Assessment(models.Model):
    TYPE_CHOICES = [
        ('PHQ9', 'PHQ-9'),
        ('GAD7', 'GAD-7'),
        ('STRESS', 'Stress Assessment'),
    ]

    title = models.CharField(max_length=200)
    assessment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class AssessmentQuestion(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    max_score = models.PositiveSmallIntegerField(default=3)

    class Meta:
        ordering = ['assessment', 'order']
        unique_together = ('assessment', 'order')

    def __str__(self):
        return f"{self.assessment.title} Q{self.order}"


class AssessmentResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_responses')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='responses')
    answers = models.JSONField(default=dict)
    total_score = models.PositiveIntegerField(default=0)
    recommendation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.assessment.title} ({self.total_score})"


class WellnessCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class WellnessResource(models.Model):
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('podcast', 'Podcast'),
        ('pdf', 'PDF'),
    ]

    title = models.CharField(max_length=200)
    category = models.ForeignKey(WellnessCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='resources')
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)
    url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class MotivationalQuote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text[:80]


class FavoriteQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_quotes')
    quote = models.ForeignKey(MotivationalQuote, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quote')
        ordering = ['-created_at']


class SelfCarePlanItem(models.Model):
    ITEM_TYPES = [
        ('goal', 'Goal'),
        ('habit', 'Habit'),
        ('meditation', 'Meditation Reminder'),
        ('exercise', 'Exercise Reminder'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='self_care_items')
    title = models.CharField(max_length=200)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    target_date = models.DateField(null=True, blank=True)
    reminder_time = models.TimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_completed', 'target_date', '-created_at']

    def __str__(self):
        return self.title


class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    title = models.CharField(max_length=200)
    body = models.TextField()
    entry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-entry_date', '-updated_at']

    def __str__(self):
        return self.title


class CrisisContact(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=40, blank=True)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('appointment', 'Appointment Reminder'),
        ('mood', 'Mood Reminder'),
        ('assessment', 'Assessment Reminder'),
        ('wellness', 'Wellness Message'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_read', '-created_at']

    def __str__(self):
        return self.title
