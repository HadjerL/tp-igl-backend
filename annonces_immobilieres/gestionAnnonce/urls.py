from django.urls import path ,include
from gestionAnnonce import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token #view acces to model token
router =DefaultRouter()
router.register('announcement', views.viewsets_annoncement)
router.register('type', views.viewsets_type)
router.register('wilaya',views.viewsets_wilayas)
router.register('commune',views.viewsets_commune)
router.register('address',views.viewsets_address)
router.register('location',views.viewsets_location)


urlpatterns = [
    path('modify/<int:id>',views.modify_Announcement),
    path('create/',views.create_Annocement ),
    path('myAnnoucement/<int:id>',views.user_annocement ),
    path('find_type/<str:type>', views.find_annocement_type),
    path('find_wilaya/<str:wilaya>',views.find_annocement_wilaya),
    path('find_commune/<str:commune>',views.find_annocement_commune),
    path('find_category/<str:category>',views.find_annocement_category),
    path('login/',views.Login ),
    path('',include(router.urls)),
    path('locations/',views.location_coordinates),
    path('coordinates/',views.coordinates_location),
    path('duck/',views.get_cities),
    #token authentication
    path('apiToken',obtain_auth_token)
]