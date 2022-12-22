from rest_framework import serializers
from .models import Annonce,Contact,Type,Caregorie



class CaregorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caregorie
        fields = 'annonce'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class AnnoceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'





