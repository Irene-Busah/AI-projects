from django.contrib import admin
from .models import Hospital, Doctor, Session, Complaint, Prescription, LabTest, Diagnosis, Appointment

# Register your models here
admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Session)
admin.site.register(Complaint)
admin.site.register(Prescription)
admin.site.register(LabTest)
admin.site.register(Diagnosis)
admin.site.register(Appointment)
