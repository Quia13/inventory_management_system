from django.db import models
from users.models import User
# Create your models here.
class AuditLog(models.Model):
    class Meta:
        db_table = 'audit_logs'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    action = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    object_id = models.CharField(max_length=255)

    changes = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)