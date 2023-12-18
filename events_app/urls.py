from django.urls import path
from .views import *

urlpatterns = [
    path('all', EventsApiView.as_view()),
    path('all/<int:pk>', EventDetailApiView.as_view()),
    path('all/<int:pk>/<int:game_id>', GameDetailApiView.as_view())
]