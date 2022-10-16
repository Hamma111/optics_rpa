from django.urls import path

from optics.dashboards.views import SubmissionsDashboard


app_name = "dashboards"

urlpatterns = [
    path("submissions-dashboard/", SubmissionsDashboard.as_view(), name="submissions_dashboard")
]
