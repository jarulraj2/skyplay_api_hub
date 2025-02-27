from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 

class APILog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    endpoint = models.URLField()
    request_data = models.TextField()
    response_data = models.TextField()
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.endpoint} - {self.timestamp}"
