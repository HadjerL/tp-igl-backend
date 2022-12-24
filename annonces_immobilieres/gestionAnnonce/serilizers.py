from rest_framework import serializers
from .models import Annonce,Contact,Type,Caregorie,AnnoncementImage

#translate python to json



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['nom_type']

class AnnoncementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnoncementImage
        fields = ["id", "image", "annoncement"]

class AnnoceSerializer(serializers.ModelSerializer):
    images=AnnoncementImageSerializer(many=True, read_only=True)
    class Meta:
        model = Annonce
        fields = [
            'id',
            'contact',
            'description',
            'prix',
            'interface',
            'type',
            'caregorie',
            'images',
            
        ]





