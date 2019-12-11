from django.http import JsonResponse

from .models import TaskList, Task


def task_lists(request):
    task_list = TaskList.objects.all()
    json_categories = [c.to_json() for c in task_list]
    return JsonResponse(json_categories, safe=False)


def task_list_detail(request, pk):
    try:
        task_list = TaskList.objects.get(id=pk)
    except TaskList.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)

    return JsonResponse(task_list.to_json())


def tasks_all(request, pk):
    try:
        task_list = TaskList.objects.get(id=pk)
    except TaskList.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)

    tasks = task_list.task_set.all()
    response = [x.to_json() for x in tasks]
    return JsonResponse(response, safe=False)


def task_detail(request, pk):
    try:
        tasks = Task.objects.get(id=pk)
    except Task.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)

    return JsonResponse(tasks.to_json2())
