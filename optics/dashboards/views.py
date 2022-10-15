from django.views.generic import TemplateView


class SubmissionsDashboard(TemplateView):
    template_name = "dashboards/submissions.html"

    def get_context_data(self, **kwargs):

        return {}
