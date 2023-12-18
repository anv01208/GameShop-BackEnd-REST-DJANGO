from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from game_app.models import Game
from category_app.models import Category
from brand_app.models import Brand
from .models import Event
from .serializers import AllEventsSerializer, SaleGameSerializer, GameDetailSerializer


# Create your views here.


class EventsApiView(APIView):
    def get(self, request):
        events = Event.objects.all()
        data = AllEventsSerializer(events, many=True).data
        return Response(data, status.HTTP_200_OK)


class EventDetailApiView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        return super.get_permissions()
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        games = Game.objects.filter(event=event)
        if 'order_by' in request.GET.keys():
            ordering = request.GET.get('order_by')
            games = games.order_by(ordering)
        if 'category' in request.GET.keys():
            category_id = Category.objects.get('category')
            category = Category.objects.get(id=category_id)
            games = Game.objects.filter(genre=category)
        if 'brand' in request.GET.keys():
            brand_id = Brand.objects.get('brand')
            brand = Brand.objects.get(id=brand_id)
            games = Game.objects.filter(brand_name=brand)
        if 'search' in request.GET.keys():
            search = request.GET.get('search')
            games = games.filter(title__contains=search).union(games.filter(description__contains=search))
        serializer = SaleGameSerializer(games, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, pk):
        request.session['cart'] = request.data['games']

        return Response({'msg': 'Added'}, status.HTTP_200_OK)


class GameDetailApiView(APIView):
    def get(self, request, pk, game_id):
        event = get_object_or_404(Event, pk=pk)
        game = get_object_or_404(Game, event=event, id=game_id)
        data = GameDetailSerializer(game).data
        return Response(data, status.HTTP_200_OK)
