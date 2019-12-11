import os
import shutil


def task_document_path(instance, filename):
    task_id = instance.project.id
    project_id = instance.task.block.project.id
    return f'projects/project_{project_id}/task_{task_id}/{filename}'


def task_delete_path(document):
    datetime_path = os.path.abspath(os.path.join(document.path, '..'))
    shutil.rmtree(datetime_path)
