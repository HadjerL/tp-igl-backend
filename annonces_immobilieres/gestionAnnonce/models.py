from django.db import models
from smart_selects.db_fields import ChainedForeignKey 
from phone_field import PhoneField
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


class Caregorie(models.Model):
    nom_cat = models.CharField(max_length=20)
    def __str__(self):
        return self.nom_cat

class Type(models.Model):
    nom_type = models.CharField(max_length=20)
    def __str__(self):
        return self.nom_type

class Contact(models.Model):
    nom = models.CharField(max_length=35)
    prenom = models.CharField(max_length=35)
    adresse = models.CharField(max_length=50)
    tele = PhoneField()
    def __str__(self):
        return self.prenom
# Location = wilaya + communes + address
# wilaya = commune+
#address= address + coordinates
class Wilaya(models.Model):
    designation = models.CharField(max_length=35, unique=True)
    def __str__(self):
        return self.designation

class Commune(models.Model):
    designation = models.CharField(max_length=35)
    wilaya = models.ForeignKey( #each commune has one wilaya
        Wilaya,
        on_delete=models.PROTECT,
        default=None,
        related_name= 'commune',
        )
    def __str__(self):
        return self.designation

class Address(models.Model):
    address= models.CharField(max_length=50,default='')
    latitude= models.DecimalField(decimal_places=7, max_digits= 9)
    longitude= models.DecimalField(decimal_places=7, max_digits= 10)
    def __str__(self):
        return self.address

class Location(models.Model):
    wilaya = models.ForeignKey( #each localization has one wilaya
        Wilaya,
        on_delete= models.CASCADE,
        default=None,
        related_name='location',
        )
    commune = ChainedForeignKey( #to get only and all communes in a wilaya
        Commune,
        chained_field="wilaya", #the field in commune where to find wilaya id
        chained_model_field="wilaya",
        show_all=False, #only show commune corresponding to selected wilaya
        on_delete= models.CASCADE,
        default=None,
        related_name= 'location',
        auto_choose= True,
        )
    address = models.OneToOneField(
        Address,
        default=None,
        on_delete=models.CASCADE,
        related_name='location',
    )
    def __str__(self):
        return self.address.address

class UserManager(BaseUserManager):
    def create_user(self,email ,password=None,**extra_fields ):
        if email is None:
            raise TypeError('Users should have an Email')
        user = self.model(email=self.normalize_email(email),is_staff=False , is_active=True,is_superuser=False,date_joined=timezone.now(),last_login=timezone.now() ,**extra_fields)
        user.set_unusable_password()
        user.save()
        return user
    def create_superuser(self,email ,password ,**extra_fields):
        if email is None:
            raise TypeError('Users should have an Email')
        user = self.model(email=self.normalize_email(email),is_staff=True , is_active=True,is_superuser=True,date_joined=timezone.now(),**extra_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254,default="", unique=True)
    family_name = models.CharField(max_length=254, null=True, blank=True)
    first_name= models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(blank = True, null=True,upload_to="images/photo%y%m%d",)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email

class Annoncement(models.Model):
    title= models.CharField(max_length=35, default='')
    caregorie = models.ForeignKey(
        Caregorie,
        default='',
        related_name='annonce',
        on_delete=models.CASCADE,
        )
    type = models.ForeignKey(
        Type,
        default='',
        related_name='annonce',
        on_delete=models.CASCADE,
        )
    interface = models.FloatField(default=0.0)
    prix= models.FloatField(default=0.0)
    description = models.TextField()
    contact = models.ForeignKey(
        Contact,
        default=None,
        related_name='annonce',
        on_delete=models.CASCADE,
        )
    location= models.OneToOneField(
        Location,
        default=None,
        on_delete=models.CASCADE,
        related_name='annonce',
        )
    creation_date= models.DateTimeField(
        default=datetime.now
    )
    user = models.ForeignKey(
        User,
        default='',
        related_name='annonce',
        on_delete=models.CASCADE,
        )
    
    
    favorated_by = models.ManyToManyField(
        User,
        default='',
        related_name='favorite',
    )
    

    def __str__(self):
        return self.title

class AnnoncementImage(models.Model):
    annoncement = models.ForeignKey(
        Annoncement,default='',
        related_name='images',
        on_delete=models.CASCADE,
        )
    image =models.ImageField(
        upload_to="images/photo%y%m%d",
        blank=True,
        null=True,
        )
    def __str__(self):
        return self.image.url

class Messages(models.Model):
    STATUS=[
        ('Pending','Pending'),
        ('Read','Read')
    ]

    content = models.TextField()
    sent_to= models.ForeignKey(
        User,
        default='',
        related_name='recieved_messages',
        on_delete=models.PROTECT
        )
    sent_by = models.ForeignKey(
        User,
        default='',
        related_name='sent_messages',
        on_delete=models.PROTECT
        )
    created_at = models.DateTimeField(auto_now=True)
    status= models.CharField(max_length=15, choices=STATUS, default='Pending')
    def __str__(self):
        return self.content