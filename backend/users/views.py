from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import SubscriptionSerializer, SubscriptionUserSerializer
from users.models import MyUser, Subscription


class CustomUserViewSet(UserViewSet):
    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=(IsAuthenticated,),
        pagination_class=None,
    )
    def subscribe(self, request, id):
        author = get_object_or_404(MyUser, id=id)
        serializer = SubscriptionSerializer(
            data={'user': request.user, 'author': author},
            context={'request': request}
        )
        if request.method == 'GET':
            serializer.is_valid(raise_exception=True)
            serializer.save(author=author, user=request.user)
            serializer = SubscriptionUserSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscription = get_object_or_404(
            Subscription,
            author=author,
            user=request.user
        )
        self.perform_destroy(subscription)
        return Response(
            f'{request.user} больше не подписан на {author}',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request, pk=None):
        authors = MyUser.objects.filter(following__user=request.user)
        recipes_limit = request.query_params.get('recipes_limit')
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(authors, request)
        serializer = SubscriptionUserSerializer(
            result_page, many=True, context={
                'current_user': request.user,
                'recipes_limit': recipes_limit
            }
        )
        return paginator.get_paginated_response(serializer.data)
