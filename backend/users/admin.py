from django.contrib.admin import ModelAdmin, register

from foodgram.settings import EMPTY_STRING_FOR_ADMIN_PY

from .models import MyUser, Subscription

ModelAdmin.empty_value_display = EMPTY_STRING_FOR_ADMIN_PY


@register(MyUser)
class MyUserAdmin(ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name', 'role',)
    list_editable = ('role',)
    search_fields = ('username', 'email')


@register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_display = ('user', 'author',)
    list_filter = ('user', 'author',)
