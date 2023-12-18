from django.urls import path
from .views import *

urlpatterns = [
    path('all/', CategoryApiView.as_view()),
    path('all/<int:pk>', CategoryDetailView.as_view()),
]