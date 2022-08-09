from django.urls import path

from submissions.views import SubmissionView

app_name = "submissions"

urlpatterns = [
    path("submission/", SubmissionView.as_view(), name="submission")
]