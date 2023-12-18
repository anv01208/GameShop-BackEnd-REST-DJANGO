from .models import Game
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import SaleGameSerializer, GameDetailSerializer, GameUpdateSerializer, CreateGameSerializer
from category_app.models import Category
from brand_app.models import Brand


# Create your views here.


class GamesApiView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return super(GamesApiView,self).get_permissions()

    def get(self, request):
        games = Game.objects.all()
        free_games = Game.objects.filter(is_free=True)
        for game in free_games:
            game.is_free = False
            game.save()
        import random
        new_free_games = random.sample(list(games),k=2)
        for game in new_free_games:
            game.is_free= True
            game.save()
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
        data = SaleGameSerializer(games, many=True).data
        return Response(data, status.HTTP_200_OK)

    def post(self, request):
        request.session['cart'] = request.data['games']
        return Response({'msg': 'Added'}, status.HTTP_200_OK)


class GameDetailApiView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'PATCH':
            return [IsAdminUser()]
        return super(GameDetailApiView, self).get_permissions()

    def get(self, request, pk):
        game = Game.objects.get(id=pk)
        data = GameDetailSerializer(game).data
        return Response(data, status.HTTP_200_OK)

    def patch(self, request, pk):
        game = Game.objects.get(id=pk)
        serializer = GameUpdateSerializer(game, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = GameDetailSerializer(game).data
            return Response(data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CreateGameApiView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CreateGameSerializer(data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
