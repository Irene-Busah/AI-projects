from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from authentication.models import Patient, CustomUser
from rest_framework.authtoken.models import Token
# from authentication
# from hospital.models import Doctor

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        # Get username or email and password from the request data
        identifier = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')
        print(identifier, password)
    
        # Authenticate the user
        user = authenticate(username=identifier, password=password)
        # user = CustomUser.objects.get(user=user)
        print(user)
        
        if user is not None:
            # Get or create a token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            if user.user_type == 'patient':
            # Return the token and user details
                patient = Patient.objects.get(user=user)
                return Response({
                    'token': token.key,
                    'user_id': str(user.id),
                    'username': user.username,
                    'patient_id': patient.patient_id,
                    'email': user.email,
                    'message': 'Login successful.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'token': token.key,
                    'user_id': str(user.id),
                    'username': user.username,
                    'email': user.email,
                    'message': 'Login successful.'
                }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# from authentication.models import CustomUser

# @api_view(['POST'])
# def doctor_login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     print(f"Username: {username}, Password: {password}")
#     user = authenticate(username=username, password=password)
#     print(user)
    
#     user = CustomUser.objects.filter(username='admin').first()
#     if user:
#         print(user.username, user.password)  # Verify the user exists and check the hashed password

#     if user is not None:
#         # Check if the user is a doctor
#         if user.user_type == 'doctor':
#             # Ensure the doctor profile exists
#             try:
#                 doctor = Doctor.objects.get(user=user)
#             except Doctor.DoesNotExist:
#                 return Response({'error': 'Doctor profile not found'}, status=status.HTTP_404_NOT_FOUND)

#             # Create or get a token for the authenticated doctor
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 'message': 'Login successful',
#                 'token': token.key,
#                 'user_type': user.user_type,
#                 'doctor_id': str(doctor.id)
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'User is not a doctor'}, status=status.HTTP_403_FORBIDDEN)
#     else:
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
