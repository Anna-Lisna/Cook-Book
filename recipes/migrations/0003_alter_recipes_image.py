# Generated by Django 4.0.7 on 2022-08-12 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipes_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_recipe', to='recipes.images'),
        ),
    ]
