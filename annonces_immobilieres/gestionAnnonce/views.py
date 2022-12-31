from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from .serilizers import AnnoceSerializer, TypeSerializer, CommuneSerializer, WilayaSerializer, AddressSerializer, LocationSerializer,RegestierSerializer,tokenSerializer
from .models import Annonce, Type, Contact, Caregorie, AnnoncementImage, Commune, Location, Wilaya,Address,User,Token
import geopy.geocoders
geopy.geocoders.options.default_timeout = 7
from geopy.geocoders import Nominatim
from rest_framework.permissions import AllowAny

#===================================================================================================================
#                                                 FILTERED QUERYSETS
#===================================================================================================================



@api_view(['GET'])
def find_annocement_type(request,type):
    annonce = Annonce.objects.filter(
        type__nom_type__iexact = type
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def find_annocement_wilaya(request,wilaya):
    annonce = Annonce.objects.filter(
        location__wilaya__designation__iexact = wilaya
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def find_annocement_commune(request,commune):
    annonce = Annonce.objects.filter(
        location__commune__designation__iexact=commune
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def find_annocement_category(request,category):
    annonce = Annonce.objects.filter(
        caregorie__nom_cat=category
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

#===================================================================================================================
#                                                         VIEWSETS
#===================================================================================================================

class viewsets_annoncement(viewsets.ModelViewSet):
    queryset=Annonce.objects.all()
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
    try:
        category= Caregorie.objects.get(id=request.data["category"])
        type= Type.objects.get(id=request.data["type"])
        wilaya= Wilaya.objects.get(id= request.data["wilaya"])
        commune= Commune.objects.get(id= request.data["commune"])
    except Caregorie.DoesNotExist or Type.DoesNotExist or Wilaya.DoesNotExist or Commune.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)
    annonce = Annonce.objects.create(
        title= request.data["title"],
        caregorie= category,
        type= type,
        interface= request.data["area"],
        prix=request.data["price"],
        description= request.data["description"],
        contact=Contact.objects.create(
            nom= request.data["name"],
            prenom= request.data["last_name"],
            adresse= request.data["personal_address"],
            tele=request.data["phone"],
        ),
        location=Location.objects.create(
            wilaya=wilaya,
            commune=commune,
            address=Address.objects.create(
                address= request.data["address"],
                latitude=get_coordinates(request.data["address"])["lat"],
                longitude=get_coordinates(request.data["address"])["long"],
            )
        )
        )
    uploaded_images = request.FILES.getlist('uploaded_images')
    for img in uploaded_images:
        AnnoncementImage.objects.create(annoncement =annonce,image=img)
    serializer= AnnoceSerializer(annonce)
    return Response(serializer.data,status=status.HTTP_201_CREATED) 

@api_view(['PUT'])
def modify_Announcement(request,id):
    try:
        category= Caregorie.objects.get(id=request.data["category"])
        type= Type.objects.get(id=request.data["type"])
        wilaya= Wilaya.objects.get(id= request.data["wilaya"])
        commune= Commune.objects.get(id= request.data["commune"])
        announcement= Annonce.objects.get(id= id)
        contact= Contact.objects.get(id=announcement.contact.id)
        location= Location.objects.get(id=announcement.location.id)
        address= Address.objects.get(id=location.address.id)
    except Caregorie.DoesNotExist or Type.DoesNotExist or Wilaya.DoesNotExist or Commune.DoesNotExist or Annonce.DoesNotExist or Contact.DoesNotExist or Location.DoesNotExist or Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    announcement.title= request.data["title"]
    announcement.caregorie= category
    announcement.type= type
    announcement.interface= request.data["area"]
    announcement.prix=request.data["price"]
    announcement.description= request.data["description"]
    contact.nom=request.data["name"],
    contact.prenom=request.data["last_name"],
    contact.adresse=request.data["personal_address"],
    contact.tele=request.data["phone"],
    location.wilaya=wilaya
    location.commune=commune
    address.address=request.data["address"]
    address.latitude=get_coordinates(request.data["address"])["lat"]
    address.longitude=get_coordinates(request.data["address"])["long"]
    announcement.save()
    uploaded_images = request.FILES.getlist('uploaded_images')
    #ask the others about this later
    for img in uploaded_images:
        AnnoncementImage.objects.create(annoncement =announcement,image=img)
    serializer= AnnoceSerializer(announcement)
    return Response(serializer.data,status=status.HTTP_201_CREATED) 

#===================================================================================================================
#                                                 CALLABLE FUNCTIONS
#===================================================================================================================

def get_coordinates(address):
    geolocator = Nominatim(user_agent="gestionAnnonce")
    location = geolocator.geocode(address)
    latitude= location.latitude
    longitude= location.longitude
    print(location.address)
    data= {
        "lat": latitude,
        "long": longitude
    }
    return data
#===================================================================================================================
#                                                 LOCATION TESTS
#===================================================================================================================
#you give it address and it returns its coordinates
@api_view(['POST'])
def location_coordinates(request):
    geolocator = Nominatim(user_agent="gestionAnnonce")
    location = geolocator.geocode(request.data["address"])
    latitude= location.latitude
    longitude= location.longitude
    print(location.address)
    data= {
        "lat": latitude,
        "long": longitude,
        "address": location.address
    }
    return Response(data)

#you give it coordinates and it returns its address
@api_view(['POST'])
def coordinates_location(request):
    geolocator = Nominatim(user_agent="gestionAnnonce")
    address= geolocator.reverse((request.data["lat"],request.data["long"])).address
    print(address)
    data={
        "address":address
    }
    return Response(data)

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
    if User.objects.filter(email=request.data['email']).exists() :
        token =Token.objects.get(user=User.objects.get(email=request.data['email']))
        return Response(token.key) 
    else :
        User.objects.create(email=request.data['email'])
        token =Token.objects.get(user=User.objects.get(email=request.data['email']))
        return Response(token.key,status=status.HTTP_201_CREATED )

class viewsets_login(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=RegestierSerializer

class viewsets_token(viewsets.ModelViewSet):
    queryset=Token.objects.all()
    serializer_class=tokenSerializer

