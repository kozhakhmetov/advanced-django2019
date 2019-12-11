from django.db import models

from utils.constants import TASK_DONE, TASK_TODO, TASK_IN_PROGRESS, TASK_NEW, TASK_STATUSES
from users.models import User
from utils.upload import task_document_path
from utils.validators import task_document_size, task_document_extension


class Project(models.Model):
    name = models.CharField(max_length=300, blank=False)
    description = models.TextField(max_length=300, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return f'{self.name}: {self.creator}'

    @property
    def tasks_count(self):
        return self.tasks.count()


class TaskProgressManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TASK_IN_PROGRESS)

    def done_tasks(self):
        return self.filter(status=TASK_IN_PROGRESS)

    def filter_by_status(self, status):
        return self.filter(status=status)


class TaskNewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TASK_NEW)

    def done_tasks(self):
        return self.filter(status=TASK_NEW)

    def filter_by_status(self, status):
        return self.filter(status=status)


class TaskTodoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TASK_TODO)

    def done_tasks(self):
        return self.filter(status=TASK_DONE)

    def filter_by_status(self, status):
        return self.filter(status=status)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TaskDoneManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TASK_DONE)

    def done_tasks(self):
        return self.filter(status=TASK_DONE)

    def filter_by_status(self, status):
        return self.filter(status=status)


class Block(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=TASK_STATUSES, default=TASK_NEW)

    def __str__(self):
        return f'{self.name}: {self.project}'


class BaseTask(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(default='')

    def get_short_name(self):
        return self.name[:3]

    @property
    def short_name(self):
        return self.name[:3]

    def set_name(self, name):
        self.name = name
        self.save()

    def show_info(self):
        raise NotImplementedError(
            'must be implemented'
        )

    class Meta:
        abstract = True


class Task(BaseTask):
    document = models.FileField(upload_to=task_document_path, validators=[task_document_size, task_document_extension],
                                null=True)
    status = models.PositiveSmallIntegerField(choices=TASK_STATUSES, default=TASK_NEW)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='tasks', null=True)
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tasks', null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

    class Meta(BaseTask.Meta):
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.name

    def __repr__(self):
        pass


class TaskDocument(models.Model):
    document = models.FileField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.document}: {self.creator}'


class TaskComment(models.Model):
    body = models.TextField(max_length=100, blank=True)
    created_at = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.creator}: {self.task}'


