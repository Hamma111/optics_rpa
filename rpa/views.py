import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render


# class PlaceOpticalPIAOrderView()
from core.utils import get_chrome_instance
from rpa.models import OpticalPIAOrder
from rpa.optical_pia import OpticalPIAScraper
from rpa.tasks import place_optical_pia_order


def index_page(request):
    # place_optical_pia_order.delay()
    df = pd.read_csv("rpa/sample.csv", dtype="str")

    orders = []
    for patient_data in df.to_dict(orient='records'):
        orders.append(OpticalPIAOrder.object_from_csv_date(patient_data))

    dr = get_chrome_instance(is_headless=False)
    optical_pia_scraper = OpticalPIAScraper(dr)
    optical_pia_scraper.login()
    optical_pia_scraper.place_orders(orders[:])
    dr.quit()
    return HttpResponse(b"done")
