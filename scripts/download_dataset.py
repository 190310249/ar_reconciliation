import os
import shutil
import kagglehub


DATA_DIR = "data/raw"

os.makedirs(DATA_DIR, exist_ok=True)


path = kagglehub.dataset_download(
    "asiryi/ai-powered-erp-ar-reconciliation"
)


for file_name in os.listdir(path):

    if file_name.endswith(".csv"):

        source_path = os.path.join(
            path,
            file_name
        )

        destination_path = os.path.join(
            DATA_DIR,
            "erp_export.csv"
        )

        shutil.copy(
            source_path,
            destination_path
        )