from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from .serilizers import AnnoceSerializer, TypeSerializer, CommuneSerializer, WilayaSerializer, AddressSerializer, LocationSerializer,UserSerializer, MessageSerializer, CategorySerializer
from .models import Annoncement, Type, Commune, Location, Wilaya,Address, Messages, Category
from rest_framework.permissions import AllowAny
from gestionAnnonce import servises
from django.shortcuts import get_object_or_404

#===================================================================================================================
#                                                 FILTERED QUERYSETS
#===================================================================================================================


@api_view(['GET'])
def user_annocement(request):
    annonce = Annoncement.objects.filter(
        user__id = request.user.id
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def find_annocement_type(request,type):
    annonce = Annoncement.objects.filter(
        type__type_name__iexact = type
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
        category__cat_name =category
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

#===================================================================================================================
#                                                         VIEWSETS
#===================================================================================================================

class viewsets_annoncement(viewsets.ModelViewSet):
    queryset=Annoncement.objects.all().order_by('creation_date')
    serializer_class=AnnoceSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['type__type_name',
    'location__wilaya__designation',
    'location__commune__designation',
    'category__cat_name ',
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
    search_fields=['type_name']

class viewsets_category(viewsets.ModelViewSet): 
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['cat_name ']

class viewsets_address(viewsets.ModelViewSet):
    queryset= Address.objects.all()
    serializer_class=AddressSerializer
    search_fields=['address']

class viewsets_location(viewsets.ModelViewSet):
    queryset= Location.objects.all()
    serializer_class= LocationSerializer
    search_fields=['address__address']

class viewsets_message(viewsets.ModelViewSet):
    queryset= Messages.objects.all()
    serializer_class= MessageSerializer
    search_fields=['content','sent_by','sent_to']

    def retrieve(self, request, pk=None):
        queryset = Messages.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.status='Read'
        user.save()
        serializer = MessageSerializer(user)
        return Response(serializer.data)

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
        request.data['category'],
        request.data['type'],
        request.user.id,
        request.data["firstName"],
        request.data["lastName"],
        request.data["personal_address"],
        request.data["phoneNumber"],
        request.data["wilaya"],
        request.data["commune"],
        request.data["adress"],
        request.FILES.getlist('images'),
        request.data["email"],
        

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
        request.FILES.getlist('images'),
        request.data["address"],
       
        )
    serializer= AnnoceSerializer(annoncement)
    return Response(serializer.data,status=status.HTTP_201_CREATED) 

@api_view(['POST'])
def send_message(request):
    message= servises.MessagManager.send_message(
        request.data['sent_by'],
        request.data['sent_to'],
        request.data['content']
    )
    serializer= MessageSerializer(message)
    return Response(serializer.data, status= status.HTTP_201_CREATED)

@api_view(['Post'])
@permission_classes([AllowAny])
def Login(request):
    return Response(servises.AuthManager.login(request.data["email"],request.data["family_name"],request.data["first_name"],request.data["image"]))


@api_view(['GET'])
def all_announcemnt(request):
    annonce =servises.AnnouncemntManager.get_announcements()
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)


@api_view(['GET']) 
def delete_announcemnt(request,id):   
    servises.AnnouncemntManager.delete_announcement(id)
    return Response(status=status.HTTP_200_OK)

@api_view(['GET']) 
def find_user(request):
    user =servises.AuthManager.find_user(request.user.id)
    serializer=UserSerializer(user ,many=False)
    return Response(serializer.data)

@api_view(['post'])
def add_favorate(request):
    servises.FavoriteManager.add_favorate(request.user.id,request.data["id_announcement"])
    return Response(status=status.HTTP_200_OK)


@api_view(['post'])
def remove_favorate(request):
    servises.FavoriteManager.remove_favorate(request.user.id,request.data["id_announcement"])
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def search_filter(request) :
    annonce = servises.AnnouncemntManager.search_filter(
        request.data["search"],
        request.data["category"],
        request.data["commune"],
        request.data["wilaya"],
        request.data["type"],
        request.data["first_date"],
        request.data["second_date"],)
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_recieved_messages(request):
    messages= servises.MessagManager.get_my_messages(request.user.id)
    serializer=MessageSerializer(messages, many=True)
    data={
        "nb_unread_messages":servises.MessagManager.unread_messages(request.user.id),
        "recieved_messages":serializer.data
    }
    return Response(data)

@api_view(['GET'])
def get_sent_messages(request):
    messages= servises.MessagManager.get_sent_messages(request.user.id)
    serializer= MessageSerializer(messages,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_my_fav(request):
    fav= servises.FavoriteManager.get_my_favorites(request.user.id)
    serializer= AnnoceSerializer(fav,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_announcement(request,id):
    annonce =servises.AnnouncemntManager.get_announcement(id)
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)