from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class MyUser(AbstractUser):
    """Модель юзера с выбором роли."""
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    USER = 'user'
    ANONYMOUS = 'anonymous'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (ANONYMOUS, 'Аноним'),
    ]

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Не корректный никнейм',
                code='invalid_username',
            ),
        ]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль'
    )
    role = models.CharField(
        max_length=30,
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )

    @property
    def is_admin(self):
        return self.is_superuser or self.role == MyUser.ADMIN

    @property
    def is_user(self):
        return self.role == MyUser.USER

    class Meta:
        """Дополнительная информация по управлению моделью MyUser."""
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписки на автора."""
    user = models.ForeignKey(
        MyUser,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        MyUser,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        """Дополнительная информация по управлению моделью Subscription."""
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.constraints.UniqueConstraint(
                fields=['user', 'author'],
                name='follow_unique'
            ),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
