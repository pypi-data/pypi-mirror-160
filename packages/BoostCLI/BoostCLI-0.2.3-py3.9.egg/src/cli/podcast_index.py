import hashlib
import time
from typing import Any, Final, Optional

import requests
from requests.api import head


class PodcastIndexService:

    DEFAULT_BASE_URL: Final = "https://api.podcastindex.org/api/1.0"

    _base_url: str = DEFAULT_BASE_URL
    _api_key: str
    _api_secret: str
    _user_agent: str

    def __init__(self, api_key: str, api_secret: str, user_agent: Optional[str] = None):
        self._api_key = api_key
        self._api_secret = api_secret
        self._user_agent = user_agent

    def _request(self, method: str, path: str, **kwargs) -> requests.Request:
        timestamp = int(time.time())
        authorization = str(hashlib.sha1(f"{self._api_key}{self._api_secret}{timestamp}".encode("utf8")).hexdigest())
        headers = kwargs.setdefault("headers", {})
        headers.setdefault("User-Agent", self._user_agent)
        headers.setdefault("X-Auth-Key", self._api_key)
        headers.setdefault("X-Auth-Date", str(timestamp))
        headers.setdefault("Authorization", authorization)
        url = f"{self._base_url}{path}"
        return requests.request(method, url, **kwargs)

    def podcasts_byfeedurl(self, feed_url: Any) -> requests.Request:
        return self._request("GET", f"/podcasts/byfeedurl?url={feed_url}")
        