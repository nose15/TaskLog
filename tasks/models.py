import datetime
from datetime import timedelta

from django.db import models
from django.db.models import ForeignKey


class TaskDetails(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    finished = models.BooleanField(default=False)


class Task(models.Model):
    task_details_id = ForeignKey(to=TaskDetails, on_delete=models.CASCADE, related_name="task_details")
    due_date_time = models.DateTimeField(null=True, blank=True)


class RecurringTaskInfo(models.Model):
    task_details_id = ForeignKey(TaskDetails, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    repeat_interval = models.DurationField(default=datetime.timedelta(days=1))
    times_finished = models.IntegerField(default=0)
