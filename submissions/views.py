from django.shortcuts import render
from django.views import View
import pandas as pd

from rpa.tasks import place_optical_pia_order
from submissions.choices import SubmissionType
from submissions.models import Submission


class UploadOpticalPIASubmissionView(View):
    template_name = "submissions/optical-pia-submission.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            print('File is not CSV type')
            # return HttpResponseRedirect(reverse("myapp:upload_csv"))
        if csv_file.multiple_chunks():
            print("Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            # return HttpResponseRedirect(reverse("myapp:upload_csv"))

        try:
            df = pd.read_csv(csv_file.temporary_file_path())
            print(df)
        except Exception as ex:
            print(ex)
            raise Exception(ex)
        submission = Submission.objects.create(file=csv_file, user=request.user, type=SubmissionType.OPTICAL_PIA)

        place_optical_pia_order.delay(submission.id)

        return render(request, self.template_name)


class UploadIEHPSubmissionView(View):
    template_name = "submissions/iehp-submission.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            print('File is not CSV type')
            # return HttpResponseRedirect(reverse("myapp:upload_csv"))
        if csv_file.multiple_chunks():
            print("Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            # return HttpResponseRedirect(reverse("myapp:upload_csv"))

        try:
            df = pd.read_csv(csv_file.temporary_file_path())
            print(df)
        except Exception as ex:
            print(ex)
            raise Exception(ex)
        submission = Submission.objects.create(file=csv_file, user=request.user, type=SubmissionType.IEHP)

        place_optical_pia_order.delay(submission.id)

        return render(request, self.template_name)
