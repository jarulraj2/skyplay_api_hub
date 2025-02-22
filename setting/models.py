from django.db import models

class SiteSetting(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"{self.key}: {self.value}"
