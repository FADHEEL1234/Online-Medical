from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    Doctor,
    Appointment,
    Assessment,
    AssessmentQuestion,
    AssessmentResponse,
    CounselingSession,
    Counselor,
    CrisisContact,
    FavoriteQuote,
    JournalEntry,
    MoodEntry,
    MotivationalQuote,
    Notification,
    SelfCarePlanItem,
    WellnessCategory,
    WellnessResource,
)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class UserAdminSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    appointment_count = serializers.IntegerField(source='appointments.count', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
            'last_login',
            'appointment_count',
        ]
        read_only_fields = fields

    def get_full_name(self, obj):
        full_name = obj.get_full_name().strip()
        return full_name or obj.username


# extend simplejwt serializer to include username in the response
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # add additional response fields
        data['username'] = self.user.username
        # include a flag so the frontend can detect an admin/staff user
        data['is_staff'] = self.user.is_staff
        data['is_superuser'] = self.user.is_superuser
        return data


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model."""
    available_days = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=6),
        source='available_days_list',
        required=False,
        allow_empty=True,
        default=list,
    )

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'email', 'phone', 'available_from', 'available_to', 'available_days', 'created_at']
        read_only_fields = ['id', 'created_at']


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model."""
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'user', 'user_name', 'doctor', 'doctor_name', 
            'doctor_specialization', 'appointment_date', 'status', 
            'created_at', 'updated_at'
        ]
        # regular users should never be able to change status directly
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class AppointmentAdminSerializer(AppointmentSerializer):
    """Variant used by admin endpoints that permits changing status."""

    class Meta(AppointmentSerializer.Meta):
        # copy fields but make `status` writable so staff can update it
        read_only_fields = [
            f for f in AppointmentSerializer.Meta.read_only_fields
            if f != 'status'
        ]


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating appointments.  We include the `id` field in
    the response so clients can immediately know the new record's identifier.
    """
    
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'appointment_date']
        read_only_fields = ['id']
    
    def validate(self, data):
        # ensure the appointment is within doctor's availability window
        appt_date = data.get('appointment_date')
        doctor = data.get('doctor')
        from django.utils import timezone
        if appt_date and appt_date < timezone.now():
            raise serializers.ValidationError("Appointment date cannot be in the past")
        if doctor and appt_date:
            # check times
            appt_time = appt_date.time()
            if doctor.available_from and appt_time < doctor.available_from:
                raise serializers.ValidationError("Appointment time is before the doctor's available hours")
            if doctor.available_to and appt_time > doctor.available_to:
                raise serializers.ValidationError("Appointment time is after the doctor's available hours")
            # check weekday availability (0=Monday ... 6=Sunday)
            weekday = appt_date.weekday()
            available_days = getattr(doctor, 'available_days_list', None)
            if available_days is not None and len(available_days) > 0 and weekday not in available_days:
                raise serializers.ValidationError("Doctor is not available on the selected day")
        return data


class CounselorSerializer(serializers.ModelSerializer):
    available_days = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=6),
        source='available_days_list',
        required=False,
        allow_empty=True,
        default=list,
    )

    class Meta:
        model = Counselor
        fields = [
            'id', 'name', 'specialization', 'email', 'phone', 'bio',
            'available_from', 'available_to', 'available_days', 'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class CounselingSessionSerializer(serializers.ModelSerializer):
    counselor_name = serializers.CharField(source='counselor.name', read_only=True)
    counselor_specialization = serializers.CharField(source='counselor.specialization', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CounselingSession
        fields = [
            'id', 'user', 'user_name', 'counselor', 'counselor_name',
            'counselor_specialization', 'session_date', 'reason', 'status',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        session_date = data.get('session_date')
        counselor = data.get('counselor')
        from django.utils import timezone
        if session_date and session_date < timezone.now():
            raise serializers.ValidationError("Session date cannot be in the past")
        if counselor and session_date:
            session_time = session_date.time()
            if session_time < counselor.available_from:
                raise serializers.ValidationError("Session time is before the counselor's available hours")
            if session_time > counselor.available_to:
                raise serializers.ValidationError("Session time is after the counselor's available hours")
            if counselor.available_days_list and session_date.weekday() not in counselor.available_days_list:
                raise serializers.ValidationError("Counselor is not available on the selected day")
        return data


class CounselingSessionAdminSerializer(CounselingSessionSerializer):
    class Meta(CounselingSessionSerializer.Meta):
        read_only_fields = [
            f for f in CounselingSessionSerializer.Meta.read_only_fields
            if f != 'status'
        ]


class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodEntry
        fields = ['id', 'mood', 'intensity', 'notes', 'entry_date', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_intensity(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Intensity must be between 1 and 10")
        return value


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuestion
        fields = ['id', 'assessment', 'text', 'order', 'max_score']


class AssessmentSerializer(serializers.ModelSerializer):
    questions = AssessmentQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = ['id', 'title', 'assessment_type', 'description', 'is_active', 'created_at', 'questions']
        read_only_fields = ['id', 'created_at']


class AssessmentResponseSerializer(serializers.ModelSerializer):
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)

    class Meta:
        model = AssessmentResponse
        fields = ['id', 'assessment', 'assessment_title', 'answers', 'total_score', 'recommendation', 'created_at']
        read_only_fields = ['id', 'total_score', 'recommendation', 'created_at']

    def validate(self, data):
        assessment = data.get('assessment')
        answers = data.get('answers') or {}
        question_ids = set(assessment.questions.values_list('id', flat=True)) if assessment else set()
        for key, value in answers.items():
            try:
                question_id = int(key)
                score = int(value)
            except (TypeError, ValueError):
                raise serializers.ValidationError("Answers must map question ids to numeric scores")
            if question_id not in question_ids:
                raise serializers.ValidationError("Answer contains a question outside this assessment")
            max_score = assessment.questions.get(id=question_id).max_score
            if score < 0 or score > max_score:
                raise serializers.ValidationError("Answer score is outside the allowed range")
        return data

    def create(self, validated_data):
        answers = validated_data.get('answers') or {}
        total = sum(int(score) for score in answers.values())
        validated_data['total_score'] = total
        validated_data['recommendation'] = self.get_recommendation(validated_data['assessment'], total)
        return super().create(validated_data)

    def get_recommendation(self, assessment, score):
        if assessment.assessment_type == 'PHQ9':
            if score >= 20:
                return 'Severe symptoms. Please seek professional support as soon as possible.'
            if score >= 10:
                return 'Moderate symptoms. Consider booking a counseling session.'
            return 'Minimal to mild symptoms. Keep tracking your mood and self-care habits.'
        if assessment.assessment_type == 'GAD7':
            if score >= 15:
                return 'Severe anxiety range. Professional guidance is recommended.'
            if score >= 10:
                return 'Moderate anxiety range. Counseling and relaxation routines may help.'
            return 'Mild anxiety range. Continue monitoring and practicing stress reduction.'
        if score >= 18:
            return 'High stress range. Prioritize rest, support, and a counseling check-in.'
        if score >= 10:
            return 'Moderate stress range. Review your self-care plan and workload.'
        return 'Lower stress range. Keep building healthy routines.'


class WellnessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessCategory
        fields = ['id', 'name', 'description']


class WellnessResourceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = WellnessResource
        fields = [
            'id', 'title', 'category', 'category_name', 'resource_type',
            'summary', 'content', 'url', 'is_featured', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class MotivationalQuoteSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = MotivationalQuote
        fields = ['id', 'text', 'author', 'is_active', 'is_favorite', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.favorites.filter(user=request.user).exists()


class FavoriteQuoteSerializer(serializers.ModelSerializer):
    quote_detail = MotivationalQuoteSerializer(source='quote', read_only=True)

    class Meta:
        model = FavoriteQuote
        fields = ['id', 'quote', 'quote_detail', 'created_at']
        read_only_fields = ['id', 'created_at']


class SelfCarePlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfCarePlanItem
        fields = ['id', 'title', 'item_type', 'target_date', 'reminder_time', 'is_completed', 'created_at']
        read_only_fields = ['id', 'created_at']


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'title', 'body', 'entry_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CrisisContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisisContact
        fields = ['id', 'name', 'phone', 'url', 'description', 'country', 'is_active']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'scheduled_for', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']
