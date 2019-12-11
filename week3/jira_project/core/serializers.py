from core.models import Project, Task, Block, TaskDocument, TaskComment
from rest_framework import serializers

from users.models import User


class ProjectSerializer(serializers.ModelSerializer):
    # creator = UserSerializer()
    # my_name = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()
    creator_id = serializers.IntegerField(write_only=True)
    tasks_count = serializers.IntegerField(default=0)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'creator_name', 'creator_id', 'tasks_count')

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
    block = serializers.PrimaryKeyRelatedField(queryset=Block.objects.all())

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


