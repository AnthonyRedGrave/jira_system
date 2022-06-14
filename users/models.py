from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField("Аватар пользователя", null=True, blank=True, upload_to="users/images/")
    tools = models.ManyToManyField('Tool', verbose_name='Инструменты')
    position = models.CharField('Должность', max_length=150, default='Software Engineer')


class Tool(models.Model):
    title = models.CharField('Название', max_length=150)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'
