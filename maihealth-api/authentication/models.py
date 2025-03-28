import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, is_password_usable


# Custom user model to accommodate both patients and doctors
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)

    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient')

    

    def save(self, *args, **kwargs):
        if not is_password_usable(self.password):  # Check if the password is already hashed
            self.password = make_password(self.password)  # Hash the password if it's not already hashed
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name}'


# Patient model linked to CustomUser
class Patient(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user_pin = models.IntegerField()
    user = models.OneToOneField('authentication.CustomUser', on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=20)
    current_location = models.CharField(max_length=50)
    patient_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)

    # Methods to grant or revoke access
    def grant_access(self, session, doctor):
        """Grant access to a doctor for a specific session."""
        from hospital.models import Permission
        permission, created = Permission.objects.get_or_create(session=session, doctor=doctor)
        permission.has_access = True
        permission.granted_by_patient = True
        permission.save()

    def revoke_access(self, session, doctor):
        """Revoke access to a doctor for a specific session."""
        from hospital.models import Permission
        try:
            permission = Permission.objects.get(session=session, doctor=doctor)
            permission.has_access = False
            permission.save()
        except Permission.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.patient_id = 'PAT' + str(uuid.uuid4())[:2].upper()
        super(Patient, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.id}'


# ============================================= The Profile model ========================================================
class Profile(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='profile')
    
    # Medical History
    CHRONIC_CONDITIONS_CHOICES = [
        ('diabetes', 'Diabetes'),
        ('hypertension', 'Hypertension'),
        ('asthma', 'Asthma'),
        ('heart_disease', 'Heart Disease'),
        ('arthritis', 'Arthritis'),
        ('none', 'None'),
        ('other', 'Other'),  # Include an option for other conditions
    ]
    
    chronic_conditions = models.CharField(
        max_length=50,
        choices=CHRONIC_CONDITIONS_CHOICES,
        blank=True,
        null=True
    )
    allergies = models.TextField(blank=True, null=True)  # e.g., "Penicillin"
    has_surgical_history = models.BooleanField(default=False)  # True if the patient has had surgeries
    surgical_details = models.TextField(blank=True, null=True)  # e.g., "Appendectomy in 2020"
    has_previous_hospitalizations = models.BooleanField(default=False)  # True if the patient has been hospitalized
    hospitalization_details = models.TextField(blank=True, null=True)  
    

    # Lifestyle Data
    dietary_restrictions = models.TextField(blank=True, null=True)  # e.g., "Low salt"
    exercise_habits = models.TextField(blank=True, null=True)  # e.g., "Walks 30 mins daily"


    # Insurance Information
    INSURANCE_PROVIDER_CHOICES = [
        ('britam', 'Britam'),
        ('eden_care', 'Eden Care'),
        ('rssb', 'RSSB'),
        ('sanlam', 'Sanlam'),
        ('other', 'Other'),
    ]
    
    insurance_provider = models.CharField(
        max_length=100,
        choices=INSURANCE_PROVIDER_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.patient.user}'