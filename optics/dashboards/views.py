from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
import logging

from optics.submissions.models import OpticalPIAOrderSubmission

logger = logging.getLogger(__name__)


class SubmissionsDashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/submissions.html"

    def get_context_data(self, **kwargs):
        order_submissions = (
            OpticalPIAOrderSubmission.objects
            .filter(submission__user=self.request.user)
            .select_related("submission")
            .prefetch_related("order")
            .order_by("-created")
        )

        return {"order_submissions": order_submissions}
