from django.urls import path
from .views import *

urlpatterns = [
    path('all/', BrandApiView.as_view()),
    path('all/<int:pk>', BrandApiDetailView.as_view()),
]