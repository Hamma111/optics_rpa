import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optics_rpa.settings')

application = get_wsgi_application()


import pandas as pd
import os

from core.utils import get_chrome_instance
from rpa.models import OpticalPIAOrder
from rpa.optical_pia import OpticalPIAScraper


df = pd.read_csv("rpa/sample.csv", dtype="str")

orders = []
for patient_data in df.to_dict(orient='records'):
    orders.append(OpticalPIAOrder.object_from_csv_date(patient_data))


dr = get_chrome_instance(False)
optical_pia_scraper = OpticalPIAScraper(dr)
optical_pia_scraper.login()
optical_pia_scraper.place_orders(orders[1:2])
