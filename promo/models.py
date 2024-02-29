from django.conf import settings
from django.db import models
from django.urls import reverse


class Promo(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    sub_title = models.CharField(max_length=200, **settings.NULLABLE, verbose_name='Предложение')
    description = models.TextField(verbose_name='Описание')
    slug = models.CharField(max_length=200, verbose_name='Слаг')
    image = models.ImageField(upload_to='promo/', **settings.NULLABLE, verbose_name='Изображение',)
    is_active = models.BooleanField(default=False, verbose_name='Активно')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('promo:promos', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
