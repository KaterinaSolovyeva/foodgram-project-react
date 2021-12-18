from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.viewsets import GenericViewSet

from users.permissions import AdminOrReadOnly


class TagIngredientMixinViewSet(
        ListModelMixin,
        CreateModelMixin,
        DestroyModelMixin,
        RetrieveModelMixin,
        GenericViewSet):
    """Миксин для классов тега и ингредиента."""
    pagination_class = None
    filter_backends = [SearchFilter, ]
    search_fields = ['name']
    permission_classes = (AdminOrReadOnly,)
