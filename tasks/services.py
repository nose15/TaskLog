from typing import List
from . models import Task, RecurringTaskInfo, TaskDetails
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, get_default_timezone


class TaskService:
    @classmethod
    def _closest_sunday(cls) -> datetime:
        today = datetime.today()
        day_of_week = today.weekday()
        days_until_sunday = (6 - day_of_week) % 7
        closest_sunday_date = today + timedelta(days=days_until_sunday)

        return make_aware(closest_sunday_date, get_default_timezone())

    @classmethod
    def _update_tasks(cls) -> None:
        ended_tasks = Task.objects.filter(due_date_time__lt=datetime.now(tz=get_default_timezone()))

        for task in ended_tasks:
            task_details = task.task_details_id
            recurring_task_info = RecurringTaskInfo.objects.get(task_details_id=task_details)

            if recurring_task_info is not None:
                cls._handle_recurring_task(recurring_task_info, task_details)

            task.delete()

    @classmethod
    def _handle_recurring_task(cls, recurring_task_info: RecurringTaskInfo, task_details: TaskDetails) -> None:
        recurring_task_info.times_finished += int(task_details.finished)

        if recurring_task_info.end_date < datetime.now(tz=get_default_timezone()):
            return

        new_date_time = recurring_task_info.start_date + recurring_task_info.repeat_interval

        while new_date_time < datetime.now(tz=get_default_timezone()):
            new_date_time += recurring_task_info.repeat_interval

        while new_date_time < cls._closest_sunday() and new_date_time < recurring_task_info.end_date:
            task, created = Task.objects.get_or_create(task_details_id=task_details, due_date_time=new_date_time)

            if created:
                task.save()

            new_date_time += recurring_task_info.repeat_interval

    def get_most_recent_tasks(self, count: int = 0) -> List[Task]:
        self._update_tasks()

        if count == 0:
            return Task.objects.all().order_by('due_date_time').filter(due_date__lte=self._closest_sunday())
        else:
            return Task.objects.all().order_by('due_date_time')[:count]


