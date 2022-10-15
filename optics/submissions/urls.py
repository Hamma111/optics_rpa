from django.urls import path

from optics.submissions.views import UploadOpticalPIASubmissionView, UploadIEHPSubmissionView

app_name = "submissions"

urlpatterns = [
    path("submission/optical-pia", UploadOpticalPIASubmissionView.as_view(), name="upload-optical-pia-submission"),
    path("submission/iehp", UploadIEHPSubmissionView.as_view(), name="upload-iehp-submission"),
]