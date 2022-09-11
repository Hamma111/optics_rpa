from django.db import models


class StatusType(models.TextChoices):
    SUCCESS = "SUCCESS", "Success"
    ERROR = "ERROR", "Error"
    PENDING = "PENDING", "Pending"


class SubmissionType(models.TextChoices):
    OPTICAL_PIA = "OPTICAL_PIA", "Optical PIA"
    IEHP = "IEHP", "IEHP"
