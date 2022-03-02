from django.contrib import admin
from .models import Task, TypeTask, EpicTask

admin.site.register(Task)
admin.site.register(TypeTask)
admin.site.register(EpicTask)