from django.db import models

from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=300, blank=True)
    creator = models.ManyToManyField(User)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Block(models.Model):
    name = models.CharField(max_length=30)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    BLOCK_TYPE_CHOICES = (
        (1, 'to_do'),
        (2, 'in_progress'),
        (3, 'done'),
        (0, 'new')
    )

    block_type = models.PositiveSmallIntegerField(choices=BLOCK_TYPE_CHOICES)


class Task(models.Model):
    name = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=300, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    block = models.ForeignKey(Block, on_delete=models.CASCADE)


class TaskDocument(models.Model):
    document = models.FileField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class TaskComment(models.Model):
    body = models.TextField(max_length=100, blank=True)
    created_at = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
