# Generated by Django 4.2.7 on 2024-02-29 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0002_promo_sub_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='promo/', verbose_name='Изображение'),
        ),
    ]
