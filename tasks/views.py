import json
from functools import wraps
from typing import Dict, Any

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from tasks.models import Task
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime


def handle_exceptions(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return wrapper


@csrf_exempt
@require_http_methods(["POST", "GET"])
@handle_exceptions
def index(request):
    if request.method == 'GET':
        tasks_list = Task.objects.all()
        context = {"tasks_list": tasks_list}
        return render(request, "tasks/index.html", context)

    elif request.method == 'POST':
        return create_task(request)


def serialize_task(task: Task) -> Dict[str, Any]:    return {
    'id': task.id,
    'title': task.title,
    'description': task.description if task.description else None,
    'status': task.status,
    'creation_date': task.creation_date.isoformat(),
    'due_date': task.due_date.isoformat() if task.due_date else None,
}


@handle_exceptions
def get_task(request, task_id: int) -> JsonResponse:
    task = get_object_or_404(Task, pk=task_id)
    return JsonResponse(serialize_task(task), status=200)


@csrf_exempt
@require_http_methods(["POST"])
@handle_exceptions
def create_task(request) -> JsonResponse:
    data = json.loads(request.body)

    if not data.get('title'):
        return JsonResponse({
            'error': '"title" is required parameter'
        }, status=400)

    due_date = None
    if data.get('due_date'):
        due_date = parse_datetime(data.get('due_date'))
        if not due_date:
            return JsonResponse({
                'error': 'Invalid due_date format. Use ISO format (e.g., "2024-01-20T15:30:00Z")'
            }, status=400)

    task = Task.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        due_date=due_date,
        status=data.get('status') if data.get('status') else 'pending'
    )

    return JsonResponse(serialize_task(task), status=201)


@csrf_exempt
@require_http_methods(["PUT"])
@handle_exceptions
def update_task(request, task_id: int) -> JsonResponse:
    """Update an existing task"""
    task = get_object_or_404(Task, pk=task_id)
    data = json.loads(request.body)

    for key, value in data.items():
        setattr(task, key, value)
    task.save()

    return JsonResponse(serialize_task(task))


@csrf_exempt
@require_http_methods(["DELETE"])
@handle_exceptions
def delete_task(request, task_id: int) -> JsonResponse:
    task = get_object_or_404(Task, pk=task_id)
    task_title = task.title
    task.delete()
    return JsonResponse({
        'message': f'Task "{task_title}" successfully deleted',
        'task_id': task_id
    }, status=200)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def handle_task(request, task_id=None):
    if request.method == 'GET':
        return get_task(request, task_id)

    elif request.method == 'PUT':
        return update_task(request, task_id)

    elif request.method == 'DELETE':
        return delete_task(request, task_id)
