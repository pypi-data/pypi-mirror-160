from dataclasses import dataclass
import hashlib
import time
from typing import Any, Dict, Final

import requests


DEFAULT_BASE_URL: Final = "https://api.podcastindex.org/api/1.0"


@dataclass
class PodcastIndexError(Exception):
    request: requests.Request


@dataclass
class PodcastIndexResponse:
    request: requests.Request
    data: Dict


@dataclass(frozen=True)
class PodcastIndexProvider:

    api_key: str
    api_secret: str
    user_agent: str
    base_url: str = DEFAULT_BASE_URL
    _request = requests.request

    def request(self, method: str, path: str, **kwargs) -> requests.Request:
        timestamp = int(time.time())
        authorization = str(hashlib.sha1(f"{self._api_key}{self._api_secret}{timestamp}".encode("utf8")).hexdigest())
        headers = kwargs.setdefault("headers", {})
        headers.setdefault("User-Agent", self._user_agent)
        headers.setdefault("X-Auth-Key", self._api_key)
        headers.setdefault("X-Auth-Date", str(timestamp))
        headers.setdefault("Authorization", authorization)
        url = f"{self._base_url}{path}"
        response = self._request(method, url, **kwargs)
        if response.status_code not in [requests.status_codes.codes.ok]:
            raise ProcessLookupError(request=response)
        return PodcastIndexResponse(request=response, data=response.json())

    def podcasts_byfeedurl(self, feed_url: Any) -> PodcastIndexResponse:
        return self.request("GET", f"/podcasts/byfeedurl?url={feed_url}")
