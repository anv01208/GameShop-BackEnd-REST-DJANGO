from rest_framework.serializers import ModelSerializer
from .models import Brand
from category_app.models import Category
from game_app.models import Game


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GamesByBrandSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = ['id','title', 'description', 'price', 'release_at', 'brand_name', 'genre']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['brand_name'] = BrandSerializer(instance.brand_name).data
        representation['genre'] = CategorySerializer(instance.genre, many=True).data

        return representation
