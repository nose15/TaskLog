from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Task)
admin.site.register(models.TaskDetails)
admin.site.register(models.RecurringTaskInfo)
