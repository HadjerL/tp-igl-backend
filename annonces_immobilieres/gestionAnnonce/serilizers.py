from rest_framework import serializers
from .models import Annonce,Contact,Type,Caregorie

#translate python to json

class CaregorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caregorie
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['annonce']

class AnnoceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'





