from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from rpa.utils import mutate_optical_pia_order
from submissions.choices import StatusType


class OpticalPIAOrder(models.Model):
    subscriber_id = models.CharField(max_length=255)
    subscriber_birthdate = models.CharField(max_length=255)
    service_date = models.CharField(max_length=255)
    issue_date = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)

    material_type = models.CharField(max_length=255)
    focal_options = models.CharField(max_length=255)

    sphere_r = models.CharField(max_length=255)
    sphere_l = models.CharField(max_length=255)
    cylinder_r = models.CharField(max_length=255)
    cylinder_l = models.CharField(max_length=255)
    axis_l = models.CharField(max_length=255)
    axis_r = models.CharField(max_length=255)
    pupillary_far_r = models.CharField(max_length=255)
    pupillary_far_l = models.CharField(max_length=255)
    pupillary_near_l = models.CharField(max_length=255)
    pupillary_near_r = models.CharField(max_length=255)

    add_power_r = models.CharField(max_length=255)
    add_power_l = models.CharField(max_length=255)
    seg_height_l = models.CharField(max_length=255)
    seg_height_r = models.CharField(max_length=255)
    oc_height_l = models.CharField(max_length=255)
    oc_height_r = models.CharField(max_length=255)

    frame_enclosed = models.CharField(max_length=255)

    frame_manufacturer = models.CharField(max_length=255)
    frame_style = models.CharField(max_length=255)
    eye_size = models.CharField(max_length=255)
    bridge_size = models.CharField(max_length=255)
    temple_size = models.CharField(max_length=255)
    color = models.CharField(max_length=255)

    frame_type = models.CharField(max_length=255)

    @classmethod
    def object_from_csv_date(cls, csv_data, mutate=True):
        frame_enclosed = "NEW FRAME ENCLOSED"

        material_type_lookup = {
            "POLYCARBONATE": "POLYCARBONATE",
            "CR39": "CR 39"
        }
        try:
            material_type = material_type_lookup[csv_data["FRAM_RX_LENSMAT"]]
        except KeyError:
            error_msg = f"Received invalid Material Type (FRAM_RX_LENSMAT) in csv row: {csv_data}"
            raise Exception(error_msg)

        focal_options_lookup = {
            "STRAIGHT TOP 28 BF": "Straight Top 28 BF",
            "BF FT-28 POLY": "Straight Top 28 BF",
            "SINGLE VISION (SV)": "Single Vision (SV)"
        }
        try:
            focal_options = focal_options_lookup[csv_data["FRAM_RX_FOCALGUID"].upper()]
        except KeyError:
            error_msg = f"Received invalid Focal Option (FRAM_RX_FOCALGUID) in csv row: {csv_data}"
            raise ValidationError(error_msg)

        frame_type_lookup = {
            "ZYL": "Zyl",
            "METAL": "Metal",
        }
        try:
            frame_type = frame_type_lookup[csv_data["FRAM_RX_FRAMEMAT"].upper()]
        except KeyError:
            error_msg = f"Received invalid Frame Type (FRAM_RX_FRAMEMAT) in csv row: {csv_data}"
            raise Exception(error_msg)

        order = OpticalPIAOrder(
            subscriber_id=csv_data["INSURED_ID"],
            subscriber_birthdate=csv_data["PATIENT_BIRTH"],
            issue_date=date.today().strftime("%m/%d/%Y"),
            service_date=csv_data["FRAM_RX_DATE"],
            gender=csv_data["GENDER"],

            material_type=material_type,
            focal_options=focal_options,

            sphere_r=csv_data["FRAM_RX_R_SPHERE"],
            sphere_l=csv_data["FRAM_RX_L_SPHERE"],
            cylinder_r=csv_data["FRAM_RX_R_CYL"],
            cylinder_l=csv_data["FRAM_RX_L_CYL"],
            axis_r=csv_data["FRAM_RX_R_AXIS"],
            axis_l=csv_data["FRAM_RX_L_AXIS"],

            pupillary_far_r=csv_data["FRAM_RX_MPD_RD"],
            pupillary_near_r=csv_data["FRAM_RX_MPD_RN"],
            pupillary_far_l=csv_data["FRAM_RX_MPD_LD"],
            pupillary_near_l=csv_data["FRAM_RX_MPD_LN"],

            add_power_r=csv_data["FRAM_RX_R_ADD"],
            add_power_l=csv_data["FRAM_RX_L_ADD"],
            seg_height_r=csv_data["FRAM_RX_SEGHGHTGEO"],
            seg_height_l=csv_data["FRAM_RX_SEGHGHTGEO"],
            oc_height_r=csv_data["FRAM_RX_OPTCNTRGEO"] or 0,
            oc_height_l=csv_data["FRAM_RX_OPTCNTRGEO"] or 0,

            frame_enclosed=frame_enclosed,

            frame_manufacturer=csv_data["FRAM_RX_FRAME_MFG"],
            frame_style=csv_data["FRAM_RX_FRAM_STY"],
            eye_size=csv_data["FRAM_RX_EYE"],
            bridge_size=csv_data["FRAM_RX_BRIDGE"],
            temple_size=csv_data["FRAM_RX_TEMPLE"],
            color=csv_data["FRAM_RX_FRAM_CLR"],

            frame_type=frame_type,
        )

        if mutate:
            order = mutate_optical_pia_order(order)

        return order
