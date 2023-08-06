import warnings
from typing import List

from dorothy_sdk.resources import Dataset, Image
from dorothy_sdk.session import Session
from dorothy_sdk.utils import url_join


class Client:
    _service_host: str = "https://dorothy-image.lps.ufrj.br"

    def __init__(self, token=None, **kwargs):
        self.session = Session(token, **kwargs)
        if kwargs.get("host"):
            warnings.warn(f"Modifying host from {self._service_host} to {kwargs.get('host')}")
            self._service_host = kwargs.get("host")

    def get_datasets(self) -> List[Dataset]:
        request = self.session.get(url_join(self._service_host, Dataset.resource))
        request.raise_for_status()
        datasets = []
        for element in request.json():
            datasets.append(Dataset(session=self.session, host=self._service_host, **element))
        return datasets

    def dataset(self, dataset_id: str) -> Dataset:
        request = self.session.get(url_join(self._service_host, Dataset.resource), params={"search": dataset_id})
        request.raise_for_status()
        if request.status_code == 200:
            return Dataset(session=self.session, host=self._service_host, **[dataset for dataset in request.json() if dataset['name'] == dataset_id][0])
        elif request.status_code == 404:
            return None
        else:
            raise RuntimeError("Unable to fetch dataset")

    def image(self, image_id: str) -> Image:
        request = self.session.get(url_join(self._service_host, Image.resource), params={"search": image_id})
        request.raise_for_status()
        if request.status_code == 200:
            return Image(session=self.session, host=self._service_host, **request.json()[0])
        elif request.status_code == 404:
            return None
        else:
            raise RuntimeError("Unable to fetch image")
