from django.db import models

from core.constants import TASK_DONE, TASK_TODO, TASK_IN_PROGRESS, TASK_NEW, TASK_STATUSES
from users.models import User


class Project(models.Model):
    """
        Project model
    """
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


class TaskTodoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=TASK_TODO)

    def done_tasks(self):
        return self.filter(status=TASK_DONE)

    def filter_by_status(self, status):
        return self.filter(status=status)


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


class Block(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=TASK_STATUSES, default=TASK_NEW)

    # done_tasks = TaskDoneManager()
    # todo_tasks = TaskTodoManager()
    # new_tasks = TaskNewManager()
    # progress_tasks = TaskProgressManager()

    def __str__(self):
        return f'{self.name}: {self.project}'


class Task(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=300, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    class Meta:
        ordering = ('name', 'block',)
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f'{self.name}: {self.creator}, {self.block}'


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
