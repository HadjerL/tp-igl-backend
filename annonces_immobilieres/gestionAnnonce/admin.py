from django.contrib import admin
from .models import Annonce,Contact,Type,Caregorie

# Register your models here.

admin.site.register(Contact)
admin.site.register(Type)
admin.site.register(Caregorie)
admin.site.register(Annonce)