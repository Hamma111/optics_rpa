from django.db import models


class StatusType(models.TextChoices):
    SUCCESS = "SUCCESS", "Success"
    ERROR = "ERROR", "Error"
    PENDING = "PENDING", "Pending"
