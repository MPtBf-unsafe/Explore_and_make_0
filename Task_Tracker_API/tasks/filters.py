from django_filters import rest_framework as filters
from .models import Task


class TaskFilter(filters.FilterSet):

    eadline_after = filters.DateFilter(
        field_name="deadline", lookup_expr='gte'
    )
    deadline_before = filters.DateFilter(
        field_name="deadline", lookup_expr='lte'
    )
    assignee = filters.CharFilter(field_name="assignee__username")
    project = filters.CharFilter(field_name="project__title")

    class Meta:
        model = Task
        fields = ['status', 'priority', 'project', 'assignee']
