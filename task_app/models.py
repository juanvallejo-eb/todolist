from django.db import models
from django.conf import settings


class Priority(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    @property
    def color(self):
        if self.name == "High":
            return "label label-danger"
        elif self.name == "Normal":
            return "label label-warning"
        else:
            return "label label-success"


class Task(models.Model):
    name = models.CharField(max_length=40)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE
    )
    event_id = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    @property
    def tick(self):
        return 'ok' if self.done else 'remove'
