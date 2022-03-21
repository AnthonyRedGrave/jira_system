from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    class TypeProject(models.TextChoices):
        software = "software", "Разработка программного обеспечения"
        service_management = "service_management", "Управление услугами"
        work_management = "work_management", "Управление работой"
        marketing = "marketing", "Маркетинг"
        work_with_personnel = "work_with_personnel", "Работа с кадрами"
        finance = "finance", "Финансы"
        design = "design", "Проектирование"
        personal = "personal", "Личные"



    title = models.CharField("Проект", max_length=150)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    type = models.CharField("Тип проекта", choices=TypeProject.choices, max_length=50)

    def __str__(self) -> str:
        return f"Проект {self.title}"

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
