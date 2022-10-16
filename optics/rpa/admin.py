from django.contrib import admin

from .models import OpticalPIAOrder, IEHPOrder


@admin.register(OpticalPIAOrder)
class OpticalPIAOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'subscriber_id',
        'subscriber_birthdate',
        'service_date',
        'issue_date',
        'gender',
        'material_type',
        'focal_options',
        'sphere_r',
        'sphere_l',
        'cylinder_r',
        'cylinder_l',
        'axis_l',
        'axis_r',
        'pupillary_far_r',
        'pupillary_far_l',
        'pupillary_near_l',
        'pupillary_near_r',
        'add_power_r',
        'add_power_l',
        'seg_height_l',
        'seg_height_r',
        'oc_height_l',
        'oc_height_r',
        'frame_enclosed',
        'frame_manufacturer',
        'frame_style',
        'eye_size',
        'bridge_size',
        'temple_size',
        'color',
        'frame_type',
        'confirmation_number',
        'pdf_file',
    )
    list_filter = ('created', 'modified')


@admin.register(IEHPOrder)
class IEHPOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'iehp_id',
        'appointment_date',
        'requesting_provider',
        'location',
        'icd_1',
        'lens_cpt_1',
        'frame_cpt_1',
        'confirmation_number',
    )
    list_filter = ('created', 'modified')
