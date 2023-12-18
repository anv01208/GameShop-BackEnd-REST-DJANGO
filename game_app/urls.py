from django.urls import path
from .views import GamesApiView,GameDetailApiView,CreateGameApiView

urlpatterns = [
    path('all/',GamesApiView.as_view()),
    path('all/<int:pk>',GameDetailApiView.as_view()),
    path('create',CreateGameApiView.as_view())
]