from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from hospital.models import Session, Doctor
from authentication.serializer import SessionSerializer
from authentication.models import Patient, CustomUser
from django.utils.timezone import now

@api_view(['GET'])
def get_medical_history(request, user_id):
    try:
        # Get the user associated with the user_id from the URL
        user = CustomUser.objects.get(id=user_id)

        # Get the patient's profile using the user
        patient = Patient.objects.get(user=user)

        # Fetch sessions for the patient and include related data
        medical_history = Session.objects.filter(patient=patient).prefetch_related(
            'complaint_set',
            'prescription_set',
            'labtest_set',
            'diagnosis_set',
            'doctor'
        )

        if medical_history.exists():
            # Prepare the data structure to serialize
            medical_history_data = []
            for session in medical_history:
                session_data = {
                    'session_id': str(session.id),
                    'doctor': {
                        'firstname': session.doctor.user.first_name, 
                        'lastname': session.doctor.user.last_name, 
                        'specialty': session.doctor.specialty 
                    },
                    'start_time': session.start_time,
                    'end_time': session.end_time,
                    'complaints': [complaint.complaint for complaint in session.complaint_set.all()],
                    'prescriptions': [prescription.prescription for prescription in session.prescription_set.all()],
                    'lab_tests': [lab_test.test for lab_test in session.labtest_set.all()],
                    'diagnoses': [{
                        'diagnosis': diagnosis.diagnosis,
                        'is_final': diagnosis.is_final_diagnosis
                    } for diagnosis in session.diagnosis_set.all()]
                }
                medical_history_data.append(session_data)

            return Response(medical_history_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No medical history found for this patient."}, status=status.HTTP_404_NOT_FOUND)

    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @api_view(['POST'])
# def create_session(request):
#     if request.method == 'POST':
#         doctor_id = request.data.get('doctor_id')
#         patient_id = request.data.get('patient_id')
#         start_time = now()
#         end_time = request.data.get('end_time')

        
#         # Check if doctor and patient exist
#         try:
#             doctor = Doctor.objects.get(id=doctor_id)
#             patient = Patient.objects.get(id=patient_id)
#         except Doctor.DoesNotExist:
#             return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Patient.DoesNotExist:
#             return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         # Create session
#         session = Session.objects.create(
#             doctor=doctor,
#             patient=patient,
#             start_time=start_time,
#             end_time=end_time
#         )
        
#         return Response({
#             'session_id': session.id,
#             'doctor': doctor.user.first_name,
#             'patient': patient.user.first_name,
#             'start_time': session.start_time,
#             'end_time': session.end_time
#         }, status=status.HTTP_201_CREATED)


# ======================================== GETTING PATIENT'S DETAILS FOR DOCTOR =================================================

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_patient_sessions(request, patient_id):
    try:
        # Get the patient based on the unique patient_id
        patient = Patient.objects.get(patient_id=patient_id)

        # Fetch related data using select_related and prefetch_related, and order by start_time descending
        sessions = Session.objects.filter(patient=patient) \
            .select_related('doctor') \
            .prefetch_related(
                'complaint_set', 
                'prescription_set', 
                'labtest_set', 
                'diagnosis_set'
            ) \
            .order_by('-start_time')  # Sort by start_time in descending order

        # Structure the response data
        session_data = []
        for session in sessions:
            complaints = session.complaint_set.all()
            prescriptions = session.prescription_set.all()
            lab_tests = session.labtest_set.all()
            diagnoses = session.diagnosis_set.all()

            session_data.append({
                'session_id': str(session.id),
                'doctor': {
                    'id': str(session.doctor.id),
                    'name': f"{session.doctor.user.first_name} {session.doctor.user.last_name}",
                    'hospital': str(session.doctor.hospital.name) if session.doctor.hospital else None,
                    'specialty': session.doctor.specialty,
                    'years_of_experience': session.doctor.years_of_experience,
                    'license_number': session.doctor.license_number,
                    'contact_email': session.doctor.contact_email,
                    'contact_phone': session.doctor.contact_phone,
                },
                'start_time': session.start_time,
                'end_time': session.end_time,
                'complaints': [complaint.complaint for complaint in complaints],
                'prescriptions': [prescription.prescription for prescription in prescriptions],
                'lab_tests': [lab_test.test for lab_test in lab_tests],
                'diagnoses': [{'diagnosis': diagnosis.diagnosis, 'is_final_diagnosis': diagnosis.is_final_diagnosis} for diagnosis in diagnoses]
            })

        # Fetch patient profile details if it exists
        profile = patient.profile

        # Structure the patient data
        patient_data = {
            'id': str(patient.id),
            'patient_id': patient.patient_id,
            'firstname': patient.user.first_name,
            'lastname': patient.user.last_name,
            'phone_number': patient.user.phone_number,
            'gender': patient.user.gender,
            'user_pin': patient.user_pin,
            'date_of_birth': patient.date_of_birth,
            'nationality': patient.nationality,
            'current_location': patient.current_location,
            'profile': {
                'chronic_conditions': profile.chronic_conditions,
                'allergies': profile.allergies,
                'has_surgical_history': profile.has_surgical_history,
                'surgical_details': profile.surgical_details,
                'has_previous_hospitalizations': profile.has_previous_hospitalizations,
                'hospitalization_details': profile.hospitalization_details,
                'dietary_restrictions': profile.dietary_restrictions,
                'exercise_habits': profile.exercise_habits,
                'insurance_provider': profile.insurance_provider,
            }
        }

        return Response({'patient': patient_data, 'sessions': session_data}, status=status.HTTP_200_OK)

    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
