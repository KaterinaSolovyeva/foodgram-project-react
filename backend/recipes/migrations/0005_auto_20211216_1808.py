# Generated by Django 2.2.16 on 2021-12-16 18:08

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_delete_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', max_length=7, samples=None, unique=True),
        ),
    ]
