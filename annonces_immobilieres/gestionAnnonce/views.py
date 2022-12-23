from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status,generics,viewsets ,filters
from rest_framework.response import Response
from .serilizers import AnnoceSerializer ,TypeSerializer,ContactSerializer
from .models import Annonce , Type,Contact,Caregorie

# to view all announcements
@api_view(['GET'])
def consult_Announcements(request):
    annonce= Annonce.objects.all()
    serializer = AnnoceSerializer(annonce, many=True)
    return Response(serializer.data)


class create_Annocement(generics.CreateAPIView):
    queryset=Annonce.objects.all()
    serializer_class=AnnoceSerializer



# to view one announcement by id
@api_view(['GET'])
def consult_Announcement(request,_id):
    try:
        annonce= Annonce.objects.get(id=id)
    except Annonce.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AnnoceSerializer(annonce)
    return Response(serializer.data)

# to modify annoucement
@api_view(['PUT'])
def modify_Announcement(request,_id):
    try:
        annonce= Annonce.objects.get(id=id)
    except Annonce.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AnnoceSerializer(annonce,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def find_annocement_type(request):
    type=Type.objects.filter(nom_type='vhfg')
    annonce = Annonce.objects.filter(type__id__in = type)
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)



class viewsets_annoncement(viewsets.ModelViewSet):
       queryset=Annonce.objects.all()
       serializer_class=AnnoceSerializer
       
class viewsets_type(viewsets.ModelViewSet): 
    queryset=Type.objects.all()
    serializer_class=TypeSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['nom_type']













    





        



