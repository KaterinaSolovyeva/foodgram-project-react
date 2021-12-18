import django_filters as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
