from django.contrib import admin

from .models import Submission, SubmissionLog, OpticalPIAOrderSubmission, IEHPOrderSubmission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'file', 'user', "type")
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
        'status',
        'error_text',
    )
    list_filter = ('created', 'modified', 'optical_pia_order', 'submission')


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
    list_filter = ('created', 'modified', 'iehp_order', 'submission')
