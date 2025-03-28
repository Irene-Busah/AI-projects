# from rest_framework import serializers
# from authentication.models import CustomUser
# from authentication.models import Patient

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['firstname', 'lastname', 'email', 'phone_number', 'gender', 'username', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = CustomUser(**validated_data)
#         user.set_password(validated_data['password'])
#         user.save()
#         return user

# class PatientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Patient
#         fields = '__all__'

from rest_framework import serializers
from hospital.models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'  

