import os
from urllib.parse import urljoin
import warnings

import requests


def upload_and_run(base_url, input_file_path, cadata_file_path):
    model_url = urljoin(base_url, "model")
    files = {
        "data_file": open(input_file_path),
        "cadata_file": open(cadata_file_path),
    }
    response = requests.post(model_url, files=files)
    if response.status_code != 200:
        raise RuntimeError(response.json()["detail"]["output"])

    output_lines = response.json()["output"].split("\n")
    model_name = response.json()["model_name"]
    timestamp = response.json()["timestamp"]
    return model_name, timestamp, output_lines


def download_artefact(base_url, model_name, timestamp, input_dir, artefact):
    artefact_url = urljoin(
        base_url, "artefact/%s/%s/%s" % (model_name, timestamp, artefact)
    )
    response_artefact = requests.get(artefact_url)
    if response_artefact.status_code != 200:
        warnings.warn("The requested artefact %s is not available!" % artefact)
    with open(os.path.join(input_dir, artefact), "wb") as file:
        file.write(response_artefact.content)
