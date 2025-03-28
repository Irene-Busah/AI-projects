from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from authentication.models import Patient, Profile
from authentication.models import CustomUser


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def complete_profile(request):
    if request.method == 'POST':
        # Get user_id from the request data
        user_id = request.data.get('user_id')

        try:
            # Get the user associated with the user_id
            user = CustomUser.objects.get(id=user_id)
            # Get the patient's profile using the user
            patient = Patient.objects.get(user=user)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the profile data to update or create
        profile_data = {
            'chronic_conditions': request.data.get('chronic_conditions', ''),
            'allergies': request.data.get('allergies', ''),
            'has_surgical_history': request.data.get('has_surgical_history', False),
            'surgical_details': request.data.get('surgical_details', ''),
            'has_previous_hospitalizations': request.data.get('has_previous_hospitalizations', False),
            'hospitalization_details': request.data.get('hospitalization_details', ''),
            'dietary_restrictions': request.data.get('dietary_restrictions', ''),
            'exercise_habits': request.data.get('exercise_habits', ''),
            'insurance_provider': request.data.get('insurance_provider', ''),
        }

        # Update or create the profile
        profile, created = Profile.objects.update_or_create(
            patient=patient,
            defaults=profile_data
        )

        return Response({
            'message': 'Profile completed successfully.',
            'profile_id': str(profile.id),
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
