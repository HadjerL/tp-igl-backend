from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Annonce, Contact, Type, Caregorie, Wilaya, Commune, Location,AnnoncementImage,User
# Registering models here.

        
admin.site.register(Contact)
admin.site.register(Type)
admin.site.register(Caregorie)
admin.site.register(Annonce)
admin.site.register(Wilaya)
admin.site.register(Commune)
admin.site.register(Location)
admin.site.register(AnnoncementImage)
admin.site.register(User)
