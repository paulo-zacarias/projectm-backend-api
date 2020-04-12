from django.contrib import admin
from .models import Project, Sprint, Task

admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(Task)
