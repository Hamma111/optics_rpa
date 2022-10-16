from django.db import models
from django_extensions.db.models import TimeStampedModel

from optics.submissions.choices import StatusType, SubmissionWebsiteType


class Submission(TimeStampedModel):
    # order = models.JSONField()
    csv_file = models.FileField(upload_to="uploaded-csv/%Y-%m/")
    website_type = models.CharField(max_length=255, choices=SubmissionWebsiteType.choices)
    status = models.CharField(max_length=25, choices=StatusType.choices, default=StatusType.PENDING)

    user = models.ForeignKey("users.User", on_delete=models.PROTECT, related_name="submissions")

    def __str__(self):
        return f"{self.user} | {self.website_type} | {self.status}"


class SubmissionLog(TimeStampedModel):
    submission = models.ForeignKey("submissions.Submission", on_delete=models.PROTECT, related_name="logs")
    status = models.CharField(max_length=25, choices=StatusType.choices)

    def __str__(self):
        return f"{self.submission} | {self.status}"


class OpticalPIAOrderSubmission(TimeStampedModel):
    screenshot1 = models.ImageField(null=True, blank=True, upload_to="optical-screenshot1/%Y-%m/")
    screenshot2 = models.ImageField(null=True, blank=True, upload_to="optical-screenshot2/%Y-%m/")
    error_screenshot = models.ImageField(null=True, blank=True, upload_to="error-screenshot/%Y-%m/")
    error_text = models.CharField(max_length=5000, null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusType.choices, default=StatusType.PENDING)

    order = models.OneToOneField("rpa.OpticalPIAOrder", on_delete=models.PROTECT, related_name="optical_pia_submission")
    submission = models.ForeignKey("submissions.Submission", on_delete=models.PROTECT, related_name="optical_pia_submissions")

    def reset_status(self):
        self.screenshot1 = None
        self.screenshot2 = None
        self.error_screenshot = None
        self.error_text = None
        self.status = StatusType.PENDING
        self.save()

    def __str__(self):
        return f"{self.submission} | {self.status}"


class IEHPOrderSubmission(TimeStampedModel):
    screenshot1 = models.ImageField(null=True, blank=True, upload_to="iehp-screenshot1/%Y-%m/")
    error_screenshot = models.ImageField(null=True, blank=True, upload_to="error-screenshot/%Y-%m/")
    error_text = models.CharField(max_length=5000, null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusType.choices, default=StatusType.PENDING)

    order = models.OneToOneField("rpa.IEHPOrder", on_delete=models.PROTECT, related_name="iehp_submission")
    submission = models.ForeignKey("submissions.Submission", on_delete=models.PROTECT, related_name="iehp_submission")

    def __str__(self):
        return f"{self.submission} | {self.status}"
