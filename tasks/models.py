from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def get_default_type_task():
    type, _ = TypeTask.objects.get_or_create(title="TO DO")
    return type.id


class TypeTask(models.Model):

    title = models.CharField("Тип задачи", max_length=20)

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name = "Тип задачи"
        verbose_name_plural = "Типы задач"


class EpicTask(models.Model):

    title = models.CharField("Эпик задачи", max_length=150)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "Эпик задачи"
        verbose_name_plural = "Эпики задач"


class Task(models.Model):

    title = models.CharField("Задача", max_length=150)
    description = models.TextField()
    type_task = models.ForeignKey(
        TypeTask,
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
        default=get_default_type_task,
    )
    epic_task = models.ForeignKey(
        EpicTask, on_delete=models.SET_NULL, related_name="tasks", null=True
    )
    implementer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"Задача {self.title} - {self.type_task.title}"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"