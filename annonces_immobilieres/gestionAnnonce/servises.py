

from .models import Annoncement, Type, Contact, Category, AnnoncementImage, Commune, Location, Wilaya,Address,User,Token, Messages
from .interface import Iannouncement,Iauth
from geopy.geocoders import Nominatim
from validate_email import validate_email
import geopy.geocoders
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
geopy.geocoders.options.default_timeout = 7
from django.core.files.uploadedfile import InMemoryUploadedFile
import json
from django.db.models import Q




class LocationManager():

    def get_cities():
        """
        This function reads from a file 'algeria_cities.json' which contains a list of cities in Algeria, and creates objects in the database for each wilaya and its corresponding commune.
    
        Returns:
        None
        
        Example:
            Suppose the file 'algeria_cities.json' contains the following data:
            [{"wilaya_name": "Algiers","commune_name": "Baba Hassen"},{"wilaya_name": "Oran","commune_name": "Arzew"},{"wilaya_name": "Algiers","commune_name": "Hydra"}]
        
            When the function get_cities() is called, it will create two objects for the two distinct wilayas "Algiers" and "Oran", and two objects for the two communes "Baba Hassen" and "Arzew", linking each commune to its corresponding wilaya.
        """

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
        print(algeria_cities)
    # get_cities()
    # del get_cities

    def get_coordinates(address):
        """
        This function takes a string argument representing an address,
        uses the Nominatim geolocator to retrieve its latitude and longitude,
        and returns them in a dictionary with the keys 'lat' and 'long'.
    
        :param address: str - A string representing an address
        :return: dict - A dictionary with keys 'lat' and 'long' containing the latitude and longitude of the address
    
        Example:
        >>> get_coordinates("1600 Amphitheatre Parkway, Mountain View, CA")
        {'lat': 37.4219999, 'long': -122.0840575}
        """
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


    def creatLocation(commune:str,id_wilaya:int,address):
        """
        This function creates a new Location object by using a commune name, wilaya id, and an address string.
    
        :param commune: The name of the commune where the location is situated.
        :type commune: str
        :param id_wilaya: The id of the wilaya where the location is situated.
        :type id_wilaya: int
        :param address: The address of the location.
        :type address: str
        :return: The newly created Location object.
        :rtype: Location
    
        Example:
        >>> location = createLocation("Oran", 31, "Avenue Hassan Badi, Oran, Algeria")
        >>> print(location.wilaya.designation)
        Oran
        >>> print(location.commune.designation)
        Oran
        >>> print(location.address.address)
        Avenue Hassan Badi, Oran, Algeria
        """

        try:
            wilaya= Wilaya.objects.get(id=id_wilaya)
            commune= Commune.objects.get(designation__iexact  =commune)
        except  Wilaya.DoesNotExist or Commune.DoesNotExist :
            raise ValueError
        location=Location.objects.create(
            wilaya=wilaya,
            commune=commune,
            address=Address.objects.create(
                address= address,
                latitude= LocationManager.get_coordinates(address)["lat"],
                longitude=LocationManager.get_coordinates(address)["long"],
            )
        )
        return(location)

class AuthManager(Iauth):
    #create token to each new user
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        """
        This function creates an authentication token for a user whenever a new user is created.
        :param sender: The sender of the signal (User model)
        :type sender: class
        :param instance: The instance of the User model that triggered the signal
        :type instance: User
        :param created: Boolean indicating if the User instance was just created or not
        :type created: bool
        :param kwargs: Additional keyword arguments
        :type kwargs: dict
        :return: None
    """
        if created:
            Token.objects.create(user=instance)
    
    def login(email,family_name ,first_name,image):
        """
            this function returns a token (if user doesn't exit create user ) 
            :param email: email of user
            :type email: str
            :param family_name: user family_name
            :type family_name: str
            :param first_name: user first_name
            :type first_name: str
            :param image: user profile picture 
            :type image: file
            
            :return: token
            :rtype: str

            example:
            >>> login(email="ki_haissam@esi.dz",family_name="imane" ,first_name="imane",image="")
            b0c4fee72c79e69a878b4d9c0127c5f9404b91a8
        """
        if User.objects.filter(email=email).exists() :
            token =Token.objects.get(user=User.objects.get(email=email))
            return (token.key) 
        else :
            is_valid =validate_email(email)
            if  is_valid :
                User.objects.create(email=email,first_name=first_name,family_name=family_name,image=image)
                token =Token.objects.get(user=User.objects.get(email=email))
                return (token.key )
            else :
                return 500

    def find_user(id):
        """
        This function takes an id as input and returns the User object with the given id.

        :param id: The id of the user to be retrieved.
        :type id: int
        :return: The User object with the given id.
        :rtype: User
        """
        return(User.objects.get(id=id))

