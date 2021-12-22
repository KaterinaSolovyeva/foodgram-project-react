from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping_cart, Tag)
from users.permissions import AuthorAdminOrReadOnly

from .filters import RecipeFilter
from .mixins import TagIngredientMixinViewSet
from .serializers import (FavoriteRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeReadSerializer,
                          RecipeSerializer, ShoppingSerializer, TagSerializer)


class TagsViewSet(TagIngredientMixinViewSet):
    """Модель обработки запроса к тегам."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(TagIngredientMixinViewSet):
    """Модель обработки запроса к ингредиентам."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    """Модель обработки запросов к рецептам."""
    queryset = Recipe.objects.all()
    permission_classes = (AuthorAdminOrReadOnly,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return RecipeReadSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )
        return serializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        favorite = Favorite.objects.filter(user=self.request.user.id)
        shopping_cart = Shopping_cart.objects.filter(user=self.request.user.id)
        if is_favorited == 'true':
            queryset = queryset.filter(favorites__in=favorite)
        elif is_favorited == 'false':
            queryset = queryset.exclude(favorites__in=favorite)
        if is_in_shopping_cart == 'true':
            queryset = queryset.filter(shopping__in=shopping_cart)
        elif is_in_shopping_cart == 'false':
            queryset = queryset.exclude(shopping__in=shopping_cart)
        return queryset

    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=(IsAuthenticated,),
        pagination_class=None,
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = FavoriteSerializer(
            data={'user': request.user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        if request.method == 'GET':
            serializer.is_valid(raise_exception=True)
            serializer.save(recipe=recipe, user=request.user)
            serializer = FavoriteRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(
            Favorite, recipe=recipe, user=request.user
        )
        self.perform_destroy(favorite)
        return Response(
            f'Рецепт {recipe} удален из избранного.',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=(IsAuthenticated,),
        pagination_class=None,
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = ShoppingSerializer(
            data={'user': request.user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        if request.method == 'GET':
            serializer.is_valid(raise_exception=True)
            serializer.save(recipe=recipe, user=request.user)
            serializer = FavoriteRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        shopping_cart = get_object_or_404(
            Shopping_cart, recipe=recipe, user=request.user
        )
        self.perform_destroy(shopping_cart)
        return Response(
            f'Рецепт {recipe} удален из списка покупок.',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request, pk=None):
        cart = request.user.shopping.all()
        shopping_list = {}
        for item in cart:
            recipe = item.recipe
            ingredients_recipe = IngredientRecipe.objects.filter(recipe=recipe)
            for item in ingredients_recipe:
                name = item.ingredients.name
                measurement_unit = item.ingredients.measurement_unit
                amount = item.amount
                if name not in shopping_list:
                    shopping_list[name] = {
                        'amount': amount,
                        'measurement_unit': measurement_unit
                    }
                else:
                    shopping_list[name]['amount'] = (
                        shopping_list[name]['amount'] + amount
                    )
        content = ['Список ингредиентов для выбранных рецептов:\n\n', ]
        for item in shopping_list:
            content.append(
                f"{item}({shopping_list[item]['measurement_unit']}) - "
                f"{shopping_list[item]['amount']}\n"
            )
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment;' 'filename="shopping_list.txt"'
        )
        return response
