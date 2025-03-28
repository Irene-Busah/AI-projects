from django.urls import path
from authentication.views.complete_profile import complete_profile
from authentication.views.login import login
from authentication.views.signup import signup

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    # path('doctor-login/', doctor_login, name='doctor-login'),
    path('complete-profile/', complete_profile, name='complete_profile'),
]