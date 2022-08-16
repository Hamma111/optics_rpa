from django.urls import path

from submissions.views import UploadSubmissionView

app_name = "submissions"

urlpatterns = [
    path("submission/", UploadSubmissionView.as_view(), name="upload-submission"),
]