from dorothy_sdk.session import Session
from requests import Session


class Image:
    resource = "images"

    def __init__(self, dataset_name: str, image_url: str, project_id: str,
                 insertion_date: str, metadata: dict, date_acquisition: str, number_reports: int,
                 session: Session, host: str, dataset_id: str = None, *args, **kwargs):
        self.dataset_name = dataset_name
        self.image_url = image_url
        self.project_id = project_id
        self.insertion_date = insertion_date
        self.metadata = metadata
        self.date_acquisition = date_acquisition
        self.number_reports = number_reports
        self.dataset_id = dataset_id
        self._session: Session = session
        self._service_host = host
        self.content = None
        self.image_format = None
        self.download_parameters = None

    def download_image(self, width: int = None, height: int = None, gray_scale: bool = False) -> bytes:
        parameters = {}
        if width:
            parameters["width"] = width
        if height:
            parameters["height"] = height
        parameters["grayscale"] = gray_scale
        self.download_parameters = parameters
        request = self._session.get(self.image_url, params=parameters)
        request.raise_for_status()
        self.image_format = request.headers.get("Content-Type", "image/png").split("/")[-1]
        if request.status_code == 200:
            self.content = request.content
            return request.content
        else:
            raise RuntimeError("Could not download image")

    def save(self, image_path: str = None):
        if not self.content:
            self.download_image()
        if image_path:
            with open(image_path, mode='w') as target_file:
                target_file.write(self.content)
            return
        else:
            with open(f"{self.dataset_name}_{self.project_id}.{self.image_format}", mode="w") as target_file:
                target_file.write(self.content)
            return

