from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project, Task, Tag


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')
    filter_horizontal = ('members',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'assignee')
    list_filter = ('status', 'priority', 'project')
    filter_horizontal = ('tags',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
