import logging

import pandas as pd

from optics.core.utils import get_chrome_instance
from config.celery import app
from optics.rpa.iehp import IEHPScraper
from optics.rpa.models import OpticalPIAOrder, IEHPOrder
from optics.rpa.optical_pia import OpticalPIAScraper
from optics.submissions.choices import StatusType
from optics.submissions.models import Submission, OpticalPIAOrderSubmission, IEHPOrderSubmission

logger = logging.getLogger(__name__)


@app.task
def place_optical_pia_order(submission_id):
    submission = Submission.objects.get(id=submission_id)
    df = pd.read_csv(submission.csv_file.open("r"), dtype="str")
    df.fillna("", inplace=True)

    orders = []
    order_submissions = []
    for patient_data in df.to_dict(orient='records'):
        order = OpticalPIAOrder.object_from_csv_date(patient_data)
        orders.append(order)
        order_submissions.append(OpticalPIAOrderSubmission(order=order, submission=submission))

    OpticalPIAOrder.objects.bulk_create(orders, batch_size=1000)
    OpticalPIAOrderSubmission.objects.bulk_create(order_submissions, batch_size=1000)

    run_automation_optical_pia_order([order.id for order in orders])

    submission.status = StatusType.SUCCESS
    for order_submission in order_submissions:
        if order_submission.status != StatusType.SUCCESS:
            submission.status = StatusType.ERROR
            break

    submission.save(update_fields=["status", "modified"])


@app.task
def run_automation_optical_pia_order(order_ids):
    orders = OpticalPIAOrder.objects.filter(id__in=order_ids)
    dr = get_chrome_instance()
    optical_pia_scraper = OpticalPIAScraper(dr)
    optical_pia_scraper.login()

    for order in orders:
        optical_pia_scraper.place_order(order)

    try:
        dr.quit()
    except Exception as ex:
        logger.error(f"Error closing optical pia order driver Exception: {ex}. Orders: {orders}.")


@app.task
def place_iehp_order(submission_id):
    submission = Submission.objects.get(id=submission_id)
    df = pd.read_csv(submission.csv_file.open("r"), dtype="str")
    df.fillna("", inplace=True)

    orders = []
    order_submissions = []
    for patient_data in df.to_dict(orient='records'):
        order = IEHPOrder.object_from_csv_date(patient_data)
        orders.append(order)
        order_submissions.append(IEHPOrderSubmission(order=order, submission=submission))

    IEHPOrder.objects.bulk_create(orders, batch_size=1000)
    IEHPOrderSubmission.objects.bulk_create(order_submissions, batch_size=1000)

    # running automation
    dr = get_chrome_instance()

    iehp_scraper = IEHPScraper(dr)
    iehp_scraper.login()
    iehp_scraper.place_vision_referral_requests(orders)

    try:
        dr.quit()
    except Exception as ex:
        logger.error(f"Error closing dr in {submission_id}. Error: {ex}")
