from .models import User, Project, Task, Comment, Tag
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    members = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'owner', 'members')


class TagSlugField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        tag, _ = Tag.objects.get_or_create(title=data)
        return tag


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    task = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Task.objects.all(),
    )

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    assignee = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    project = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Project.objects.all(),
    )

    status = serializers.CharField(required=False)

    tags = TagSlugField(
        slug_field='title',
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def validate(self, data):
        project = data.get('project')
        assignee = data.get('assignee')

        if project and assignee:
            if assignee not in project.members.all():
                raise serializers.ValidationError({
                    "assignee": "Исполнитель должен быть участником проекта."
                })

        return data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)

        for tag in tags_data:
            task.tags.add(tag)
        return task


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
