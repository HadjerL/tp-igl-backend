from django.urls import path ,include
from gestionAnnonce import views
from rest_framework.routers import DefaultRouter

router =DefaultRouter()
router.register('announcements', views.viewsets_annoncement)
router.register('types', views.viewsets_type)
router.register('categories',views.viewsets_category)
router.register('wilayas',views.viewsets_wilayas)
router.register('communes',views.viewsets_commune)
router.register('addresses',views.viewsets_address)
router.register('locations',views.viewsets_location)
router.register('messages', views.viewsets_message)


urlpatterns = [
    path('modify/<int:id>',views.modify_Announcement),
    path('create/',views.create_Annocement ),
    path('userAnnoncement/<int:id>',views.user_annocement ),
    path('find_type/<str:type>', views.find_annocement_type),
    path('find_wilaya/<str:wilaya>',views.find_annocement_wilaya),
    path('find_commune/<str:commune>',views.find_annocement_commune),
    path('find_category/<str:category>',views.find_annocement_category),
    path('all_announcement/',views.all_announcemnt),
    path('delete_announcement/<int:id>',views.delete_announcemnt),
    path('find_user',views.find_user),
    path('add_favorate',views.add_favorate),
    path('remove_favorate',views.remove_favorate),
    path('search_filter',views.search_filter),
    path('login/',views.Login ),
    path('send_message/',views.send_message),
    path('get_recieved_messges/',views.get_recieved_messages),
    path('get_sent_messges/',views.get_sent_messages),
    path('get_my_fav/',views.get_my_fav),
    path('',include(router.urls)),

]