# Generated by Django 4.2.7 on 2024-02-29 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_diagnostic_test_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='test_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='main.testcategory', verbose_name='Категория'),
        ),
    ]
