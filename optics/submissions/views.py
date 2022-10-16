from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, UpdateView

from optics.rpa.models import OpticalPIAOrder
from optics.rpa.tasks import place_optical_pia_order, place_iehp_order, run_automation_optical_pia_order
from optics.submissions.choices import SubmissionWebsiteType, StatusType
from optics.submissions.models import Submission, OpticalPIAOrderSubmission
from optics.submissions.utils import validate_uploaded_file


class UploadOpticalPIASubmissionView(LoginRequiredMixin, View):
    template_name = "submissions/upload_optical_pia_submission.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES["csv_file"]
        validate_uploaded_file(csv_file)

        submission = Submission.objects.create(
            csv_file=csv_file, user=request.user, website_type=SubmissionWebsiteType.OPTICAL_PIA,
            status=StatusType.PENDING
        )
        place_optical_pia_order.delay(submission.id)

        return render(request, self.template_name)


class UploadIEHPSubmissionView(LoginRequiredMixin, View):
    template_name = "submissions/upload_iehp_submission.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES["csv_file"]
        validate_uploaded_file(csv_file)

        submission = Submission.objects.create(
            csv_file=csv_file, user=request.user, website_type=SubmissionWebsiteType.IEHP, status=StatusType.PENDING
        )
        place_iehp_order.delay(submission.id)

        return redirect(reverse("dashboards:submissions_dashboard"))


class OpticalPIAOrderSubmissionUpdateView(LoginRequiredMixin, UpdateView):
    model = OpticalPIAOrder
    fields = [
        "subscriber_id", "subscriber_birthdate", "service_date", "issue_date", "gender", "material_type",
        "focal_options", 'sphere_r', "sphere_l", "cylinder_r", "cylinder_l", "axis_l", 'axis_r', 'pupillary_far_r',
        'pupillary_far_l', "pupillary_near_l", 'pupillary_near_r', 'add_power_r', 'add_power_l', 'seg_height_l',
        'seg_height_r', 'oc_height_l', 'oc_height_r', 'frame_enclosed', 'frame_manufacturer', 'frame_style',
        'eye_size', 'bridge_size', 'temple_size', 'color', 'frame_type',
    ]
    template_name = "submissions/update_optical_pia_order_submission.html"

    def get_success_url(self):
        return reverse("dashboards:submissions_dashboard")

    def dispatch(self, request, *args, **kwargs):
        ret = super().dispatch(request, *args, **kwargs)

        order = self.get_object()

        order_submission = order.optical_pia_submission
        order_submission.status = StatusType.PENDING
        order_submission.save(update_fields=["status", "modified"])

        run_automation_optical_pia_order.delay([order.id])

        return ret


class OpticalPIAOrderSubmissionReadOnlyDetailView(LoginRequiredMixin, DetailView):
    model = OpticalPIAOrder
    fields = "__all__"
    template_name = "submissions/detail_optical_pia_order_submission.html"
