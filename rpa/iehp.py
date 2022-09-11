from io import BytesIO
from datetime import datetime
from time import sleep
from typing import List

from constance import config
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
        ).send_keys("FDIndio")
        WebDriverWait(self.dr, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        ).send_keys("Eyesee01*")
        WebDriverWait(self.dr, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Log In')]"))
        ).click()

    def place_vision_referral_request(self, order: IEHPOrder):
        self.dr.get(config.IEHP_VISION_REFERRAL_REQUEST_FORM_URL)

        WebDriverWait(self.dr, 10).until(
            EC.presence_of_element_located((By.ID, "memberID"))
        ).send_keys(order.iehp_id)
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//label[contains(text(), '{order.service_priority}')]"))
        ).click()
        WebDriverWait(self.dr, 10).until(EC.element_to_be_clickable((By.ID, "postdos"))).click()
        WebDriverWait(self.dr, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"//a[@ng-repeat='item in days' and contains(text(), '{datetime.utcnow().day - 1}')]"))
        ).click()

        sleep(5)

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@title='Please Select A Requesting Provider']"))
        ).click()
        WebDriverWait(self.dr, 10).until(EC.element_to_be_clickable((By.ID, "providerSearchInput"))).send_keys(
            order.location
        )
        WebDriverWait(self.dr, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{order.location}')]"))
        ).click()

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
        ).click()

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//label[contains(text(), '{order.services_requested}')]"))
        ).click()

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.NAME, "icd-0"))
        ).click()
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.ID, "ICDSearch"))
        ).send_keys()
        WebDriverWait(self.dr, 15).until(
            EC.element_to_be_clickable((By.XPATH, f"//strong[contains(text(), '{order.icd_1}')]"))
        ).click()
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close')]"))
        ).click()

        for service in order.materials_services.split(','):
            WebDriverWait(self.dr, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//label[@class='ng-binding' and contains(text(), '{service}')]"))
            ).click()

        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.NAME, "framesDropdownOptions"))
        ).send_keys(order.material_options)

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
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@name='qtySelect-sub-2-0-0']"))
        ).send_keys(order.lens_qty)

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
        WebDriverWait(self.dr, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@name='qtySelect-sub-2-1-0']"))
        ).send_keys(order.frame_qty)

    def place_vision_referral_requests(self, orders: List[IEHPOrder]):
        for index, order in enumerate(orders):
            try:
                self.place_vision_referral_request(order)
                self.dr.save_screenshot(f'success_{index}.png')
            except Exception as ex:
                self.dr.save_screenshot(f'error_{index}.jpg')

    def save_screenshot(self, order, image_field):
        order_submission = order.submission.get(status=StatusType.PENDING)

        image = self.dr.get_screenshot_as_png()
        image = ImageFile(BytesIO(image), name=f'{order_submission.id}.jpg')

        setattr(order_submission, image_field, image)
        order_submission.save(update_fields=[image_field])
