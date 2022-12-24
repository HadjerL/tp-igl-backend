from django.contrib import admin
from .models import Annonce, Contact, Type, Caregorie, Wilaya, Commune, Localization,AnnoncementImage

# Registering models here.

admin.site.register(Contact)
admin.site.register(Type)
admin.site.register(Caregorie)
admin.site.register(Annonce)
admin.site.register(Wilaya)
admin.site.register(Commune)
admin.site.register(Localization)
admin.site.register(AnnoncementImage)