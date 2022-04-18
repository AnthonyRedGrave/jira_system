from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project
from tasks.models import Task


User = get_user_model()


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        task = "task", "Задача"
        invitation = "invitation", "Приглашение"
        change = "change", "Изменение"
        message = "message", "Сообщение"

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="notifictions"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifictions_to"
    )
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifictions_from"
    )
    read = models.BooleanField(default=False)
    type = models.CharField("Тип уведомления", max_length=30, choices=NotificationType.choices)
    message = models.CharField("Сообщение", max_length=150, null=True, blank=True)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE, related_name='notificications')

    def __str__(self) -> str:
        return f"{self.project} {self.user} {self.read}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
