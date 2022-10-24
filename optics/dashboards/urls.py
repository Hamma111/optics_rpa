from django.urls import path

from optics.dashboards.views import PIASubmissionsDashboardView, IEHPSubmissionsDashboardView

app_name = "dashboards"

urlpatterns = [
    path("pia-submissions-dashboard/", PIASubmissionsDashboardView.as_view(), name="pia_submissions_dashboard"),
    path("iehp-submissions-dashboard/", IEHPSubmissionsDashboardView.as_view(), name="iehp_submissions_dashboard")
]
