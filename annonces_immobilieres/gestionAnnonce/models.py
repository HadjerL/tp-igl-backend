from django.db import models




class Caregorie(models.Model):
    nom_cat = models.CharField(max_length=20)

class Type(models.Model):
    nom_type = models.CharField(max_length=20)



class Contact(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    adresse = models.TextField(blank=True)
    tele = models.IntegerField()
    



class Annonce(models.Model):
    caregorie = models.ForeignKey(Caregorie,default='', related_name='annonce',on_delete=models.CASCADE)
    type = models.ForeignKey(Type,default='', related_name='annonce',on_delete=models.CASCADE)
    interface = models.FloatField(default=0.0)
    prix= models.FloatField(default=0.0)
    description = models.TextField(blank=True)
    contact = models.ForeignKey(Contact,default='', related_name='annonce',on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to="photo%y%m%d",blank=True,null=True)
   