from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status,generics,viewsets ,filters
from rest_framework.response import Response
from .serilizers import AnnoceSerializer ,TypeSerializer,ContactSerializer,RegestierSerializer,tokenSerializer
from .models import Annonce , Type,Contact,Caregorie,AnnoncementImage,User,Token

from rest_framework.permissions import AllowAny


# to creat annoucement
@api_view(['Post'])
def create_Annocement(request):
    annonce = Annonce()
    annonce.interface =request.data['area']
    annonce.description=request.data['description']
    annonce.prix=request.data['price']
    type =Type()
    type.pk= request.data['type']
    cat = Caregorie()
    cat.pk =request.data['caregory']
    contacts=Contact()
    contacts.nom =request.data['lastname']
    contacts.prenom =request.data['name']
    contacts.adresse=request.data['address']
    contacts.tele =request.data['phone']
    contacts.save()
    annonce.contact=contacts
    annonce.type=type
    annonce.caregorie =cat
    annonce.save()
    uploaded_images = request.FILES.getlist('uploaded_images')
    for img in uploaded_images:
        AnnoncementImage.objects.create(annoncement =annonce,image=img)
    return Response(status=status.HTTP_201_CREATED) 




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

