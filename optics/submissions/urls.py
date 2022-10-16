from django.urls import path

from optics.submissions.views import (
    UploadOpticalPIASubmissionView, UploadIEHPSubmissionView, OpticalPIAOrderSubmissionUpdateView,
    OpticalPIAOrderSubmissionReadOnlyDetailView
)

app_name = "submissions"

urlpatterns = [
    path("upload-optical-pia-submission", UploadOpticalPIASubmissionView.as_view(),
         name="upload-optical-pia-submission"),
    path("upload-iehp-submission", UploadIEHPSubmissionView.as_view(), name="upload-iehp-submission"),
    path("optical-pia-submissions/<int:pk>/update/", OpticalPIAOrderSubmissionUpdateView.as_view(),
         name="update-optical-pia-order-submission"),
    path("optical-pia-submissions/<int:pk>/detail/", OpticalPIAOrderSubmissionReadOnlyDetailView.as_view(),
         name="detail-optical-pia-order-submission"),
]
