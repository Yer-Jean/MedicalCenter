# Generated by Django 4.2.7 on 2024-03-04 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_medicalresult_medicalresultfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalresult',
            name='description',
            field=models.CharField(default=0, max_length=200, verbose_name='Описание'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='prescription',
            field=models.TextField(blank=True, null=True, verbose_name='Медицинское назначение'),
        ),
    ]
