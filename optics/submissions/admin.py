from django.contrib import admin

from .models import Submission, OpticalPIAOrderSubmission, IEHPOrderSubmission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'csv_file', 'user', "website_type")
    list_filter = ('created', 'modified', 'user')


@admin.register(OpticalPIAOrderSubmission)
class OpticalPIAOrderSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'screenshot1',
        'screenshot2',
        'error_screenshot',
        'status',
        'error_text',
    )
    list_filter = ('created', 'modified', 'order', 'submission')


@admin.register(IEHPOrderSubmission)
class IEHPOrderSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'screenshot1',
        'error_screenshot',
        'status',
        'error_text',
    )
    list_filter = ('created', 'modified', 'order', 'submission')
