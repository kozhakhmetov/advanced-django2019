from core.models import Project, Task, Block, TaskDocument, TaskComment
from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    creator_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'creator_id')

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.first_name
        return ''


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'
        read_only_fields = ('project',)


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    status = serializers.IntegerField()
    project_id = serializers.IntegerField(write_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('creator',)

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        return task

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.description = validated_data.get('description', instance.description)
        instance.project_id = validated_data.get('project_id', instance.project_id)

        instance.save()
        return instance

    def validate_status(self, value):
        if 1 < value > 3:
            raise serializers.ValidationError('status options: [1, 2, 3]')
        return value


class TaskShortSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'status', 'project_id', 'creator')

    def get_document_url(self, obj):
        if obj.document:
            return self.context['request'].build_absolute_uri(obj.document.url)
        return None


class TaskFullSerializer(TaskShortSerializer):
    class Meta(TaskShortSerializer.Meta):
        fields = TaskShortSerializer.Meta.fields + ('priority', 'description')


class TaskDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDocument
        fields = '__all__'


class TaskCommentSerializer(serializers.ModelSerializer):
    body = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField()
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = TaskComment
        fields = '__all__'
        read_only_fields = ('creator',)

    def create(self, request):
        TaskComment.objects.create(body=self.validated_data['body'],
                                   creator=request.user,
                                   created_at=self.validated_data['created_at'],
                                   task=self.validated_data['task'])
