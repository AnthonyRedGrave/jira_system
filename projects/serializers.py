from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):

    manager_name = serializers.StringRelatedField(source="manager")
    type = serializers.ChoiceField(choices=Project.TypeProject, source='get_type_display')

    class Meta:
        model = Project
        fields = ('id', 'title', 'manager_name', 'type')