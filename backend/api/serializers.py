from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping_cart, Tag)
from users.models import MyUser, Subscription
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    recipe = serializers.IntegerField(source='recipe.id')

    class Meta:
        model = Favorite
        fields = ('user', 'recipe',)

    def validate(self, data):
        user = data['user']['id']
        recipe = data['recipe']['id']
        if Favorite.objects.filter(user__id=user, recipe__id=recipe).exists():
            raise serializers.ValidationError(
                {'ошибка': 'Нельзя добавить повторно рецепт в избранное.'}
            )
        return data

    def create(self, validated_data):
        user = validated_data['user']
        recipe = validated_data['recipe']
        Favorite.objects.get_or_create(user=user, recipe=recipe)
        return validated_data


class ShoppingSerializer(FavoriteSerializer):
    class Meta:
        model = Shopping_cart
        fields = ('user', 'recipe',)

    def validate(self, data):
        user = data['user']['id']
        recipe = data['recipe']['id']
        if Shopping_cart.objects.filter(
            user__id=user, recipe__id=recipe
        ).exists():
            raise serializers.ValidationError(
                {'ошибка': 'Этот рецепт уже есть в вашем списке покупок.'}
            )
        return data

    def create(self, validated_data):
        user = validated_data['user']
        recipe = validated_data['recipe']
        Shopping_cart.objects.get_or_create(user=user, recipe=recipe)
        return validated_data


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit'
    )
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        source='recipe_ingredient',
        many=True,
        read_only=True,
    )
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return Shopping_cart.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        for ingredient_item in ingredients:
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': ('Убедитесь, что количество '
                                    'ингредиента больше 0')
                })
        data['ingredients'] = ingredients
        return data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        for ingredient in ingredients_data:
            IngredientRecipe.objects.get_or_create(
                recipe=recipe,
                ingredients_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        recipe.is_favorited = False
        recipe.is_in_shopping_cart = False
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientRecipe.objects.filter(recipe=instance).all().delete()
        for ingredient in validated_data.get('ingredients'):
            ingredient_amount_obj = IngredientRecipe.objects.create(
                recipe=instance,
                ingredients_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            ingredient_amount_obj.save()
        instance.save()
        return instance


class RecipeReadSerializer(RecipeSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(
        required=True,
        slug_field='username',
        queryset=MyUser.objects.all()
    )

    class Meta:
        model = Subscription
        fields = ('user', 'author',)
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'author'],
                message='Нельзя дважды подписаться на одного и того же автора.'
            )
        ]


class SubscriptionUserSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.BooleanField(default=True)

    class Meta:
        model = MyUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return recipes.count()

    def get_recipes(self, obj):
        queryset = obj.recipes.all()
        try:
            if self.context['recipes_limit'] is not None:
                limit = queryset[:int(self.context['recipes_limit'])]
                return FavoriteRecipeSerializer(limit, many=True).data
        except KeyError:
            return FavoriteRecipeSerializer(queryset, many=True).data
        return FavoriteRecipeSerializer(queryset, many=True).data
