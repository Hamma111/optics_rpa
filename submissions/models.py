from django.db import models
from django_extensions.db.models import TimeStampedModel

from submissions.choices import StatusType, SubmissionType


class Submission(TimeStampedModel):
    file = models.FileField(upload_to="uploaded-csv/%Y-%m/")

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=SubmissionType.choices, null=True)

    def __str__(self):
        return f"{self.user} | {self.created}"


class SubmissionLog(TimeStampedModel):
    order = models.JSONField()
    status = models.CharField(max_length=25, choices=StatusType.choices, default=StatusType.PENDING)

    submission = models.ForeignKey("submissions.Submission", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.submission} | {self.status}"


class OpticalPIAOrderSubmission(TimeStampedModel):
    screenshot1 = models.ImageField(null=True, blank=True, upload_to="optical-screenshot1/%Y-%m/")
    screenshot2 = models.ImageField(null=True, blank=True, upload_to="optical-screenshot2/%Y-%m/")
    error_screenshot = models.ImageField(null=True, blank=True, upload_to="error-screenshot/%Y-%m/")
    error_text = models.CharField(max_length=5000, null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusType.choices, default=StatusType.PENDING)

    optical_pia_order = models.ForeignKey("rpa.OpticalPIAOrder", on_delete=models.PROTECT, related_name="submission")
    submission = models.ForeignKey("submissions.Submission", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.submission} | {self.status}"


class IEHPOrderSubmission(TimeStampedModel):
    screenshot1 = models.ImageField(null=True, blank=True, upload_to="iehp-screenshot1/%Y-%m/")
    error_screenshot = models.ImageField(null=True, blank=True, upload_to="error-screenshot/%Y-%m/")
    error_text = models.CharField(max_length=5000, null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusType.choices, default=StatusType.PENDING)

    iehp_order = models.ForeignKey("rpa.IEHPOrder", on_delete=models.PROTECT, related_name="submission")
    submission = models.ForeignKey("submissions.Submission", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.submission} | {self.status}"
