from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Annoncement, Contact, Type, Caregorie, Wilaya, Commune, Location, AnnoncementImage, User, Address
# Registering models here.


admin.site.register(Contact)
admin.site.register(Type)
admin.site.register(Caregorie)
admin.site.register(Annoncement)
admin.site.register(Wilaya)
admin.site.register(Commune)
admin.site.register(Location)
admin.site.register(AnnoncementImage)
admin.site.register(Address)
admin.site.register(User)