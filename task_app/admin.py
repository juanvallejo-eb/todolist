from django.contrib import admin
from .models import Priority, Task

# Register your models here.
admin.site.register(Task)
admin.site.register(Priority)
