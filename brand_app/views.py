from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework import status
from .models import Brand
from .serializers import BrandSerializer,GamesByBrandSerializer
from game_app.models import Game


# Create your views here.


class BrandApiView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return super(BrandApiView,self).get_permissions()
    def get(self,request):
        categories = Brand.objects.all()
        data = BrandSerializer(categories,many=True).data
        return Response(data,status.HTTP_200_OK)

    def post(self,request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class BrandApiDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'PATCH' or 'DELETE':
            return [IsAdminUser()]
        return super(BrandApiDetailView,self).get_permissions()

    def get(self,request,pk):
        games = Game.objects.filter(brand_name=pk)
        data = GamesByBrandSerializer(games,many=True).data
        return Response(data, status.HTTP_200_OK)

    def patch(self,request,pk):
        brand = Brand.objects.get(id=pk)
        serializer = BrandSerializer(brand,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        brand = Brand.objects.get(id=pk)
        brand.delete()
        return Response({'msg':'Brand deleted'}, status.HTTP_200_OK)