class AnnouncemntManager (Iannouncement):

    def create_Announcement(title:str,area:int,price:int,description:str,id_category:int,id_type:int,id_user:int,name:str,last_name:str,personal_address:str,phone:str,id_wilaya:int,commune:str,address:str,uploaded_images,email):
        """
        Creates an announcement.

        :param title: Title of the announcement
        :param area: Area in square meters
        :param price: Price in Algerian dinars
        :param description: Description of the announcement
        :param id_category: Category id of the announcement
        :param id_type: Type id of the announcement
        :param id_user: User id of the announcement's creator
        :param name: First name of the contact person
        :param last_name: Last name of the contact person
        :param personal_address: Address of the contact person
        :param phone: Phone number of the contact person
        :param id_wilaya: Wilaya id of the location
        :param commune: Commune of the location
        :param address: Address of the location
        :param uploaded_images: Images uploaded for the announcement
        :param email: Email of the contact person
        :return: Created announcement object

        :raises: ValueError if category, type, or user with the specified ids does not exist
        """
        try:
            category= Category.objects.get(pk=id_category)
            type= Type.objects.get(id=id_type)
            user=User.objects.get(id=id_user)
        except Category.DoesNotExist or Type.DoesNotExist or User.DoesNotExist :
            raise ValueError
        
        annonce = Annoncement.objects.create(
        title= title,
        category = category,
        type= type,
        user=user,
        area= area,
        price=price,
        description= description,
        deleted =False,
        contact=Contact.objects.create(
            first_name = name,
            family_name = last_name,
            address = personal_address,
            phone =phone,
            mail =email
        ),
        location=LocationManager.creatLocation(commune,id_wilaya,address)
        )
        
        for img in uploaded_images:
            AnnoncementImage.objects.create(annoncement =annonce,image=img)
        return(annonce)

    def delete_announcement(id):
        """
        This function deletes an announcement based on its id (logic deletion).

        :param id: The id of the announcement to be deleted.
        :type id: int
        :return: Returns an empty tuple.
        :raises: Raises ValueError if the announcement has already been deleted.
        """
        announcement= Annoncement.objects.get(id=id)
        if announcement.deleted ==True :
            raise ValueError
        else:
            announcement.deleted =True
            announcement.save()
        return ()
    
    def get_announcements():
        """
        This function retrieves all the announcements that have not been deleted, and orders them by creation date in descending order.
    
        Returns:
            Queryset: A queryset containing the retrieved announcements.
        """
        return (Annoncement.objects.filter(deleted=False))
    
    def get_announcement(id):
        """
        Retrieve an announcement by its id.

        :param id: The id of the announcement to be retrieved.
        :type id: int
        :return: A QuerySet object containing the announcement with the specified id.
        :rtype: QuerySet
        """
        return (Annoncement.objects.filter(deleted=False,id =id))
    
    def search_filter(search,category,commune,wilaya,type,first_date,second_date):
            """
            This function searches and filters through the announcements.

            :param search: List of keywords to search for in the announcements
            :type search: list
            :param category: category id to filter by
            :type category: int
            :param commune: commune id to filter by
            :type commune: int
            :param wilaya:  wilaya id to filter by
            :type wilaya: int
            :param type: type id to filter by
            :type type: int
            :param first_date: Start date to filter by (optional)
            :type first_date: str
            :param second_date: End date to filter by (optional)
            :type second_date: str

            :return: Queryset of filtered and sorted announcements
            :rtype: QuerySet

            """
            annonce = Annoncement.objects.filter(deleted=False).order_by('-creation_date')
            if len (search )!=0:
                annoncement =Annoncement.objects.none()
                for keyword in search:
                    annoncement= annoncement | (annonce.filter(Q(title__iregex=fr"\y({keyword})\y") | Q(description__iregex=fr"\y({keyword})\y")).order_by('-creation_date'))
                annonce =annoncement
            if category != "":
                annonce= annonce.filter(category__id__in=category)
            if type!="":
                annonce= annonce.filter(type__id__in=type)
            if commune != "" :
                annonce= annonce.filter(location__commune__id__in=commune)
            if wilaya!="" :
                annonce=annonce.filter(location__wilaya__id__in=wilaya)
            if first_date!="" :
                if second_date!="":
                    annonce= annonce.filter(creation_date__range=[first_date,second_date ])
                else:
                    annonce= annonce.filter(creation_date__date=first_date)
            elif second_date!="" :
                    annonce= annonce.filter(creation_date__date=second_date)
            return (annonce)

