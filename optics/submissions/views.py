from django.shortcuts import render
from django.views import View

from optics.rpa.tasks import place_optical_pia_order, place_iehp_order
from optics.submissions.choices import SubmissionWebsiteType, StatusType
from optics.submissions.models import Submission
from submissions.utils import validate_uploaded_file


class UploadOpticalPIASubmissionView(View):
    template_name = "submissions/optical-pia-submission.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES["csv_file"]
        validate_uploaded_file(csv_file)

        submission = Submission.objects.create(
            csv_file=csv_file, user=request.user, website_type=SubmissionWebsiteType.OPTICAL_PIA, status=StatusType.PENDING
        )
        place_optical_pia_order.delay(submission.id)

        return render(request, self.template_name)


class UploadIEHPSubmissionView(View):
    template_name = "submissions/iehp-submission.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES["csv_file"]
        validate_uploaded_file(csv_file)

        submission = Submission.objects.create(
            csv_file=csv_file, user=request.user,website_type=SubmissionWebsiteType.IEHP, status=StatusType.PENDING
        )
        place_iehp_order.delay(submission.id)

        return render(request, self.template_name)
