from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import MyUser, Subscription


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = MyUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscription.objects.filter(
            user=request.user,
            author=obj
        ).exists()
