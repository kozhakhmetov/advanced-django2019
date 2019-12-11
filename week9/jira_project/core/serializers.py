from core.models import Project, Task, Block, TaskDocument, TaskComment
from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    # creator = UserSerializer()
    # my_name = serializers.SerializerMethodField()
    # creator_name = serializers.SerializerMethodField()
    creator_id = serializers.IntegerField(write_only=True)
    # tasks_count = serializers.IntegerField(default=0)

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


class TaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    executor = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())
    status = serializers.IntegerField()

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('creator',)

    def create(self, request):
        Task.objects.create(name=self.validated_data['name'],
                            description=self.validated_data['description'],
                            creator=request.user,
                            executor=self.validated_data['executor'],
                            block=self.validated_data['block'])


class TaskShortSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    creator = UserSerializer(read_only=True)
    # document = serializers.FileField(write_only=True)
    # document_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'document', 'status', 'project_id', 'creator')

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


