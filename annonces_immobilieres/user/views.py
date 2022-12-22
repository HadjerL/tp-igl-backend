from django.shortcuts import render
from rest_framework import generics
from .serilizers import UserSerializer
from .models import User



class Userprofile(generics.CreateAPIView):
    queryset= User.objects.all()
    serializer_class = UserSerializer

