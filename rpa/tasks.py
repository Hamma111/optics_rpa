from io import BytesIO

import pandas as pd
from django.core.files.images import ImageFile

from core.utils import get_chrome_instance
from config.celery import app
from rpa.iehp import IEHPScraper
from rpa.models import OpticalPIAOrder, IEHPOrder
from rpa.optical_pia import OpticalPIAScraper
from submissions.models import Submission, OpticalPIAOrderSubmission, IEHPOrderSubmission


@app.task
def place_optical_pia_order(submission_id):
    submission = Submission.objects.get(id=submission_id)
    df = pd.read_csv(submission.file.open("r"), dtype="str")
    df.fillna("", inplace=True)

    orders = []
    order_submissions = []
    for patient_data in df.to_dict(orient='records'):
        order = OpticalPIAOrder.object_from_csv_date(patient_data)
        orders.append(order)
        order_submissions.append(OpticalPIAOrderSubmission(optical_pia_order=order, submission=submission))

    OpticalPIAOrder.objects.bulk_create(orders, batch_size=1000)
    OpticalPIAOrderSubmission.objects.bulk_create(order_submissions, batch_size=1000)

    # running automation
    dr = get_chrome_instance(is_headless=True)
    optical_pia_scraper = OpticalPIAScraper(dr)
    optical_pia_scraper.login()

    for order in orders:
        optical_pia_scraper.place_order(order)
    try:
        dr.quit()
    except:
        pass


@app.task
def place_iehp_order(submission_id):
    submission = Submission.objects.get(id=submission_id)
    df = pd.read_csv(submission.file.open("r"), dtype="str")
    df.fillna("", inplace=True)

    orders = []
    order_submissions = []
    for patient_data in df.to_dict(orient='records'):
        order = IEHPOrder.object_from_csv_date(patient_data)
        orders.append(order)
        order_submissions.append(IEHPOrder(optical_pia_order=order, submission=submission))

    IEHPOrder.objects.bulk_create(orders, batch_size=1000)
    IEHPOrderSubmission.objects.bulk_create(order_submissions, batch_size=1000)

    # running automation
    dr = get_chrome_instance(is_headless=True)
    iehp_scraper = IEHPScraper(dr)
    iehp_scraper.login()

    iehp_scraper.place_vision_referral_requests(orders)
    try:
        dr.quit()
    except:
        pass
