from django.urls import path
from hospital.views.medical_history import get_medical_history, get_patient_sessions
from hospital.views.session_data import create_session_and_records

urlpatterns = [
    path('medical-history/<str:user_id>/', get_medical_history, name='get-medical-history'),
    path('patient-records/<str:patient_id>/', get_patient_sessions, name='patient-records'),
    path('session-data/', create_session_and_records, name='session-data'),
]