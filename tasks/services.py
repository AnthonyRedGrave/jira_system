from .models import RoadMapTask

def create_road_map_task(task, content, roadmap):
    RoadMapTask.objects.create(task=task, content=content, roadmap=roadmap)