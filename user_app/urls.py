from django.urls import path
from .views import *

urlpatterns = [
    path('auth/', AuthApiView.as_view()),
    path('logout/',LogoutApiView.as_view()),
    path('registration/',RegistrationApiView.as_view()),
    path('profile/',ProfileApiView.as_view()),
    path('profile/purchases/',PurchaseHistoryApiView.as_view()),
    path('cart/',CartApiView.as_view()),
    path('jokes/',JokesApiView.as_view())
    # path('email/',EmailApiView.as_view())

]
