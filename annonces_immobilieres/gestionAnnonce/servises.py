

from .models import Annoncement, Type, Contact, Caregorie, AnnoncementImage, Commune, Location, Wilaya,Address,User,Token, Messages
from .interface import Iannouncement,Iauth
from geopy.geocoders import Nominatim
from validate_email import validate_email
import geopy.geocoders
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
geopy.geocoders.options.default_timeout = 7
import json
import django_filters
from django.db.models import Q





class LocationManager():

    def get_cities():
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
    # get_cities()
    # del get_cities

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

    def modifyLocation(announcement:Annoncement,id_wilaya:int,id_commune:int,addres:str):
        try:
            location= Location.objects.get(id=announcement.location.pk)
            wilaya= Wilaya.objects.get(id=id_wilaya)
            commune= Commune.objects.get(id=id_commune)
            address= Address.objects.get(id=location.address.pk)
        except Wilaya.DoesNotExist or Commune.DoesNotExist or Location.DoesNotExist or Address.DoesNotExist:
            raise ValueError
        location.wilaya=wilaya
        location.commune=commune
        address.address=addres
        address.latitude=LocationManager.get_coordinates(address)["lat"]
        address.longitude=LocationManager.get_coordinates(address)["long"]
        return(location)

    def creatLocation(id_commune:int,id_wilaya:int,address):
        try:
            wilaya= Wilaya.objects.get(id=id_wilaya)
            commune= Commune.objects.get(id=id_commune)
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
        if created:
            Token.objects.create(user=instance)

    def login(email,family_name ,first_name,image):
        if User.objects.filter(email=email).exists() :
            token =Token.objects.get(user=User.objects.get(email=email))
            return (token.key) 
        else :
            is_valid = validate_email(email,verify=True)
            if  is_valid :
                User.objects.create(email=email,first_name=first_name,family_name=family_name,image=image)
                token =Token.objects.get(user=User.objects.get(email=email))
                return (token.key )
            else :
                raise ValueError

    def find_user(token):
        mail= (Token.objects.get(key=token)).user
        return(User.objects.get(email=mail))



