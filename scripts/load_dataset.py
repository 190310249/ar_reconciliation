import os
import sys
import django
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()


from workflows.models import Workflow
from workflows.tasks import ingestion_task


CSV_PATH = "data/raw/erp_export.csv"


df = pd.read_csv(CSV_PATH)

records = df.to_dict(orient="records")


for index, row in enumerate(records):

    external_id = f"ERP-{index}"

    workflow, created = Workflow.objects.get_or_create(

        external_id=external_id,

        defaults={
            "payload": row
        }
    )

    if created:

        ingestion_task.delay(
            str(workflow.workflow_id)
        )