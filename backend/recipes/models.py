from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import MyUser


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=50,
        blank=False,
    )

    class Meta:
        """Дополнительная информация по управлению моделью Ingredient."""
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель для тега."""
    name = models.CharField('Название', max_length=200, unique=True,)
    color = ColorField(
        default='#FF0000',
        unique=True,
        max_length=7,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Не корректный slug',
                code='invalid_slug',
            ),
        ])

    class Meta:
        """Дополнительная информация по управлению моделью Tag."""
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField('Название', max_length=200)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        help_text='Загрузите фото готового блюда.'
    )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        help_text='Напишите время приготовления в минутах',
        validators=[
            MinValueValidator(
                1,
                'Минимальное время приготовления - 1 минута.'
            ),
        ]
    )

    class Meta:
        """Дополнительная информация по управлению моделью Recipe."""
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Таблица связи ингридиентов и рецепта."""
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
        verbose_name='Ингредиенты'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Рецепт'
    )
    amount = models.PositiveIntegerField('Количество',)

    class Meta:
        """Дополнительная информация по управлению моделью IngredientRecipe."""
        verbose_name = "Ингредиент для рецепта"
        verbose_name_plural = "Ингредиенты для рецепта"

    def __str__(self):
        return f'{self.ingredients} для {self.recipe}'


class Favorite(models.Model):
    """Модель избранного рецепта."""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name="favorites",
                             )

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='favorites')

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.user} добавил в избраное рецепт {self.recipe}'


class Shopping_cart(models.Model):
    """Модель рецепта, добавленного в покупки."""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name="shopping",
                             )

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='shopping')

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.user} добавил в список покупок рецепт {self.recipe}'
