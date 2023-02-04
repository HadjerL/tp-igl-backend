from django.urls import path ,include
from gestionAnnonce import views
from rest_framework.routers import DefaultRouter

router =DefaultRouter()
router.register('types', views.viewsets_type)
router.register('categories',views.viewsets_category)
router.register('wilayas',views.viewsets_wilayas)
router.register('communes',views.viewsets_commune)
router.register('messages', views.viewsets_message)


urlpatterns = [
    # path('modify/<int:id>',views.modify_Announcement),
    path('create/',views.create_Annocement ),
    path('userAnnoncement/',views.user_annocement ),
    path('all_announcement/',views.all_announcemnt),
    path('get_announcement/<int:id>/',views.get_announcement),
    path('delete_announcement/<int:id>/',views.delete_announcemnt),
    path('find_user/',views.find_user),
    path('add_favorite/',views.add_favorate),
    path('remove_favorate/',views.remove_favorate),
    path('search_filter/',views.search_filter),
    path('login/',views.Login ),
    path('send_message/',views.send_message),
    path('get_recieved_messges/',views.get_recieved_messages),
    path('get_sent_messges/',views.get_sent_messages),
    path('get_my_fav/',views.get_my_fav),
    path('',include(router.urls)),
]