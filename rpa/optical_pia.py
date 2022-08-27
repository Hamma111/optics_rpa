from io import BytesIO
from time import sleep
from typing import List

from constance import config
from django.core.files.images import ImageFile
from selenium.webdriver.common.by import By

from core.utils import send_keys_to_element, close_alert_pop_ups
from rpa.models import OpticalPIAOrder
from submissions.choices import StatusType


class OpticalPIAScraper:
    def __init__(self, dr):
        self.dr = dr

    def login(self):
        self.dr.get(config.OPTICAL_PIA_LOGIN_URL)

        userid_element = self.dr.find_element(By.ID, "txtUserID")
        password_element = self.dr.find_element(By.ID, "txtPassword")
        submit_element = self.dr.find_element(By.XPATH, "//input[@type='submit']")

        userid_element.send_keys(config.OPTICAL_PIA_USERID)
        password_element.send_keys(config.OPTICAL_PIA_PASSWORD)
        submit_element.click()
        assert self.dr.current_url != config.OPTICAL_PIA_LOGIN_URL

    def _start_order(self, order: OpticalPIAOrder):
        self.dr.get(config.OPTICAL_PIA_START_ORDER_URL)
        self.dr.find_element(By.ID, "txtMediCalID").send_keys(order.subscriber_id)
        self.dr.find_element(By.ID, "txtDateofBirth").send_keys(order.subscriber_birthdate)
        self.dr.find_element(By.ID, "txtDateofIssue").send_keys(order.issue_date)
        self.dr.find_element(By.ID, "txtDateofService").send_keys(order.service_date)
        if order.gender in ("m", "M", "male", "Male", "MALE"):
            self.dr.find_element(By.ID, "ChkMale").click()
        elif order.gender in ("f", "F", "female", "Female", "FEMALE"):
            self.dr.find_element(By.ID, "ChkFemale").click()
        else:
            raise Exception(f"Invalid Gender value in order {order}")

        self.dr.find_element(By.ID, "butVerifyEligibility").click()
        self.save_screenshot(order, "screenshot1")

    def _place_order(self, order):
        self._start_order(order)

        self.dr.find_element(By.ID, "ddlMaterialType").send_keys(order.material_type)
        close_alert_pop_ups(self.dr, 2, 2, attempt_jumping_to_next_element=False)
        close_alert_pop_ups(self.dr, 2)

        self.dr.find_element(By.ID, "ddlFocalOptions").send_keys(order.focal_options)

        self.dr.find_element(By.ID, "txtRSphere").send_keys(order.sphere_r)
        self.dr.find_element(By.ID, "txtLSphere").send_keys(order.sphere_l)

        close_alert_pop_ups(self.dr)
        self.dr.find_element(By.ID, "txtRCylinder").send_keys(order.cylinder_r)
        self.dr.find_element(By.ID, "txtLCylinder").send_keys(order.cylinder_l)

        close_alert_pop_ups(self.dr)
        send_keys_to_element(self.dr.find_element(By.ID, "txtRAxis"), order.axis_r)
        send_keys_to_element(self.dr.find_element(By.ID, "txtLAxis"), order.axis_l)

        close_alert_pop_ups(self.dr)
        send_keys_to_element(self.dr.find_element(By.ID, "txtRFar"), order.pupillary_far_r)
        send_keys_to_element(self.dr.find_element(By.ID, "txtLFar"), order.pupillary_far_l)

        close_alert_pop_ups(self.dr)
        send_keys_to_element(self.dr.find_element(By.ID, "txtRNear"), order.pupillary_near_r)
        send_keys_to_element(self.dr.find_element(By.ID, "txtLNear"), order.pupillary_near_l)

        close_alert_pop_ups(self.dr)
        send_keys_to_element(self.dr.find_element(By.ID, "txtRAddPower"), order.add_power_r)
        send_keys_to_element(self.dr.find_element(By.ID, "txtLAddPower"), order.add_power_l)

        close_alert_pop_ups(self.dr)
        send_keys_to_element(self.dr.find_element(By.ID, "txtRSegHeight"), order.seg_height_r)
        close_alert_pop_ups(self.dr)
        send_keys_to_element(self.dr.find_element(By.ID, "txtLSegHeight"), order.seg_height_l)
        close_alert_pop_ups(self.dr)

        close_alert_pop_ups(self.dr)
        self.dr.find_element(By.ID, "txtROCHeight").send_keys(order.oc_height_r)
        close_alert_pop_ups(self.dr)
        self.dr.find_element(By.ID, "txtLOCHeight").send_keys(order.oc_height_l)
        close_alert_pop_ups(self.dr)

        self.dr.find_element(By.ID, "ddlFrameEnclosed").send_keys(order.frame_enclosed)

        self.dr.find_element(By.ID, "txtFrameManufacturer").send_keys(order.frame_manufacturer)
        self.dr.find_element(By.ID, "txtFrameStyle").send_keys(order.frame_style)
        self.dr.find_element(By.ID, "txtEyeSize").send_keys(order.eye_size)
        self.dr.find_element(By.ID, "txtBridgeSize").send_keys(order.bridge_size)
        self.dr.find_element(By.ID, "txtTemple").send_keys(order.temple_size)
        self.dr.find_element(By.ID, "txtColor").send_keys(order.color)
        self.dr.find_element(By.ID, "selFrameMaterial").send_keys(order.frame_type)

        self.dr.find_element(By.ID, "chkCertifiedSOC").click()
        self.save_screenshot(order, "screenshot2")

    def place_order(self, order):
        try:
            self._place_order(order)
            order_submission = order.submission.get(status=StatusType.PENDING)
            order_submission.status = StatusType.SUCCESS
        except Exception as ex:
            self.save_screenshot(order, "error_screenshot")
            order_submission = order.submission.get(status=StatusType.PENDING)
            order_submission.status = StatusType.ERROR
            order_submission.error_text = ex

        order_submission.save(update_fields=["status", "error_text"])

    def place_orders(self, optical_pia_orders: List[OpticalPIAOrder]):
        for index, order in enumerate(optical_pia_orders):
            try:
                self.place_order(order)
                self.dr.save_screenshot(f'success_{index}.png')
            except Exception as ex:
                self.dr.save_screenshot(f'error_{index}.jpg')

    def save_screenshot(self, order, image_field):
        order_submission = order.submission.get(status=StatusType.PENDING)

        image = self.dr.get_screenshot_as_png()
        image = ImageFile(BytesIO(image), name=f'{order_submission.id}.jpg')

        setattr(order_submission, image_field, image)
        order_submission.save(update_fields=[image_field])

