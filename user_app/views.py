from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout, authenticate
from user_app.serializers import UserCreateSerializer, UserProfileSerializer, UserProfileUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from game_app.models import Game
from events_app.serializers import SaleGameSerializer


# Create your views here.

class AuthApiView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: 'Welcome',
            403: 'Username or/and password is not valid!',
        }
    )
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            data = {'message': 'Welcome!'}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': 'Username or/and password is not valid!'}
            return Response(data, status.HTTP_403_FORBIDDEN)


class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        data = {'message': 'GoodBye!'}
        return Response(data, status.HTTP_200_OK)


class RegistrationApiView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'name', 'surname'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'surname': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: 'You will receive you data',
            400: 'Serializer errors',
        }
    )
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)

        import json
        from urllib.request import urlopen

        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)

        IP = data['ip']
        org = data['org']
        city = data['city']
        country = data['country']
        region = data['region']

        location = {'IP': IP,
                    'org': org,
                    'city': city,
                    'country': country,
                    'region': region
                    }
        if location['country'] == 'RU' or 'KZ' or 'UZ' or 'AZ' or 'AM' or 'KG' or 'MD' or 'TJ':
            location['msg'] = 'Здравствуй странник из СНГ!'
        else:
            location['msg'] = 'Welcome dear,Wanderer!'

        return Response(data=[serializer.data, location], status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = UserProfileSerializer(user).data
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'msg': 'User deleted'}, status.HTTP_200_OK)


class CartApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if 'cart' in request.session.keys():
            games_id = request.session['cart']
            games = Game.objects.filter(id__in=games_id)
            data = SaleGameSerializer(games, many=True).data
            total = 0
            for price in data:
                total += price['discounted_price']
            data.append({'sum': total})
            return Response(data, status.HTTP_200_OK)
        else:
            return Response({'msg': ' Shopping Cart is empty'}, status.HTTP_200_OK)

    def post(self, request):
        if 'cart' in request.session.keys():
            games_id = request.session['cart']
            games = Game.objects.filter(id__in=games_id)
            request.user.number_of_purchases += len(games_id)
            request.user.history_of_purchases.add(*games_id)
            games = Game.objects.filter(id__in=games_id)
            data = SaleGameSerializer(games, many=True).data
            total = 0
            for game_data in data:
                is_free = game_data.get('is_free', False)
                if is_free:
                    total = total
                else:
                    total += game_data['discounted_price']
            if 30 <= request.user.number_of_purchases <= 55:
                total = total - (total * 5 / 100)
            elif 55 < request.user.number_of_purchases <= 100:
                total = total - (total * 10 / 100)
            elif request.user.number_of_purchases > 100:
                total = total - (total * 15 / 100)
            if request.user.wallet >= total:
                request.user.wallet -= total
                request.user.save()
                request.session.pop('cart')
                return Response(
                    {'msg': 'Purchase successfull, remaining on your balance is {0}'.format(request.user.wallet)})
            else:
                return Response({'msg': ' You dont have enough balance in wallet'})
        else:
            return Response({'msg': 'Add games to cart'}, status.HTTP_200_OK)


class PurchaseHistoryApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        purchases = request.user.history_of_purchases.all()
        data = SaleGameSerializer(purchases, many=True).data
        return Response(data, status.HTTP_200_OK)


# class EmailApiView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self,request):
#         text = request.data['message']
#         receiver = request.data['receiver']
#         from .functions import send_email
#         send_email(text,receiver)
#         return Response({'msg':'Message send'},status=status.HTTP_200_OK)


class JokesApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        import requests

        url = "https://official-joke-api.appspot.com/random_joke"

        response = requests.get(url)
        data = response.json()
        return Response(data, status.HTTP_200_OK)
