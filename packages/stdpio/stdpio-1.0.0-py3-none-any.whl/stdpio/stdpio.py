import os
import time
import requests
import threading
import hashlib
import json
from datetime import datetime


class stdpio:

    API = "https://stdp.io/api/"
    ENDPOINTS = {
        "auth": "{}token-auth".format(API),
        "my_models": "{}my-models".format(API),
        "download_model": "{}download-model".format(API),
        "get_prototype": "{}prototypes".format(API),
        "has_face": "{}utils/has-face".format(API),
        "redgreen": "{}utils/redgreen".format(API),
        "redgreen_reset": "{}utils/redgreen/reset".format(API),
    }

    def __init__(self, **kwargs):
        # init values
        self.models_to_sync = []
        self.akida_models = {}

        self.last_sync = (
            ""  # datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        )
        self.token = False

        # set credentials
        if kwargs.get("username") and kwargs.get("password"):
            self.username = kwargs.get("username")
            self.password = kwargs.get("password")
            self.authenticate()
        elif kwargs.get("token"):
            self.token = kwargs.get("token")

        # set the interval and sync directory
        self.interval = kwargs.get("interval", 5)
        self.model_dir = kwargs.get("model_dir", "/tmp/")

        # watch and sync
        self.model_sync = threading.Thread(target=self.fetch_and_sync_models)
        self.model_sync.start()

    def query(self, method, **kwargs):
        r = requests.request(method, **kwargs)
        if r.status_code == 200:
            return r.json()

    def authenticate(self):
        data = self.query(
            "post",
            url=self.ENDPOINTS.get("auth"),
            data={"username": self.username, "password": self.password},
        )
        if data:
            self.token = data.get("token")

    def get_token(self):
        return self.token

    def get_prototype(self, unique_id):
        url = "{}/{}/".format(self.ENDPOINTS.get("get_prototype"), unique_id)
        data = self.query(
            "get",
            url=url,
            headers={"Authorization": "Token {}".format(self.token)},
        )
        return data

    def has_face(self, frame, min_accuracy=False, hittest=False):
        url = "{}/{}".format(self.ENDPOINTS.get("has_face"), "has_face.jpeg")

        data = self.query(
            "put",
            url=url,
            headers={
                "Content-Type": "image/jpeg",
                "Authorization": "Token {}".format(self.token),
            },
            data=frame,
            params={"min_accuracy": min_accuracy, "hittest": hittest},
        )
        if data.get("status", True):
            data["boxes"] = json.loads(data["boxes"])
        return data

    def redgreen_reset(self, prototype):
        data = {"prototype": prototype}
        data = self.query(
            "post",
            url=self.ENDPOINTS.get("redgreen_reset"),
            headers={
                "Authorization": "Token {}".format(self.token),
            },
            data=data,
        )
        return data

    def redgreen(self, prototype_uuid, frame, neuron=False):
        url = "{}/{}".format(self.ENDPOINTS.get("redgreen"), "redgreen.jpeg")
        params = {"prototype": prototype_uuid}
        if type(neuron) is int:
            params["neuron"] = neuron
        data = self.query(
            "put",
            url=url,
            headers={
                "Content-Type": "image/jpeg",
                "Authorization": "Token {}".format(self.token),
            },
            params=params,
            data=frame,
        )
        return data

    def fetch_model_file(self, model):
        filepath = self.get_filepath(model.get("unique_id"))
        if filepath:
            with requests.get(
                self.ENDPOINTS.get("download_model"),
                stream=True,
                headers={"Authorization": "Token {}".format(self.token)},
                params={"unique_id": model["unique_id"]},
            ) as r:
                r.raise_for_status()
                with open(filepath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                return filepath

    def fetch_known(self, model):
        labels = model.get("labels")
        learned = model.get("learned")
        if labels or learned:
            known = {
                "labels": labels,
                "learned": learned,
            }
            return known

    def my_models(self, *args, **kwargs):
        data = self.query(
            "get",
            url=self.ENDPOINTS.get("my_models"),
            headers={"Authorization": "Token {}".format(self.token)},
            params=dict(kwargs, format="json"),
        )
        return data

    def get_model(self, unique_id):
        data = self.query(
            "get",
            url="{}/{}".format(self.ENDPOINTS.get("my_models"), unique_id),
            headers={"Authorization": "Token {}".format(self.token)},
            params={"format": "json"},
        )
        return data

    def sync_model(self, unique_id):
        if unique_id not in self.models_to_sync:
            self.models_to_sync.append(unique_id)

    def unsync_model(self, unique_id):
        if unique_id in self.models_to_sync:
            self.models_to_sync.remove(unique_id)

    def fetch_and_sync_models(self):
        while True:
            if len(self.models_to_sync) > 0:

                # if file isnt there, fetch
                for model in self.models_to_sync:
                    filepath = self.get_filepath(model)
                    if not os.path.isfile(filepath):
                        self.last_sync = ""

                try:
                    q = {
                        "unique_id__in": ",".join(self.models_to_sync),
                        "updated_at__gte": self.last_sync,
                    }
                    models = self.my_models(**q)
                    if models and len(models) > 0:
                        for model in models:
                            # check if its in the list of available models
                            if model["unique_id"] in self.akida_models:
                                # remove it temporarily
                                del self.akida_models[model["unique_id"]]

                            # get md5 of current file if exists
                            last_md5 = self.model_md5(model["unique_id"])

                            # fetch model from site and return filepath
                            filepath = self.fetch_model_file(model)
                            # add model back to available list
                            akida_model = {
                                "model": model,
                                "filepath": filepath,
                                "md5": self.model_md5(model["unique_id"]),
                                "last_md5": last_md5,
                            }
                            self.akida_models[model["unique_id"]] = akida_model
                        self.last_sync = datetime.utcnow().strftime(
                            "%Y-%m-%dT%H:%M:%S.%fZ"
                        )
                        # print("=== fetched {} ===".format(len(models)))
                    else:
                        # print("=== nothing fetched ===")
                        pass

                except Exception as e:
                    pass
                    # handle bad model sync

                time.sleep(self.interval)

    def get_filepath(self, unique_id):
        filename = "{}.fbz".format(unique_id)
        local_storage_path = os.path.join(self.model_dir, filename)
        return local_storage_path

    def model_md5(self, unique_id):
        filepath = self.get_filepath(unique_id)
        if filepath and os.path.isfile(filepath):
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        return None

    def get_model_object(self, unique_id):
        if unique_id in self.akida_models:
            akida_model = self.akida_models[unique_id]
            return akida_model
        return None

    def get_model_path(self, unique_id):
        model = self.get_model_object(unique_id)
        if model:
            if os.path.isfile(model["filepath"]):
                if model["last_md5"] == model["md5"] and model.get(
                    "loaded", False
                ):
                    return None

                if (
                    model["last_md5"] is None
                    or not model.get("loaded", False)
                    or model["last_md5"] != model["md5"]
                ):
                    model["loaded"] = True
                    return model["filepath"]
        return None
