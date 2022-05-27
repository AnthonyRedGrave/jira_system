from tasks.serializers import TaskSerializer
from tasks.models import TypeTask

def get_tasks_board(tasks):
    tasks_json = {"TO DO": [], "DEVELOPMENT": [], "TESTING": [], "REVIEW": []}
    # required_type_tasks = []
    for task in tasks:
        if tasks_json.get(task.type_task.title) != None:
            tasks_json[task.type_task.title].append(TaskSerializer(task, many=False).data)
        else:
            tasks_json[task.type_task.title] = [(TaskSerializer(task, many=False).data)]

    return tasks_json


