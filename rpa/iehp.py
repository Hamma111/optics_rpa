from io import BytesIO
from datetime import datetime
from time import sleep
from typing import List

from constance import config
from django.conf import settings
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.core.files.images import ImageFile

from rpa.models import IEHPOrder
from submissions.choices import StatusType


class IEHPScraper:
    def __init__(self, dr):
        self.dr = dr

    def login(self):
        self.dr.get(config.IEHP_LOGIN_URL)

        WebDriverWait(self.dr, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        ).send_keys(settings.IEHP_LOGIN_ID)
        WebDriverWait(self.dr, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        ).send_keys(settings.IEHP_PASSWORD)
        WebDriverWait(self.dr, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Log In')]"))
        ).click()
        sleep(5)

    def _place_vision_referral_request(self, order: IEHPOrder):
        self.dr.get(config.IEHP_VISION_REFERRAL_REQUEST_FORM_URL)

        WebDriverWait(self.dr, 30).until(
            EC.presence_of_element_located((By.ID, "memberID"))
        ).send_keys(order.iehp_id)
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//label[contains(text(), 'Standard Post-Service')]"))
        ).click()
        WebDriverWait(self.dr, 10).until(EC.element_to_be_clickable((By.ID, "postdos"))).click()

        day = order.appointment_date.split("/")[1]
        try:
            WebDriverWait(self.dr, 10).until(EC.element_to_be_clickable(
                (By.XPATH, f"//a[@ng-repeat='item in days' and contains(text(), '{day}')]"))
            ).click()
        except TimeoutException as e:
            print(f"error {e} with {order.__dict__} in IEHP appt date selection.")
            WebDriverWait(self.dr, 1).until(EC.element_to_be_clickable(
                (By.XPATH, f"//a[@ng-click='prevMonth()']"))
            ).click()
            WebDriverWait(self.dr, 10).until(EC.element_to_be_clickable(
                (By.XPATH, f"//a[@ng-repeat='item in days' and contains(text(), '{day}')]"))
            ).click()

        sleep(5)

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@title='Please Select A Requesting Provider']"))
        ).click()
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.ID, "providerSearchInput"))
        ).send_keys(order.requesting_provider)
        WebDriverWait(self.dr, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{order.location}')]"))
        ).click()
        sleep(5)

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
        ).click()

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//label[contains(text(), 'Materials')]"))
        ).click()

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.NAME, "icd-0"))
        ).click()
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.ID, "ICDSearch"))
        ).send_keys(order.icd_1)
        WebDriverWait(self.dr, 15).until(
            EC.element_to_be_clickable((By.XPATH, f"//strong[contains(text(), '{order.icd_1}')]"))
        ).click()
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close')]"))
        ).click()

        # for service in order.materials_services.split(','):
        #     WebDriverWait(self.dr, 5).until(
        #         EC.element_to_be_clickable(
        #             (By.XPATH, f"//label[@class='ng-binding' and contains(text(), '{service}')]"))
        #     ).click()

        WebDriverWait(self.dr, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//label[@class='ng-binding' and contains(text(), 'Lenses')]"))
        ).click()
        WebDriverWait(self.dr, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//label[@class='ng-binding' and contains(text(), 'Frames')]"))
        ).click()

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.NAME, "framesDropdownOptions"))
        ).send_keys("Replacement of lost/broken/stolen materials")

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='cpt-sub-2-0-0']"))
        ).click()
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//strong[@class='ng-binding' and contains(text(), '{order.lens_cpt_1}')]")
            )).click()
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='vc.close()']"))
        ).click()
        try:
            WebDriverWait(self.dr, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@name='qtySelect-sub-2-0-0']"))
            ).send_keys("2")  # lenses Qty
        except TimeoutException:
            pass

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='cpt-sub-2-1-0']"))
        ).click()
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//strong[@class='ng-binding' and contains(text(), '{order.frame_cpt_1}')]"))
        ).click()
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='vc.close()']"))
        ).click()
        try:
            WebDriverWait(self.dr, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@name='qtySelect-sub-2-1-0']"))
            ).send_keys("1")  # frames Qty
        except TimeoutException:
            pass

        oath_checkbox_els = WebDriverWait(self.dr, 1).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH,
                 "//span[contains(text(), ' 1. Member has supplied the provider with a signed statement under')]",
                 ))
        )
        oath_checkbox_els[0].click()
        oath_checkbox_els[1].click()

        self.save_screenshot(order, "screenshot1")

    def place_vision_referral_requests(self, orders: List[IEHPOrder]):
        for index, order in enumerate(orders):
            try:
                self._place_vision_referral_request(order)
                order_submission = order.submission.get(status=StatusType.PENDING)
                order_submission.status = StatusType.SUCCESS
            except Exception as ex:
                self.save_screenshot(order, "error_screenshot")
                order_submission = order.submission.get(status=StatusType.PENDING)
                order_submission.status = StatusType.ERROR
                order_submission.error_text = ex

            order_submission.save(update_fields=["status", "error_text"])

    def save_screenshot(self, order, image_field):
        order_submission = order.submission.get(status=StatusType.PENDING)

        image = self.dr.get_screenshot_as_png()
        image = ImageFile(BytesIO(image), name=f'{order_submission.id}.jpg')

        setattr(order_submission, image_field, image)
        order_submission.save(update_fields=[image_field])
