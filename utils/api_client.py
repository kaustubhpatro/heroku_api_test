import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

DEFAULT_TIMEOUT = 10


class APIClient:
    def __init__(self, base_url: str, timeout: Optional[int] = DEFAULT_TIMEOUT):
        self.base = base_url.rstrip('/')
        self.timeout = timeout

    def _log_request(self, method: str, url: str, **kwargs):
        logger.info(f"Request: {method} {url}")
        if 'json' in kwargs:
            logger.info(f"Payload: {kwargs['json']}")
        if 'headers' in kwargs:
            logger.info(f"Headers: {kwargs['headers']}")

    def _log_response(self, response: requests.Response):
        logger.info(f"Response: {response.status_code}")
        try:
            logger.info(f"Response Body: {response.json()}")
        except ValueError:
            logger.warning("Response is not JSON")

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base}{endpoint}"
        self._log_request(method, url, **kwargs)
        try:
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
            self._log_response(response)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def auth(self, user: str, pwd: str) -> str:
        resp = self._request("POST", "/auth", json={"username": user, "password": pwd})
        return resp.json().get("token")

    def create(self, data: dict) -> dict:
        resp = self._request("POST", "/booking", json=data)
        return resp.json()

    def partial_update(self, booking_id: int, data: dict, token: str) -> dict:
        headers = {"Cookie": f"token={token}", "Content-Type": "application/json"}
        resp = self._request("PATCH", f"/booking/{booking_id}", json=data, headers=headers)
        return resp.json()

    def get(self, booking_id: int) -> dict:
        resp = self._request("GET", f"/booking/{booking_id}")
        return resp.json()