class MessagManager():

    # ========COUNTER==========
    # *) Unread recieved messages to a certain user
    def unread_messages(id_user):
        """
        Returns the count of unread messages sent to a specific user.

        :param id_user: The ID of the user to count unread messages for.
        :type id_user: int

        :return: The number of unread messages sent to the specified user.
        :rtype: int
        """
        return Messages.objects.filter(status= 'Pending',sent_to=id_user).count()

    # *) creates a new message
    def send_message(sending_user:int, recieving_user:int, content:str, title:str):
        """
        This function allows a user to send a message to another user.
    
        Parameters:
            sending_user (int): The id of the user who is sending the message.
            recieving_user (int): The id of the user who will receive the message.
            content (str): The content of the message.
            title (str): The title of the message.
    
        Returns:
            message: The created message object.
    
        Raises:
            ValueError: If either the sending user or the receiving user does not exist.
        """
        try:
            sent_by= User.objects.get(id=sending_user)
            sent_to= User.objects.get(id=recieving_user)
        except User.DoesNotExist:
            raise ValueError
        message =Messages.objects.create(
            content=content,
            sent_by=sent_by,
            sent_to=sent_to,
            title=title,
        )
        return(message)

    # *) Gets messges logged user recieved messages
    def get_my_messages(user_id):
        """
        Get all messages sent to a specific user.

        Parameters:
        user_id (int): The ID of the user to retrieve messages for.

        Returns:
        QuerySet: A QuerySet of the messages sent to the user.

        Raises:
        ValueError: If the user does not exist.
        """
        try:
            my_messages= Messages.objects.filter(sent_to=user_id).order_by('created_at')
        except Messages.DoesNotExist:
            raise ValueError
        return my_messages

    # *) Gets logged user sent messages
    def get_sent_messages(user_id):
        """
        Returns a queryset containing the messages sent by the specified user, ordered by creation date in descending order.

        :param user_id: The ID of the user who sent the messages.
        :type user_id: int
        :return: A queryset containing the messages sent by the specified user.
        :rtype: Queryset
        :raises ValueError: If no messages are found for the specified user.
        """
        try:
            sent_messages= Messages.objects.filter(sent_by=user_id)
        except Messages.DoesNotExist:
            raise ValueError
        return sent_messages
    pass

class FavoriteManager():
    def add_favorate(id_user,id_announcement):
        """
        Adds an announcement to a user's list of favorites.

        Parameters:
        id_user (int): ID of the user.
        id_announcement (int): ID of the announcement.

        Returns:
        Announecement: the announcement added to user list of favourite.
        
        """
        announcement = Annoncement.objects.get(id=id_announcement,deleted=False)
        user =User.objects.get(id=id_user)
        announcement.favorated_by.add(user.id)
        return (announcement)
    
    def remove_favorate(id_user,id_announcement):
        """
        This function removes a specific announcement from the favorites list of a user.

        Parameters:
        id_user (int): The id of the user whose favorites list will be updated.
        id_announcement (int): The id of the announcement to be removed from the user's favorites list.

        Returns:
        None

        Raises:
        ValueError: If the provided id_announcement does not correspond to an existing announcement or the provided id_user does not correspond to an existing user.
        """
        announcement = Annoncement.objects.get(id=id_announcement,deleted=False)
        user =User.objects.get(id=id_user)
        announcement.favorated_by.remove(user.id)
        return ()
    
    def get_my_favorites(user_id):
        """
        This function returns a queryset of the Annoncement objects that are marked as favorites by a specific user. 
    
        Args:
        user_id (int): The ID of the user whose favorite announcements will be retrieved.
    
        Returns:
        QuerySet: A queryset of Annoncement objects that are marked as favorites by the specified user.
    
        Raises:
        ValueError: If there is no Annoncement with the specified user_id or if the Annoncement objects are not marked as favorites by the specified user.
        """
        try:
            my_fav= Annoncement.objects.filter(favorated_by=user_id,deleted=False)
        except Annoncement.DoesNotExist:
            raise ValueError
        return my_fav
