from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serilizers import AnnoceSerializer ,TypeSerializer,ContactSerializer,CaregorieSerializer
from .models import Annonce , Type,Contact,Caregorie


@api_view(['GET'])
def consult_Announcements(request):
    annonce= Annonce.objects.all()
    serializer = AnnoceSerializer(annonce, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_Annocement(request):
    serializer = AnnoceSerializer(data=request.data)
    if serializer.is_valid():
         serializer.save()
         return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def consult_Announcement(request,id):
    try:
          annonce= Annonce.objects.get(id=id)
    except Annonce.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AnnoceSerializer(annonce)
    return Response(serializer.data)



@api_view(['PUT'])
def modify_Announcement(request,id):
    try:
         annonce= Annonce.objects.get(id=id)
    except Annonce.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AnnoceSerializer(annonce,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)













    





        



