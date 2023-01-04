

from .models import Annoncement, Type, Contact, Caregorie, AnnoncementImage, Commune, Location, Wilaya,Address,User,Token
from .interface import Iannouncement,Iauth
from geopy.geocoders import Nominatim
from validate_email import validate_email
import geopy.geocoders
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
geopy.geocoders.options.default_timeout = 7
import json





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
    get_cities()
    del get_cities


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

class AnnouncemntManager (Iannouncement):
    #create token to each new user
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
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

class MessagManager():
    pass


