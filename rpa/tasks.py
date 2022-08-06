import pandas as pd

from core.utils import get_chrome_instance
from config.celery import app
from rpa.models import OpticalPIAOrder
from rpa.optical_pia import OpticalPIAScraper


@app.task
def place_optical_pia_order():

    df = pd.read_csv("rpa/sample.csv", dtype="str")

    orders = []
    for patient_data in df.to_dict(orient='records'):
        orders.append(OpticalPIAOrder.object_from_csv_date(patient_data))

    dr = get_chrome_instance(is_headless=True)
    optical_pia_scraper = OpticalPIAScraper(dr)
    optical_pia_scraper.login()
    optical_pia_scraper.place_orders(orders[1:2])

