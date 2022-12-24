from rest_framework import serializers
from .models import Annonce, Contact, Type, Caregorie, Wilaya, Commune , Location

#translate python to json



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['nom_type']

class AnnoceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'

class CommuneSerializer(serializers.ModelSerializer):
    model = Commune
    fields = ['designation', 'location']
    # gets the field designation from commune and locations related


class WilayaSerializer(serializers.ModelSerializer):
    model = Wilaya
    fields = ['id','location']
    # gets the field designation from wilaya and location related


class LocationSerializer(serializers.ModelSerializer):
    model = Location
    fields = ['__all__','annonce']
    # gets all fields along with related announcements