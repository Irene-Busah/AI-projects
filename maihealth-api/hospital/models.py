import uuid
from django.db import models

class Hospital(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    website = models.URLField()

class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField('authentication.CustomUser', on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)

    # Additional fields for doctor profile
    specialty = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)  # Number of years of experience
    license_number = models.CharField(max_length=50, blank=True, null=True)  # Medical license number
    qualifications = models.TextField(blank=True, null=True)  # Detailed qualifications, degrees, etc.
    bio = models.TextField(blank=True, null=True)  # Short biography or description
    contact_email = models.EmailField(blank=True, null=True)  
    contact_phone = models.CharField(max_length=15, blank=True, null=True)  

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.id}'

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


class Session(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    doctor = models.ForeignKey('hospital.Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ForeignKey('authentication.Patient', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.patient} - {self.id}'

class Complaint(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    complaint = models.TextField()

class Prescription(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    prescription = models.TextField()

class LabTest(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    test = models.TextField()

class Diagnosis(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    is_final_diagnosis = models.BooleanField(default=False)

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    doctor = models.ForeignKey('hospital.Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey('authentication.Patient', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

# Permission model to control access to medical data
class Permission(models.Model):
    session = models.ForeignKey('hospital.Session', on_delete=models.CASCADE)
    doctor = models.ForeignKey('hospital.Doctor', on_delete=models.CASCADE)    
    has_access = models.BooleanField(default=False)                          
    granted_by_patient = models.BooleanField(default=False)