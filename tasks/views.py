from django.shortcuts import render
from . models import Task, TaskDetails, RecurringTaskInfo
from datetime import datetime, timedelta
from . services import TaskService
from django.views.generic import TemplateView
from django.utils.timezone import get_default_timezone


class TaskView(TemplateView):
    template_name = "tasks/index.html"
    task_service = TaskService()

    def get(self, request, *args, **kwargs):
        try:
            task_count = request.GET.get('task_count')
        except KeyError as e:
            task_count = 0

        recent_tasks = self.task_service.get_most_recent_tasks(task_count)
        return render(request, "tasks/index.html", {"recent_tasks": recent_tasks, "time": datetime.now(tz=get_default_timezone())})
