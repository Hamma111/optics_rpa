from time import sleep

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
import logging

from optics.dashboards.filters import OpticalPIAOrderSubmissionFilter, IEHPOrderSubmissionFilter
from optics.submissions.models import OpticalPIAOrderSubmission, IEHPOrderSubmission

logger = logging.getLogger(__name__)


class PIASubmissionsDashboardView(LoginRequiredMixin, ListView):
    template_name = "dashboards/pia_submissions.html"
    model = OpticalPIAOrderSubmission

    def get_queryset(self):
        order_submissions = (
            OpticalPIAOrderSubmission.objects
            .filter(submission__user=self.request.user)
            .select_related("submission")
            .prefetch_related("order")
            .order_by("-created")
        )
        order_submissions = OpticalPIAOrderSubmissionFilter(self.request.GET, queryset=order_submissions).qs

        return order_submissions

    def get_context_data(self, **kwargs):
        return {"order_submissions": self.get_queryset()}

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get("is_redirected_from_upload_page"):
            sleep(3)

        return super().dispatch(request, *args, **kwargs)


class IEHPSubmissionsDashboardView(LoginRequiredMixin, ListView):
    template_name = "dashboards/iehp_submissions.html"
    model = OpticalPIAOrderSubmission

    def get_queryset(self):
        order_submissions = (
            IEHPOrderSubmission.objects
            .filter(submission__user=self.request.user)
            .select_related("submission")
            .prefetch_related("order")
            .order_by("-created")
        )
        # order_submissions = IEHPOrderSubmissionFilter(self.request.GET, queryset=order_submissions).qs

        return order_submissions

    def get_context_data(self, **kwargs):
        return {"order_submissions": self.get_queryset()}

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get("is_redirected_from_upload_page"):
            sleep(3)

        return super().dispatch(request, *args, **kwargs)
