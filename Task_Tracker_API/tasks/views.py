from rest_framework import viewsets
from .permissions import (
    IsProjectMember, IsOwnerOrReadOnly,
    IsTaskAuthorOrAssignee, IsCommentAuthorOrProjectOwner
)
from .filters import TaskFilter
from .models import Project, Task, Comment
from .serializers import (
    ProjectSerializer, TaskSerializer, CommentSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectMember, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        project.members.add(self.request.user)

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [IsProjectMember, IsTaskAuthorOrAssignee]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Task.objects.filter(
            project__members=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsProjectMember, IsCommentAuthorOrProjectOwner]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Comment.objects.filter(
            task__project__members=self.request.user
        )
