import requests
import os
import copy
import hashlib
import hmac
import json

IMAGE_RESOURCE_URL = "/v1/image"
VIDEO_RESOURCE_URL = "/v1/video"
ENGAGEMENT_RESOURCE_URL = "/v1/engagement"
ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "jpe", "jif", "jfif", "jfi", "png", "gif", "tiff", "tif", "bmp", "svg"]
ALLOWED_VIDEO_EXTENSIONS = ["mp4"]


class SparkAIException(Exception):
    def __init__(self, code, message):
        message = "Exception [{}] {}".format(code, message)
        super(SparkAIException, self).__init__(message)


class SparkAIClient(object):
    def __init__(self, api_key, sandbox=False):
        self.api_key = api_key
        self.headers = {"Authorization": "Bearer " + self.api_key}
        if "SPARKAI_HOST" in os.environ:
            self.base_url = os.environ["SPARKAI_HOST"]
        elif sandbox:
            self.base_url = "https://sandbox.spark.ai"
        else:
            self.base_url = "https://app.spark.ai"

    def _post(self, path, json=None, files=None, data=None):
        r = requests.post(path, headers=self.headers, files=files, json=json, data=data)
        if r.status_code == 200:
            return r.json()
        else:
            try:
                print(r.json())
                message = r.json()["message"]
                raise SparkAIException(r.status_code, message)
            except:
                raise SparkAIException(r.status_code, r.text)

    def _get(self, path, query_params):
        r = requests.get(path, headers=self.headers, params=query_params)
        if r.status_code == 200:
            return r.json()
        else:
            try:
                print(r.json())
                message = r.json()["message"]
                raise SparkAIException(r.status_code, message)
            except:
                raise SparkAIException(r.status_code, r.text)

    def _make_payload(self, content_location, program_name, instructions, metadata, label_list, annotations, **kwargs):
        content_type = kwargs.get("content_type", "image")
        d = {
            "content_location": content_location,
            "content_type": content_type,
            "program_name": program_name,
            "instructions": instructions,
            "metadata": metadata,
            "priors": {"label_list": label_list, "annotations": annotations},
        }
        if d["priors"]["label_list"] is None and d["priors"]["annotations"] is None:
            d["priors"] = None
        return {k: v for k, v in d.items() if v is not None}

    def _create_engagement_from_url(
        self, url, program_name=None, instructions=None, metadata=None, label_list=None, annotations=None, **kwargs
    ):
        video = kwargs.get("video", False)
        if isinstance(url, list):
            url = list(map(lambda x: x.strip(), url))
        else:
            url = url.strip()
        content_type = "video" if video else "image"
        engagement_data = self._make_payload(
            url, program_name, instructions, metadata, label_list, annotations, content_type=content_type
        )
        return self._post(path=self.base_url + ENGAGEMENT_RESOURCE_URL, json=engagement_data)

    def upload_binary(self, media_binary, filename, tag=None, **kwargs):
        video = kwargs.get("video", False)
        if not video:
            allowed_extensions = ALLOWED_IMAGE_EXTENSIONS
            form_data_name = "image_file"
            resource_url = IMAGE_RESOURCE_URL
        else:
            allowed_extensions = ALLOWED_VIDEO_EXTENSIONS
            form_data_name = "video_file"
            resource_url = VIDEO_RESOURCE_URL

        split_filename = filename.split(".")
        if len(split_filename) != 2:
            raise ValueError("Invalid filename: " + filename)
        [extensionless, extension] = split_filename
        if extension not in allowed_extensions:
            raise ValueError("Extension " + extension + " not in allowed extensions " + ",".join(allowed_extensions))
        extensionless = extensionless or "media"
        files = {
            form_data_name: (extensionless + "." + extension, media_binary, "multipart/form-data", {"Expires": "0"})
        }
        data = {} if tag is None else {"tag": tag}
        return self._post(path=self.base_url + resource_url, files=files, data=data)

    def upload_image(self, file_path, tag=None):
        with open(file_path, "rb") as file:
            binary_image = file.read()
        image_name = os.path.basename(file_path)
        return self.upload_binary(binary_image, image_name, tag)

    def upload_video(self, file_path, tag=None):
        with open(file_path, "rb") as file:
            binary_video = file.read()
        video_name = os.path.basename(file_path)
        return self.upload_binary(binary_video, video_name, tag, video=True)

    def create_annotation(self, vertices, type, label, metadata, image_idx=None):
        d = {"vertices": vertices, "type": type, "label": label, "metadata": metadata, "image_idx": image_idx}
        return {k: v for k, v in d.items() if v is not None}

    def create_engagement_from_image_url(
        self, image_url, program_name=None, instructions=None, metadata=None, label_list=None, annotations=None
    ):
        return self._create_engagement_from_url(
            image_url, program_name, instructions, metadata, label_list, annotations
        )

    def create_engagement_from_file(
        self,
        file_path,
        program_name=None,
        instructions=None,
        metadata=None,
        label_list=None,
        annotations=None,
        **kwargs
    ):
        video = kwargs.get("video", False)
        if video:
            upload_url = self.upload_video(file_path)["url"]
        else:
            upload_url = self.upload_image(file_path)["url"]
        return self._create_engagement_from_url(
            upload_url, program_name, instructions, metadata, label_list, annotations, video=video
        )

    def create_engagement_from_media_binary(
        self,
        media_binary,
        filename,
        program_name=None,
        instructions=None,
        metadata=None,
        label_list=None,
        annotations=None,
        **kwargs
    ):
        video = kwargs.get("video", False)
        upload_url = self.upload_binary(media_binary, filename, None, video=video)["url"]
        return self._create_engagement_from_url(
            upload_url, program_name, instructions, metadata, label_list, annotations, video=video
        )

    def create_engagement_from_video_url(
        self, video_url, program_name=None, instructions=None, metadata=None, label_list=None
    ):
        return self._create_engagement_from_url(
            video_url, program_name, instructions, metadata, label_list, None, video=True
        )

    def get_engagements(self, query_params={}, limit=10, cursor=0, count="false", engagement_id=None):
        id_str = "" if engagement_id is None else ("/" + engagement_id)
        _query_params = copy.deepcopy(query_params)
        if not engagement_id:
            if "limit" not in query_params:
                _query_params["limit"] = limit
            if "cursor" not in query_params:
                _query_params["cursor"] = cursor
            if "count" not in query_params:
                _query_params["count"] = count
        return self._get(path=self.base_url + ENGAGEMENT_RESOURCE_URL + id_str, query_params=_query_params)

    def validate_webhook_secret(self, request_secret_header, request_body, self_secret):

        split_header = request_secret_header.split("t=")[1].split(",v1=")
        timestamp = split_header[0]
        received_hash = split_header[1]

        json_payload = json.dumps(request_body, separators=(",", ":"))
        hash_payload = timestamp + "." + json_payload

        byte_key = bytes(self_secret, "UTF-8")
        message = hash_payload.encode()

        h = hmac.new(byte_key, message, hashlib.sha256).hexdigest()

        return h == received_hash
