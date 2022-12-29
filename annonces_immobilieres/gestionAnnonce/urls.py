
from django.urls import path ,include
from .views import create_Annocement,modify_Announcement,viewsets_annoncement,viewsets_token,Login
from gestionAnnonce import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token #view acces to model token
router =DefaultRouter()
router.register('', views.viewsets_annoncement)
router.register('Type', views.viewsets_type)

router.register('token', viewsets_token)
urlpatterns = [
    path('modify/<int:_id>',modify_Announcement),
    path('create/',create_Annocement ),
    path('log/',Login ),
    path("find_type/", views.find_annocement_type),
    path('',include(router.urls)),
    #token authentication
    path('apiToken',obtain_auth_token)
]