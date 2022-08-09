from django.shortcuts import render
from django.views import View
import pandas as pd


class SubmissionView(View):
    template_name = "submissions/submission.html"

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

        df = pd.read_csv(csv_file.temporary_file_path())

        return render(request, self.template_name)
