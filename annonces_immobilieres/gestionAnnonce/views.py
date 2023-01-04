from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from .serilizers import AnnoceSerializer, TypeSerializer, CommuneSerializer, WilayaSerializer, AddressSerializer, LocationSerializer
from .models import Annoncement, Type, Commune, Location, Wilaya,Address
import geopy.geocoders
geopy.geocoders.options.default_timeout = 7
from geopy.geocoders import Nominatim
from rest_framework.permissions import AllowAny
from gestionAnnonce import servises

#===================================================================================================================
#                                                 FILTERED QUERYSETS
#===================================================================================================================


@api_view(['GET'])
def user_annocement(request,id):
    annonce = Annoncement.objects.filter(
        user__id__iexact = id
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def find_annocement_type(request,type):
    annonce = Annoncement.objects.filter(
        type__nom_type__iexact = type
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def find_annocement_wilaya(request,wilaya):
    annonce = Annoncement.objects.filter(
        location__wilaya__designation__iexact = wilaya
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def find_annocement_commune(request,commune):
    annonce = Annoncement.objects.filter(
        location__commune__designation__iexact=commune
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def find_annocement_category(request,category):
    annonce = Annoncement.objects.filter(
        caregorie__nom_cat=category
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

#===================================================================================================================
#                                                         VIEWSETS
#===================================================================================================================

class viewsets_annoncement(viewsets.ModelViewSet):
    queryset=Annoncement.objects.all()
    serializer_class=AnnoceSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['type__nom_type',
    'location__wilaya__designation',
    'location__commune__designation',
    'caregorie__nom_cat',
    'description',
    'title'
    ]

class viewsets_wilayas(viewsets.ModelViewSet):
    queryset=Wilaya.objects.all()
    serializer_class=WilayaSerializer
    search_fields=['designation']

class viewsets_commune(viewsets.ModelViewSet):
    queryset=Commune.objects.all()
    serializer_class=CommuneSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['designation']

class viewsets_type(viewsets.ModelViewSet): 
    queryset=Type.objects.all()
    serializer_class=TypeSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['nom_type']

class viewsets_address(viewsets.ModelViewSet):
    queryset= Address.objects.all()
    serializer_class=AddressSerializer
    search_fields=['address']

class viewsets_location(viewsets.ModelViewSet):
    queryset= Location.objects.all()
    serializer_class= LocationSerializer
    search_fields=['address__address']


#===================================================================================================================
#                                                 UPDATING AND CREATING
#===================================================================================================================

@api_view(['POST'])
def create_Annocement(request):
    annoncement=servises.AnnouncemntManager.create_Announcement(
        request.data["title"],
        request.data['area'],
        request.data['price'],
        request.data['description'],
        request.data['id_category'],
        request.data['id_type'],
        request.data['id_user'],
        request.data["name"],
        request.data["last_name"],
        request.data["personal_address"],
        request.data["phone"],
        request.data["id_wilaya"],
        request.data["id_commune"],
        request.data["address"],
        request.FILES.getlist('uploaded_images')
        )
    serializer= AnnoceSerializer(annoncement)
    return Response(serializer.data,status=status.HTTP_201_CREATED) 

@api_view(['PUT'])
def modify_Announcement(request,id):
    annoncement=servises.AnnouncemntManager.modify_Announcement(
        request.data["title"],
        request.data['area'],
        request.data['price'],
        request.data['description'],
        request.data['id_category'],
        request.data['id_type'],
        request.data["name"],
        request.data["last_name"],
        request.data["personal_address"],
        request.data["phone"],
        request.data["id_wilaya"],
        request.data["id_commune"],
        id,
        request.data["address"],
       

        )
    serializer= AnnoceSerializer(annoncement)
    return Response(serializer.data,status=status.HTTP_201_CREATED) 
    
        



#===================================================================================================================
#                                              INITIALIZING FUNCTION
#===================================================================================================================
import json
@api_view(['GET'])
def get_cities(request):
    f=open('algeria_cities.json',encoding='UTF-8')
    algeria_cities= json.load(f)
    print(algeria_cities)
    for commune in algeria_cities:
        Wilaya.objects.get_or_create(
                designation=commune["wilaya_name"]
            )
    for commune in algeria_cities:
        Commune.objects.get_or_create(
            designation=commune["commune_name"],
            wilaya=Wilaya.objects.get(
                designation=commune["wilaya_name"]
            )
        )
    return Response({"bird":"duck"})



@api_view(['Post'])
@permission_classes([AllowAny])
def Login(request):
    return Response(servises.AuthManager.login(request.data["email"],request.data["first_name"],request.data["first_name"],request.data["image"]))
   