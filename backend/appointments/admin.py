from django.contrib import admin
from .models import Doctor, Appointment
from django import forms


class DoctorAdminForm(forms.ModelForm):
    available_days = forms.MultipleChoiceField(
        choices=Doctor.WEEKDAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Select weekdays the doctor is available (0=Monday)'
    )

    class Meta:
        model = Doctor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and getattr(self.instance, 'available_days', None) is not None:
            self.fields['available_days'].initial = self.instance.available_days_list

    def clean_available_days(self):
        data = self.cleaned_data.get('available_days') or []
        return [int(x) for x in data]

    def save(self, commit=True):
        instance = super().save(commit=False)
        # `available_days` comes from clean as list[int]
        vals = self.cleaned_data.get('available_days', [])
        instance.available_days_list = vals
        if commit:
            instance.save()
        return instance


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    form = DoctorAdminForm
    list_display = ['id', 'name', 'specialization', 'email', 'phone', 'created_at']
    search_fields = ['name', 'specialization', 'email']
    list_filter = ['specialization']
    fieldsets = (
        (None, {
            'fields': ('name', 'specialization', 'email', 'phone')
        }),
        ('Availability', {
            'fields': ('available_from', 'available_to', 'available_days')
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'doctor', 'appointment_date', 'status', 'created_at']
    search_fields = ['user__username', 'doctor__name']
    list_filter = ['status', 'appointment_date', 'created_at']
    date_hierarchy = 'appointment_date'
