# Generated by Django 4.2.7 on 2024-02-29 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostic',
            name='test_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnostics', to='main.diagnosticcategory', verbose_name='Категория'),
        ),
    ]
