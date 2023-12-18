from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer,GamesByCategorySerializer
from game_app.models import Game


# Create your views here.


class CategoryApiView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAdminUser()]
        elif self.request.method == 'PATCH':
            return [IsAdminUser()]
        elif self.request.method == 'DELETE':
            return [IsAdminUser()]
        return super(CategoryApiView,self).get_permissions()

    def get(self, request):
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data, status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PATCH':
            return [IsAdminUser()]
        elif self.request.method == 'DELETE':
            return [IsAdminUser()]
        return super(CategoryDetailView,self).get_permissions()

    def get(self, request, pk):
        games = Game.objects.filter(genre=pk)
        data = GamesByCategorySerializer(games,many=True).data
        return Response(data, status.HTTP_200_OK)

    def patch(self, request, pk):
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = Category.objects.get(id=pk)
        category.delete()
        return Response({'msg': 'Category deleted'}, status.HTTP_200_OK)
