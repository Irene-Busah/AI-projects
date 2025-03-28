from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from authentication.models import CustomUser
from rest_framework.authtoken.models import Token
from authentication.models import CustomUser, Patient
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from hospital.models import Doctor
import requests

token='eyJhbGciOiJIUzUxMiJ9.eyJpZCI6InVzZXJfMDFKOFdQWTUyRzRBTVJWNDRDNFg2VzcxQlIiLCJyZXZva2VkX3Rva2VuX2NvdW50IjowLCJpYXQiOjE3Mjc1NDA0NjMsImV4cCI6MTgyMjE0ODQ2M30.EC7BkUptAxMCbeRBLIq_7S-BCaq9yTP4hU7YpcsFhskBqcwqwphxgn5ZD0DO7NMhqMiVstZVeBWe8CCQRr8Fsw'
headers = {'Authorization': 'Bearer ' + token}


def send_sms(data):
    url = 'https://api.pindo.io/v1/sms/'
    response = requests.post(url, json=data, headers=headers)
    return response


@api_view(['POST'])
def verify_doctor(request):
    """
        Verify if the username and temporary password are correct.
    """
    username = request.data.get('username')
    temp_password = request.data.get('password')

    user = authenticate(username=username, password=temp_password)

    if user is not None and user.user_type == 'doctor':  # Ensure the user is a doctor
        return Response({'message': 'Credentials verified. Please change your password.'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_doctor_password(request):
    """
    Allow the doctor to change their password after verification.
    """
    user = request.user  # This assumes that the user has been authenticated via token/session
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if new_password and confirm_password:
        if new_password == confirm_password:
            user.password = make_password(new_password)  # Hash the new password
            user.save()
            return Response({'message': 'Password changed successfully!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Please provide both new_password and confirm_password.'}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def signup(request):
    """
        Sign up a new user and create a patient profile.
    """

    # Collecting basic user data and patient details from the request
    data = request.data
    try:
        user = CustomUser.objects.create(
            first_name=data['first_name'],  
            last_name=data['last_name'],
            username=data['first_name'].lower(),     
            email=data['email'],
            phone_number=data['phone_number'],
            gender=data['gender'],
            user_type=data.get('user_type', 'patient')
        )
        user.set_password(data['password'])
        user.save()

        # Creating patient profile
        if user.user_type == 'patient':
            patient = Patient.objects.create(
                user=user,
                user_pin=data['user_pin'],
                date_of_birth=data['date_of_birth'],
                nationality=data.get('nationality', ''), 
                current_location=data.get('current_location', ''),
            )
            message = f'''Welcome to mAIhealth App!\n\nUnique Patient ID: {patient.patient_id}\n\n
                Kindly keep it safe and use it each time you visit the doctor\n\n\nThank you! 
                Responsible Health,     Our     Priority\n\nmAiHealth'''
            data = {'to' : "+25"+patient.user.phone_number, 'text' : message, 'sender' : 'PindoTest'}
            send_sms(data=data)

            # Generate authentication token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
            'token': token.key,
            'user_id': user.id,
            'patient_id': patient.patient_id,
            'message': 'User registered successfully.'
        }, status=status.HTTP_201_CREATED)
            
        else:
            doctor = Doctor.objects.create(user=user)
            message = f'''Welcome to mAIhealth App!\nUsername: {doctor.user.username}\nTemporary Password: {data['password']}\n\n
                        Kindly login with these credentials to change your password\n\n\n
                        Thank you! Responsible Health, Our Priority\nmAiHealth'''
            data = {'to' : "+25"+doctor.user.phone_number, 'text' : message, 'sender' : 'PindoTest'}
            send_sms(data=data)

            # Generate authentication token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
            'token': token.key,
            'user_id': user.id,
            'message': 'User registered successfully.'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)