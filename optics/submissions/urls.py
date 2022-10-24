from django.urls import path

from optics.submissions.views import (
    UploadOpticalPIASubmissionView, UploadIEHPSubmissionView, OpticalPIAOrderSubmissionUpdateView,
    OpticalPIAOrderSubmissionReadOnlyDetailView, IEHPOrderSubmissionUpdateView, IEHPOrderSubmissionReadOnlyDetailView
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
    path("iehp-submissions/<int:pk>/update/", IEHPOrderSubmissionUpdateView.as_view(),
         name="update-iehp-order-submission"),
    path("iehp-submissions/<int:pk>/detail/", IEHPOrderSubmissionReadOnlyDetailView.as_view(),
         name="detail-iehp-order-submission"),
]
