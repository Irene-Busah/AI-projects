from django.contrib import admin
from authentication.models import CustomUser, Patient, Profile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(Profile)


