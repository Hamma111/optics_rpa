import django_filters

from optics.submissions.models import OpticalPIAOrderSubmission, IEHPOrderSubmission


class OpticalPIAOrderSubmissionFilter(django_filters.FilterSet):
    created = django_filters.CharFilter()
    patient_name = django_filters.CharFilter(field_name="order__patient_name", lookup_expr='icontains')

    class Meta:
        model = OpticalPIAOrderSubmission
        fields = ['status', 'created']


class IEHPOrderSubmissionFilter(django_filters.FilterSet):
    class Meta:
        model = IEHPOrderSubmission
        fields = ['status', 'created']
