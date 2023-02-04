from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from .serilizers import AnnoceSerializer, TypeSerializer, CommuneSerializer, WilayaSerializer,UserSerializer, MessageSerializer, CategorySerializer
from .models import Annoncement, Type, Commune, Wilaya, Messages, Category
from rest_framework.permissions import AllowAny
from gestionAnnonce import servises
from django.shortcuts import get_object_or_404


@api_view(['Post'])
@permission_classes([AllowAny])
def Login(request):
    """
    This view function logs in a user.
    
    Args:
        request: a Request object containing data for login, including "email", "family_name", "first_name", and "image".
        
    Returns:
        A Response object containing the result of the login.
    """
    return Response(servises.AuthManager.login(request.data["email"],request.data["family_name"],request.data["first_name"],request.data["image"]))

@api_view(['GET'])
def user_annocement(request):
    """
    Retrieve the announcement of a specific user.
    
    This function is decorated with the @api_view decorator from the rest_framework package, which indicates that it is a RESTful API view. The ['GET'] argument specifies that the view can only handle HTTP GET requests.
    
    The function retrieves the Annoncement objects that are related to the current user, as specified by the request.user attribute. The user's ID is obtained from the request and used to filter the related Annoncement objects.
    
    The AnnoceSerializer is then used to serialize the filtered Annoncement objects, and the many=True argument is used to indicate that the serializer should handle multiple objects. The serialized data is returned in a Response object, which is a RESTful API response that contains the data and appropriate HTTP status code.
    
    Returns:
        Response: A RESTful API response that contains the serialized data of the related Annoncement objects.
    """

    annonce = Annoncement.objects.filter(
        user__id = request.user.id
        )
    serializer=AnnoceSerializer(annonce ,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_Annocement(request):
    """
    Creates an announcement by using the data provided in the request. 
    
    The following data is expected to be present in the request data:
    - title: Title of the announcement
    - area: Area of the property
    - price: Price of the property
    - description: Description of the property
    - category: Category of the property
    - type: Type of the property
    - user.id: ID of the user creating the announcement
    - firstName: First name of the person creating the announcement
    - lastName: Last name of the person creating the announcement
    - personal_address: Address of the person creating the announcement
    - phoneNumber: Phone number of the person creating the announcement
    - wilaya: Wilaya of the property
    - commune: Commune of the property
    - address: Address of the property
    - images: Images of the property
    - email: Email of the person creating the announcement
    
    Returns:
    - HTTP 201 CREATED: If the announcement is successfully created
    """
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

@api_view(['POST'])
def send_message(request):
    """
    Send a message.
    
    This API allows users to send messages to other users. To use this API, make a POST request 
    with the following parameters:

    - sent_to: The user id of the recipient.
    - content: The content of the message.
    - title: The title of the message.
    
    Returns:
    A serialized representation of the message that was sent, along with a 201 status code.

    Example:
    
    POST /send_message/
    {
        "sent_to": 2,
        "content": "Hello, how are you?",
        "title": "Greeting"
    }
    
    Response:
    
    {
        "id": 1,
        "sent_by": 1,
        "sent_to": 2,
        "content": "Hello, how are you?",
        "title": "Greeting",
        "created_at": "2022-07-24T10:30:00Z"
    }
    
    """
    message= servises.MessagManager.send_message(
        request.user.id,
        request.data['sent_to'],
        request.data['content'],
        request.data['title'],
    )
    serializer= MessageSerializer(message)
    return Response(serializer.data, status= status.HTTP_201_CREATED)

@api_view(['GET'])
def all_announcemnt(request):
    """
    This function implements the all_announcements endpoint that retrieves all the announcements stored in the database.

    URL : /api/announcements/

    Method : GET

    Auth required : No

    Permissions required : None

    Data : None

    Success Response
    Code : 200 OK

    Content :

    perl
    Copy code   
    {
        "id": 1,
        "title": "House for rent",
        "area": 100,
        "price": 1000,
        "description": "A beautiful house for rent",
        "category": {
            "id": 1,
            "cat_name": "Rental"
        },
        "type": {
            "id": 1,
            "type_name": "House"
        },
        "user": {
            "id": 1,
            "email": "john@example.com"
        },
        "created_at": "2022-11-20T10:30:00Z",
        "updated_at": "2022-11-20T10:30:00Z",
        "firstName": "John",
        "lastName": "Doe",
        "personal_address": "1234 Main St.",
        "phoneNumber": "555-555-5555",
        "wilaya": {
            "id": 1,
            "designation": "Algiers"
        },
        "commune": {
            "id": 1,
            "designation": "Baba Hassen"
        },
        "adress": {
            "id": 1,
            "address": "123 Main St."
        }
    }
    Notes
    The response contains all the announcements stored in the database.
    The category field holds the category of the announcement.
    The type field holds the type of the announcement.
    The user field holds the user who posted the announcement.
    The wilaya field holds the wilaya of the announcement.
    The commune field holds the commune of the announcement.
    The adress field holds the address of the announcement.
    """
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


class viewsets_wilayas(viewsets.ModelViewSet):
    """
    This class is a subclass of viewsets.ModelViewSet from the Django Rest Framework library. 

    The serializer_class attribute specifies the serializer class to use for handling serialization and deserialization of the Wilaya model. 
    In this case, the serializer_class is set to WilayaSerializer.

    The search_fields attribute specifies the fields that should be searched when the viewset performs a search operation. 
    In this case, the value ['designation'] indicates that only the designation field of the Wilaya model should be searched.
    """

    queryset=Wilaya.objects.all()
    serializer_class=WilayaSerializer
    search_fields=['designation']

class viewsets_commune(viewsets.ModelViewSet):
    """
    This class is a subclass of viewsets.ModelViewSet from the Django Rest Framework library. 
    
    The serializer_class attribute specifies the serializer class to use for handling serialization and deserialization of commune model. 
    In this case, the serializer_class is set to communeSerializer.

    The search_fields attribute specifies the fields that should be searched when the viewset performs a search operation. 
    In this case, the value ['designation'] indicates that only the designation field of the commune model should be searched.
    """
    queryset=Commune.objects.all()
    serializer_class=CommuneSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['designation']

class viewsets_type(viewsets.ModelViewSet): 
    """
    This class is a subclass of viewsets.ModelViewSet from the Django Rest Framework library. 
    
    The serializer_class attribute specifies the serializer class to use for handling serialization and deserialization of commune model. 
    In this case, the serializer_class is set to TypeSerializer.

    The search_fields attribute specifies the fields that should be searched when the viewset performs a search operation. 
    In this case, the value ['designation'] indicates that only the designation field of the Type model should be searched.
    """
    queryset=Type.objects.all()
    serializer_class=TypeSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['type_name']

class viewsets_category(viewsets.ModelViewSet): 
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['cat_name ']


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

