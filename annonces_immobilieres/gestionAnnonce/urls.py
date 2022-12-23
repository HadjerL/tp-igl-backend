
from django.urls import path 
from .views import consult_Announcement,consult_Announcements,create_Annocement,modify_Announcement

urlpatterns = [
    path('modify/',modify_Announcement),
    path('create/',create_Annocement),
    path('consult/',consult_Announcement),
    path('all/',consult_Announcements),
]
