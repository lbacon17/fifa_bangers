from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    class Meta:
        verbose_name_plural = "Profiles"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.username
