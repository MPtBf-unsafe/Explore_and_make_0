from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ProjectViewSet, TaskViewSet, CommentViewSet

router = SimpleRouter()
router.register('projects', ProjectViewSet)
router.register('tasks', TaskViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
