from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsTaskAuthorOrAssignee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'author'):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.project.owner == request.user:
            return True

        is_author = obj.author == request.user
        is_assignee = obj.assignee == request.user

        if request.method == 'DELETE':
            return is_author

        if request.method in ['PUT', 'PATCH']:
            update_fields = set(request.data.keys())

            author_allowed = {'description'}
            assignee_allowed = {'status', 'priority'}

            allowed_fields = set()
            if is_author:
                allowed_fields.update(author_allowed)
            if is_assignee:
                allowed_fields.update(assignee_allowed)

            return update_fields.issubset(allowed_fields)

        return False


class IsCommentAuthorOrProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'task'):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        is_author = obj.author == request.user
        is_project_owner = obj.task.project.owner == request.user

        if request.method == 'DELETE':
            return is_author or is_project_owner

        if request.method in ['PUT', 'PATCH']:
            return is_author

        return False


class IsProjectMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'members'):
            return obj.members.filter(id=request.user.id).exists()

        if hasattr(obj, 'project'):
            return obj.project.members.filter(id=request.user.id).exists()

        if hasattr(obj, 'task'):
            return obj.task.project.members.filter(id=request.user.id).exists()

        return False
