from django.db import models
from django.conf import settings
import uuid

class FCMToken(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration_id = models.TextField()

    def __str__(self):
        return self.token
