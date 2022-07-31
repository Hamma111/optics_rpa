from dataclasses import dataclass
from datetime import date

from rpa.utils import mutate_optical_pia_order


@dataclass
class OpticalPIAOrder:
    subscriber_id: str
    subscriber_birthdate: str
    service_date: str
    issue_date: str
    gender: str

    material_type: str
    focal_options: str

    sphere_r: str
    sphere_l: str
    cylinder_r: str
    cylinder_l: str
    axis_l: str
    axis_r: str
    pupillary_far_r: str
    pupillary_far_l: str
    pupillary_near_l: str
    pupillary_near_r: str

    add_power_r: str
    add_power_l: str
    seg_height_l: str
    seg_height_r: str
    oc_height_l: str
    oc_height_r: str

    frame_enclosed: str

    frame_manufacturer: str
    frame_style: str
    eye_size: str
    bridge_size: str
    temple_size: str
    color: str

    frame_type: str

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
            "Single Vision (SV)": "Single Vision (SV)"
        }
        try:
            focal_options = focal_options_lookup[csv_data["FRAM_RX_LENSGUID"]]
        except KeyError:
            error_msg = f"Received invalid Focal Option (FRAM_RX_LENSGUID) in csv row: {csv_data}"
            raise Exception(error_msg)

        frame_type_lookup = {
            "DR. SUP - TO COME": "New Frame Enclosed",
        }
        try:
            frame_type = frame_type_lookup[csv_data["FRAM_RX_FRAMESPPLYR"]]
        except KeyError:
            error_msg = f"Received invalid Frame Type (FRAM_RX_FRAMESPPLYR) in csv row: {csv_data}"
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
            seg_height_r=csv_data["FRAM_RX_OPTCNTRGEO"] or 0,
            seg_height_l=csv_data["FRAM_RX_OPTCNTRGEO"] or 0,
            oc_height_r=csv_data["FRAM_RX_FRAMEMAT"],
            oc_height_l=csv_data["FRAM_RX_FRAMEMAT"],

            frame_enclosed=frame_enclosed,

            frame_manufacturer=csv_data["FRAM_RX_FRAME_MFG"],
            frame_style=csv_data["FRAM_RX_FRAM_STY"],
            eye_size=csv_data["FRAM_RX_EYE"],
            bridge_size=csv_data["FRAM_RX_BRIDGE"],
            temple_size=csv_data["FRAM_RX_TEMPLE"],
            color=csv_data["FRAM_RX_FRAM_CLR"],

            frame_type=csv_data['FRAM_RX_FRAMEMAT'],
        )

        if mutate:
            order = mutate_optical_pia_order(order)

        return order
