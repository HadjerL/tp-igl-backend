from rest_framework import serializers
from .models import Annonce, Contact, Type, Caregorie, Wilaya, Commune , Location,AnnoncementImage,User,Token

#translate python to json



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['nom_type']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Caregorie
        fields = ['nom_cat']

class AnnoncementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnoncementImage
        fields = ["id", "image", "annoncement"]


class AnnoceSerializer(serializers.ModelSerializer):
    images=AnnoncementImageSerializer(many=True, read_only=True)
    type= TypeSerializer(many=False, read_only=True)
    caregorie= CategorySerializer(many= False, read_only= True)
    class Meta:
        model = Annonce
        fields = [
            'id',
            'caregorie',
            'type',
            'images'
            ]

class CommunSerializer(serializers.ModelSerializer):
    model = Commune
    fields = ['designation', 'location']
    # gets the field designation from commune and locations related
class WilayaSerializer(serializers.ModelSerializer):
    model = Wilaya
    fields = ['designation','location']
    # gets the field designation from wilaya and location related

class CommunSerializer(serializers.ModelSerializer):
    model = Commune
    fields = ['designation', 'location']
    # gets the field designation from commune and locations related
class WilayaSerializer(serializers.ModelSerializer):
    model = Wilaya
    fields = ['designation','location']
    # gets the field designation from wilaya and location related

class LocationSerializer(serializers.ModelSerializer):
    model = Location
    fields = ['__all__','annonce']
    # gets all fields along with related announcements


class tokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']
class RegestierSerializer(serializers.ModelSerializer):
    key=tokenSerializer
    class Meta:
        model = User
        fields = ['email','key']
    
   

