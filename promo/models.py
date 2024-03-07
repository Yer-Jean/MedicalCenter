from django.conf import settings
from django.db import models


class Promo(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    sub_title = models.CharField(max_length=200, **settings.NULLABLE, verbose_name='Предложение')
    description = models.TextField(**settings.NULLABLE, verbose_name='Описание')
    image = models.ImageField(upload_to='promo/', **settings.NULLABLE, verbose_name='Изображение',)
    is_active = models.BooleanField(default=False, verbose_name='Активно')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        permissions = [('set_promo_active_status', 'Can activate/deactivate promo')]