class AnnouncemntManager (Iannouncement):

    def create_Announcement(title:str,area:int,price:int,description:str,id_category:int,id_type:int,id_user:int,name:str,last_name:str,personal_address:str,phone:str,id_commune:int,id_wilaya:int,address:str,uploaded_images):
        try:
            category= Caregorie.objects.get(id=id_category)
            type= Type.objects.get(id=id_type)
            user=User.objects.get(id=id_user)
        except Caregorie.DoesNotExist or Type.DoesNotExist or User.DoesNotExist :
            raise ValueError
        
        annonce = Annoncement.objects.create(
        title= title,
        caregorie= category,
        type= type,
        user=user,
        interface= area,
        prix=price,
        description= description,
        deleted =False,
        contact=Contact.objects.create(
            nom= name,
            prenom= last_name,
            adresse= personal_address,
            tele=phone,
        ),
        location=LocationManager.creatLocation(id_commune,id_wilaya,address)
        )
        for img in uploaded_images:
            AnnoncementImage.objects.create(annoncement =annonce,image=img)
        return(annonce)

    def modify_Announcement(title:str,area:int,price:int,description:str,id_category:int,id_type:int,name:str,last_name:str,personal_address:str,phone:str,id_wilaya:int,id_commune:int,id_announcement:int,adress:str):
        try:
            category= Caregorie.objects.get(id=id_category)
            type= Type.objects.get(id=id_type)
            announcement= Annoncement.objects.get(id=id_announcement)
            contact= Contact.objects.get(id=announcement.contact.pk)
        except Caregorie.DoesNotExist or Type.DoesNotExist or Annoncement.DoesNotExist or Contact.DoesNotExist :
                raise ValueError
        if announcement.deleted ==True :
            raise ValueError
        announcement.title= title
        announcement.caregorie= category
        announcement.type= type
        announcement.interface=area
        announcement.prix=price
        announcement.description= description
        contact.nom=name
        contact.prenom=last_name
        contact.adresse=personal_address
        contact.tele=phone
        announcement.contact=contact
        announcement.location=LocationManager.modifyLocation(announcement,id_wilaya,id_commune,adress)
        announcement.save()
        return(announcement)
    
    def delete_announcement(id):
        announcement= Annoncement.objects.get(id=id)
        if announcement.deleted ==True :
            raise ValueError
        else:
            announcement.deleted =True
            announcement.save()
        return ()
    
    def get_announcements():
        return (Annoncement.objects.filter(deleted=False))
    
    def search_filter(search,category,commune,wilaya,type,first_date,second_date):
        annonce = Annoncement.objects.filter(deleted=False)
        m=["imane","h"]
        if search != "":
            annoncement = []
            for keyword in search:
                annoncement = annoncement or annonce.filter(Q(description__contains=keyword) | Q(title__contains=keyword))
            if category != "" or commune != "" or wilaya!="" or type !="" :
                if first_date !="" and  second_date !="":
                    annoncement = annoncement.filter(Q(caregorie__id__in=category) | Q (location__commune__id__in=commune ) | Q( location__wilaya__id__in= wilaya) | Q(type__id__in= type)|Q(creation_date__range=[first_date,second_date ] ) )
                    return (annoncement)
                elif first_date =="" and  second_date =="" :
                    annoncement = annoncement.filter( Q(caregorie__id__in=category) | Q (location__commune__id__in=commune ) | Q( location__wilaya__id__in= wilaya) | Q(type__id__in= type) )
                    return (annoncement)
                else:
                    raise ValueError
            else:
                return (annoncement)

        else :
            if category != "" or commune != "" or wilaya!="" or type !="" :
                if first_date !="" and  second_date !="" :
                    annonce = annonce.filter(caregorie__id__in=category ,location__commune__id__in=commune , location__wilaya__id__in= wilaya ,type__id__in= type,creation_date__range=[first_date,second_date ] ) 
                    return(annonce)
                elif first_date =="" and  second_date =="" :
                    annonce = annonce.filter(caregorie__id__in=category ,location__commune__id__in=commune ,location__wilaya__id__in= wilaya,type__id__in= type) 
                    return(annonce)
                else :
                    raise ValueError
            else:
                return(annonce)
        



class MessagManager():

    # ========COUNTER==========
    # *) Unread recieved messages to a certain user
    def unread_messages(id_user):
        return Messages.objects.filter(status= 'Pending',sent_to=id_user).count()

    # *) creates a new message
    def send_message(sending_user: str, recieving_user: str, content:str):
        try:
            sent_by= User.objects.get(email=sending_user)
            sent_to= User.objects.get(email=recieving_user)
        except User.DoesNotExist:
            raise ValueError
        Messages.objects.create(
            content=content,
            sent_by=sent_by,
            sent_to=sent_to,
        )

    # *) Gets messges logged user recieved messages
    def get_my_messages(user_id):
        try:
            my_messages= Messages.objects.filter(sent_to=user_id)
        except Messages.DoesNotExist:
            raise ValueError
        return my_messages

    # *) Gets logged user sent messages
    def get_sent_messages(user_id):
        try:
            sent_messages= Messages.objects.filter(sent_by=user_id)
        except Messages.DoesNotExist:
            raise ValueError
        return sent_messages
    pass

class FavoriteManager():
    def add_favorate(id_user,id_announcement):
        announcement = Annoncement.objects.get(id=id_announcement)
        user =User.objects.get(id=id_user)
        announcement.favorated_by.add(user.id)

    def remove_favorate(id_user,id_announcement):
        announcement = Annoncement.objects.get(id=id_announcement,deleted=False)
        user =User.objects.get(id=id_user)
        announcement.favorated_by.remove(user.id)
        return ()

    def get_my_favorites(user_id):
        try:
            my_fav= Annoncement.objects.filter(favorated_by=user_id,deleted=False)
        except Annoncement.DoesNotExist:
            raise ValueError
        return my_fav
