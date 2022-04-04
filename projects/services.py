from tasks.serializers import TaskSerializer
from projects.models import Notification

def get_tasks_board(tasks):
    tasks_json = {}
    for task in tasks:
        if tasks_json.get(task.type_task.title) != None:
            tasks_json[task.type_task.title].append(TaskSerializer(task, many=False).data)
        else:
            tasks_json[task.type_task.title] = [(TaskSerializer(task, many=False).data)]

    return tasks_json


def create_notification(kwargs):
    Notification.objects.create(**kwargs)