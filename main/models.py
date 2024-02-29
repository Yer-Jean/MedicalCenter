from django.conf import settings
from django.db import models


class TestCategory(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**settings.NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория анализа'
        verbose_name_plural = 'Категории анализов'
        ordering = ('name',)


class Test(models.Model):
    article = models.CharField(max_length=10, verbose_name='Артикул')
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**settings.NULLABLE, verbose_name='Описание')
    test_category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, related_name='tests', verbose_name='Категория')
    deadline = models.PositiveSmallIntegerField(default=1, verbose_name='Срок исполнения')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return f'{self.article} - {self.name}'

    class Meta:
        verbose_name = 'Анализ'
        verbose_name_plural = 'Анализы'
        ordering = ('name',)


class DiagnosticCategory(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**settings.NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория диагностики'
        verbose_name_plural = 'Категории диагностик'
        ordering = ('name',)


class Diagnostic(models.Model):
    article = models.CharField(max_length=10, verbose_name='Артикул')
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**settings.NULLABLE, verbose_name='Описание')
    test_category = models.ForeignKey(DiagnosticCategory, on_delete=models.CASCADE, related_name='diagnostics', verbose_name='Категория')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return f'{self.article} - {self.name}'

    class Meta:
        verbose_name = 'Диагностика'
        verbose_name_plural = 'Диагностики'
        ordering = ('name',)
