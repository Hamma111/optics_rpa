import logging

import pandas as pd


logger = logging.getLogger(__name__)


def validate_uploaded_file(csv_file):
    if not csv_file.name.endswith('.csv'):
        raise Exception('File is not CSV type')
    if csv_file.multiple_chunks():
        raise Exception("Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))

    try:
        df = pd.read_csv(csv_file.temporary_file_path())
    except Exception as ex:
        raise Exception(f"{ex}")
