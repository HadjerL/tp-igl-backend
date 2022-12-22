
from django.urls import path 
from .views import Userprofile 

urlpatterns = [
    path('profil/',Userprofile.as_view()),
 
]
