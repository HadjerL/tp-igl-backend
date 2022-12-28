from django.db import models
from smart_selects.db_fields import ChainedForeignKey 




class Caregorie(models.Model):
    nom_cat = models.CharField(max_length=20)
    def __str__(self):
        return self.nom_cat


class Type(models.Model):
    nom_type = models.CharField(max_length=20)
    def __str__(self):
        return self.nom_type

class Contact(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    adresse = models.TextField(blank=True)
    tele = models.IntegerField()
    def __str__(self):
        return self.prenom


# Localisation = state(wilaya) + communes
# state = commune+
class Wilaya(models.Model):
    designation = models.CharField(max_length=35)
    def __str__(self):
        return self.designation

class Commune(models.Model):
    designation = models.CharField(max_length=35)
    wilaya = models.ForeignKey( #each commune has one wilaya
        Wilaya,
        on_delete=models.PROTECT,
        default=None,
        related_name= 'commune'
        )
    def __str__(self):
        return self.designation

class Location(models.Model):
    wilaya = models.ForeignKey( #each localization has one wilaya
        Wilaya,
        on_delete= models.CASCADE,
        default=None,
        related_name='location'
        )
    commune = ChainedForeignKey( # to get only and all communes in a wilaya
        Commune,
        chained_field="wilaya", #the field in commune of wilaya
        chained_model_field="wilaya",
        show_all=False,  # only show commune corresponding to selected wilaya
        on_delete= models.CASCADE,
        default=None,
        related_name= 'location',
        auto_choose= True
        )
    address = models.CharField(max_length=50)
    def __str__(self):
        return self.address

class Annonce(models.Model):
    title= models.CharField(max_length=35, default='')
    caregorie = models.ForeignKey(
        Caregorie,
        default='',
        related_name='annonce',
        on_delete=models.CASCADE
        )
    type = models.ForeignKey(
        Type,
        default='',
        related_name='annonce',
        on_delete=models.CASCADE
        )
    interface = models.FloatField(default=0.0)
    prix= models.FloatField(default=0.0)
    description = models.TextField(blank=True)
    contact = models.ForeignKey(
        Contact,default='',
        related_name='annonce',
        on_delete=models.CASCADE
        )
    location= models.OneToOneField(
        Location,
        default=None,
        on_delete=models.CASCADE,
        related_name='annonce',
        )
    def __str__(self):
        return self.title
#ay haja
class AnnoncementImage(models.Model):
    annoncement = models.ForeignKey(
        Annonce,default='',
        related_name='images',
        on_delete=models.CASCADE
        )
    image =models.ImageField(
        upload_to="photo%y%m%d",
        blank=True,
        null=True
        )
    def __str__(self):
        return self.image.url
