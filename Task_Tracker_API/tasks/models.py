from django.db import models
from django.contrib.auth import models as auth_models


# Create your models here.
class User(auth_models.AbstractUser):
    ...


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_projects'
    )
    members = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.title


STATUS_CHOICES = [
    ('To Do', 'Запланированно'),
    ('In Progress', 'В процессе'),
    ('Done', 'Сделано'),
]
PRIORITY_CHOICES = [
    ('Low', 'Низкий'),
    ('Medium', 'Средний'),
    ('High', 'Высокий'),
]


class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default='To Do')
    priority = models.CharField(choices=PRIORITY_CHOICES)
    deadline = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_tasks'
    )
    assignee = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='tasks'
    )
    tags = models.ManyToManyField(Tag)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'project'],
                name='unique_task_in_project'
            )
        ]


class Comment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
