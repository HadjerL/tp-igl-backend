from rest_framework import serializers
from .models import Annonce, Contact, Type, Caregorie, Wilaya, Commune, Location, AnnoncementImage, Address, User, Token

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
    type= serializers.StringRelatedField(many=False, read_only=True)
    caregorie= serializers.StringRelatedField(many= False, read_only= True)
    class Meta:
        model = Annonce
        fields = [
            'id',
            'title',
            'caregorie',
            'interface',
            'prix',
            'description',
            'contact',
            'location',
            'type',
            'creation_date',
            'images',
            ]


class WilayaSerializer(serializers.ModelSerializer):
    #targets the related field using its primaryKey
    commune = serializers.StringRelatedField(many= True, read_only=True)
    class Meta:
        model = Wilaya
        # gets the field designation from wilaya and all commune related
        fields = ['designation','commune']

class CommuneSerializer(serializers.ModelSerializer):
    wilaya= serializers.StringRelatedField(many= False, read_only= True)
    class Meta:
        model = Commune
        fields = ['designation','wilaya']
        # gets the field designation from commune and locations related

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model= Address
        fields= ['address','latitude','longitude','location']

class LocationSerializer(serializers.ModelSerializer):
    wilaya= serializers.StringRelatedField(many=False, read_only=True)
    commune= serializers.StringRelatedField(many=False, read_only=True)
    address= serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = Location
        fields = ['wilaya','commune','address']
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


