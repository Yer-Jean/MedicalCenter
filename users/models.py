from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    username = None  # удаляем поле username, так как авторизовать будем по полю email
    email = models.EmailField(unique=True, verbose_name='Email')

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')

    birthday = models.DateField(verbose_name='Дата рождения', **settings.NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **settings.NULLABLE)
    address = models.CharField(max_length=150, verbose_name='Адрес', **settings.NULLABLE)
    photo = models.ImageField(upload_to='users/', verbose_name='Фото', **settings.NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **settings.NULLABLE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Modified date')
    is_active = models.BooleanField(default=False, verbose_name='Active')
    verification_token = models.CharField(max_length=50, **settings.NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def role(self, group_name):
        return self.groups.filter(name=group_name).exists()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('last_name',)
        # permissions = [('set_user_active_status', 'Can activate/deactivate users')]
