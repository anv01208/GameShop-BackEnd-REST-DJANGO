from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Game
from brand_app.models import Brand
from category_app.models import Category


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SaleGameSerializer(ModelSerializer):
    discounted_price = SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'title', 'price', 'event', 'discounted_price', 'is_free']

    def get_discounted_price(self, obj):
        if obj.event.pk == 1:
            discount_percentage = 25
        elif obj.event.pk == 3:
            discount_percentage = 25
        elif obj.event.pk == 2:
            discount_percentage = 50
        elif obj.event.pk == 4:
            discount_percentage = 15
        else:
            return obj.price

        discounted_price = obj.price * (1 - discount_percentage / 100)
        return discounted_price


class GameDetailSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = ['title', 'description', 'price', 'release_at', 'brand_name', 'genre', 'event', 'is_free']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['brand_name'] = BrandSerializer(instance.brand_name).data
        representation['genre'] = CategorySerializer(instance.genre, many=True).data
        representation['is_free'] = 'Free' if instance.is_free else 'Not Free'

        return representation


class GameUpdateSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = ['title', 'description', 'price', 'release_at', 'brand_name', 'genre', 'event', 'is_free']


class CreateGameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = ['title', 'description', 'price', 'genre', 'brand_name', 'release_at', 'event', 'is_free']
