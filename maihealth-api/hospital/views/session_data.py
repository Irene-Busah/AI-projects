from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from hospital.models import Session, Complaint, Prescription, LabTest, Diagnosis, Doctor
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from authentication.models import CustomUser

@api_view(['POST'])
def create_session_and_records(request):
    if request.method == 'POST':

        print(request.data)
        # Extract user information from the request
        doctor_id = request.data.get('doctor_id')

        try:
            # Get the CustomUser associated with the provided doctor_id
            user = CustomUser.objects.get(id=doctor_id)
            print(user)
            doctor = Doctor.objects.get(user=user)
            print(doctor.specialty)
        
            
            # Retrieve the Doctor profile for the user
            # doctor = Doctor.objects.get(user=user)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Doctor not found with the provided user ID'}, status=status.HTTP_404_NOT_FOUND)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor profile not found for the provided user'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get patient information
        patient_id = request.data.get('patient_id')
        
        # Create a new session
        session = Session.objects.create(
            doctor=doctor, 
            patient_id=patient_id,
            start_time=timezone.now()
        )

        # Handle single complaint
        complaint = request.data.get('complaint')
        if complaint:
            Complaint.objects.create(session=session, complaint=complaint)

        # Handle single prescription
        prescription = request.data.get('prescription')
        if prescription:
            Prescription.objects.create(session=session, prescription=prescription)

        # Handle single lab test
        lab_test = request.data.get('lab_test')
        if lab_test:
            LabTest.objects.create(session=session, test=lab_test)

        # Handle diagnoses
        initial_diagnosis = request.data.get('initial_diagnosis')
        final_diagnosis = request.data.get('final_diagnosis')

        if initial_diagnosis:
            Diagnosis.objects.create(session=session, diagnosis=initial_diagnosis, is_final_diagnosis=False)

        if final_diagnosis:
            final_diagnosis_record = Diagnosis.objects.create(session=session, diagnosis=final_diagnosis, is_final_diagnosis=True)
            session.end_time = timezone.now()  # Set end time when final diagnosis is created
            session.save()  # Save session with end time

        return Response({'message': 'Session and records created successfully.', 'session_id': session.id}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)
