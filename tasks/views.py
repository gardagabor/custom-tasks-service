from cgi import print_form

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tasks.models import Task
from django.utils.dateparse import parse_datetime
import json


def index(request):
    tasks_list = Task.objects.all()
    context = {"tasks_list": tasks_list}
    return render(request, "tasks/index.html", context)

def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, "tasks/detail.html", {"task": task})

@csrf_exempt  # Only for testing - remove in production and properly handle CSRF
def create_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
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
                status=data.get('status')
            )

            return JsonResponse({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'creation_date': task.creation_date.isoformat(),
                'due_date': task.due_date.isoformat()
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

