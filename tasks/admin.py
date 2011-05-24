from django.contrib import admin
from erp.tasks.models import *

admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(TaskComment)
admin.site.register(SubTaskComment)
