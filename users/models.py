from django.db import models
from django.contrib.auth.models import User

class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.PositiveIntegerField()

    def __str__(self):
        return self.code