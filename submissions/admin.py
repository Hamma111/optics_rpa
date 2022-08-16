from django.contrib import admin

from .models import Submission, SubmissionLog, OpticalPIAOrderSubmission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'file', 'user')
    list_filter = ('created', 'modified', 'user')


@admin.register(SubmissionLog)
class SubmissionLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'status',
    )
    list_filter = ('created', 'modified', 'submission')


@admin.register(OpticalPIAOrderSubmission)
class OpticalPIAOrderSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'screenshot1',
        'screenshot2',
        'error_screenshot',
        'error_text',
        'status',
    )
    list_filter = ('created', 'modified', 'optical_pia_order', 'submission')
