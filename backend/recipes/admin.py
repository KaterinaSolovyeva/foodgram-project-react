from django.contrib import admin

from foodgram.settings import EMPTY_STRING_FOR_ADMIN_PY

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     Shopping_cart, Tag)

admin.ModelAdmin.empty_value_display = EMPTY_STRING_FOR_ADMIN_PY


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color',)
    search_fields = ('name',)
    list_filter = ('slug',)
    prepopulated_fields = {'slug': ('name',)}


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientRecipeInline,
    ]
    list_display = (
        'pk', 'author', 'name', 'cooking_time',
        'text', 'get_ingredients', 'get_tags', 'in_favorite'
    )
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags')

    def get_ingredients(self, obj):
        return '\n'.join(
            [str(ingredients) for ingredients in obj.ingredients.all()]
        )
    get_ingredients.short_description = 'Ингредиенты'

    def get_tags(self, obj):
        return '\n'.join([str(tags) for tags in obj.tags.all()])
    get_tags.short_description = 'Теги'

    def in_favorite(self, obj):
        in_favorite = Favorite.objects.filter(recipe=obj).count()
        return in_favorite
    in_favorite.short_description = 'В избранном'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredients', 'recipe', 'amount',)
    list_filter = ('recipe', 'ingredients',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)


@admin.register(Shopping_cart)
class Shopping_cartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
