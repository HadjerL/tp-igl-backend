from rest_framework import serializers
from .models import Annoncement, Contact, Type, Category, Wilaya, Commune, Location, AnnoncementImage, Address, User, Token, Messages


#translate python to json



class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model.

    This serializer will handle the conversion of a Contact model instance into
    Python data types that can be easily rendered into JSON .

    The ContactSerializer uses all fields specified by the model.

    Attributes:
        model (Contact): The model to use for the serializer.
        fields (all): The fields to include in the serializer output.
    """
    class Meta:
        model = Contact
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Type model. This class is a subclass of serializers.ModelSerializer from the Django Rest Framework library. 
    
    This serializer will handle the conversion of a Type model instance into
    Python data types that can be easily rendered into JSON .

    Attributes:
        model (Type): The model to use for the serializer.
        fields (all): The fields to include in the serializer,the value '_all_' indicates that all fields should be included.
    """
    class Meta:
        model = Type
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    This serializer will handle the conversion of a Category model instance into
    Python data types that can be easily rendered into JSON .

    The CategorySerializer uses all fields specified by the model.

    Attributes:
        model (Category): The model to use for the serializer.
        fields (all): The fields to include in the serializer output.
    """
    class Meta:
        model = Category
        fields = '__all__'

class AnnoncementImageSerializer(serializers.ModelSerializer):
    """
    This class is a subclass of serializers.ModelSerializer from the Django Rest Framework library. 
    It is used to serialize instances of the AnnoncementImage model into Python data structures 
    that can be easily converted into JSON or other formats for APIs.
    """
    class Meta:
        model = AnnoncementImage
        fields = ["id", "image", "annoncement"]

class CommuneSerializer(serializers.ModelSerializer):
    """
    This class is a subclass of serializers.ModelSerializer from the Django Rest Framework library. 
    It is used to serialize instances of the Commune model into Python data structures, 
    that can be easily converted into JSON .
    """
    wilaya= serializers.StringRelatedField(many= False, read_only= True)
    class Meta:
        model = Commune
        fields = ['designation','wilaya']
        # gets the field designation from commune and locations related

class WilayaSerializer(serializers.ModelSerializer):
    """
    This class is a subclass of serializers.ModelSerializer from the Django Rest Framework library. 
    It is used to serialize instances of the Wilaya  model into Python data structures, 
    that can be easily converted into JSON .
    """
    #targets the related field using its primaryKey
    commune = CommuneSerializer(many= True, read_only=True)
    class Meta:
        model = Wilaya
        # gets the field designation from wilaya and all commune related
        fields = ['id','designation','commune']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model= Address
        fields= ['address','latitude','longitude','location']

class LocationSerializer(serializers.ModelSerializer):
    """
    This class is a subclass of serializers.ModelSerializer from the Django Rest Framework library. 
    It is used to serialize instances of the Location  model into Python data structures, 
    that can be easily converted into JSON .
    """
    wilaya= serializers.StringRelatedField(many=False, read_only=True)
    commune= serializers.StringRelatedField(many=False, read_only=True)
    address= AddressSerializer(many=False, read_only=True)
    class Meta:
        model = Location
        fields = ['wilaya','commune','address']
    # gets all fields along with related announcements

class AnnoceSerializer(serializers.ModelSerializer):
    """
    This class is a subclass of serializers.ModelSerializer from the Django Rest Framework library. 
    It is used to serialize instances of the Annoncement model into Python data structures, 
    that can be easily converted into JSON .
    """
    images=serializers.StringRelatedField(many=True, read_only=True)
    type= TypeSerializer(many=False, read_only=True)
    category = CategorySerializer(many= False, read_only= True)
    location= LocationSerializer(many=False, read_only=True)
    class Meta:
        model = Annoncement
        fields = [
            'id',
            'title',
            'category',
            'area',
            'price',
            'description',
            'contact',
            'location',
            'type',
            'creation_date',
            'images',
            'user',
            'favorated_by',
            'deleted'
            ]


class tokenSerializer(serializers.ModelSerializer):
    """
    This class is a subclass of serializers.ModelSerializer from the Django Rest Framework library. 
    It is used to serialize instances of the Token  model into Python data structures, 
    that can be easily converted into JSON .
    """
    class Meta:
        model = Token
        fields = ['key']


class UserSerializer(serializers.ModelSerializer):
    """
    This class is a subclass of serializers.ModelSerializer from the Django Rest Framework library. 
    It is used to serialize instances of the User  model into Python data structures, 
    that can be easily converted into JSON .
    """
    class Meta:
        model = User
        fields = [
            'email',
            'annonce',
            'last_login',
            'date_joined',
            'image',
            'first_name',
            'family_name',
            'favorite',
        ]

class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'family_name',
        ]

class MessageSerializer(serializers.ModelSerializer):
    sent_to= serializers.PrimaryKeyRelatedField(many= False, read_only= True)
    sent_by= SenderSerializer(many= False, read_only=True)

    class Meta:
        model = Messages
        fields= ['title','content','sent_to','sent_by','created_at','status']


