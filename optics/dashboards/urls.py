from django.urls import path

from optics.dashboards.views import SubmissionsDashboard


app_name = "dashboards"

urlpatterns = [
    path("dashboard/", SubmissionsDashboard.as_view(), name="dashboard")
]
