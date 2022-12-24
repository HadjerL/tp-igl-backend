
from django.urls import path ,include
from .views import consult_Announcement,consult_Announcements,create_Annocement,modify_Announcement,viewsets_annoncement
from gestionAnnonce import views
from rest_framework.routers import DefaultRouter
router =DefaultRouter()
router.register('annoncement', views.viewsets_annoncement)
router.register('Type', views.viewsets_type)
urlpatterns = [
    path('modify/<int:_id>',modify_Announcement),
    path('create/',create_Annocement.as_view() ),
    path('consult/<int:_id>',consult_Announcement),
    path('all/',consult_Announcements),
    path("find_type/", views.find_annocement_type),
    path('',include(router.urls)),
    path('try/', views.trial)
]
