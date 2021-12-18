from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet

from .views import IngredientViewSet, RecipeViewSet, TagsViewSet

app_name = 'api'

router = DefaultRouter()
router.register(
    'tags',
    TagsViewSet,
    basename='tags')
router.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients'
)
router.register(
    'recipes',
    RecipeViewSet,
    basename='recipes'
)
router.register(
    'users',
    CustomUserViewSet,
    basename='users'
)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
