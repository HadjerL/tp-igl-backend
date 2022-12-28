from rest_framework.decorators import api_view
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from .serilizers import AnnoceSerializer, TypeSerializer, CommuneSerializer, WilayaSerializer
from .models import Annonce, Type, Contact, Caregorie, AnnoncementImage, Commune, Location, Wilaya
import geopy.geocoders
geopy.geocoders.options.default_timeout = 7
from geopy.geocoders import Nominatim


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

class viewsets_commune(viewsets.ModelViewSet):
    queryset=Commune.objects.all()
    serializer_class=CommuneSerializer

class viewsets_type(viewsets.ModelViewSet): 
    queryset=Type.objects.all()
    serializer_class=TypeSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['nom_type']



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
            address=request.data["address"]
        )
        )
    uploaded_images = request.FILES.getlist('uploaded_images')
    for img in uploaded_images:
        AnnoncementImage.objects.create(annoncement =annonce,image=img)
    return Response(status=status.HTTP_201_CREATED) 

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
    except Caregorie.DoesNotExist or Type.DoesNotExist or Wilaya.DoesNotExist or Commune.DoesNotExist or Annonce.DoesNotExist or Contact.DoesNotExist or Location.DoesNotExist:
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
    location.address=request.data["address"]
    uploaded_images = request.FILES.getlist('uploaded_images')
    #ask the others about this later
    for img in uploaded_images:
        AnnoncementImage.objects.create(annoncement =announcement,image=img)
    serializer= AnnoceSerializer(announcement)
    return Response(serializer.data,status=status.HTTP_201_CREATED) 


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
