"""
    CUSTOM FALCON READER CLASSES
"""
import os
from typing import Generator, Callable, Set

import requests

from sdc_dp_helpers.api_utilities.date_managers import date_handler, date_range
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.retry_managers import request_handler, retry_handler


class CustomFalconReader:
    """
    Custom Falcon Reader
    """

    def __init__(self, creds_file: str, config_file=None):
        self._creds: dict = load_file(creds_file, "yml")
        self._config: dict = load_file(config_file, "yml")

        self.request_session: requests.Session = requests.Session()
        self.base_url: str = "https://api.falcon.io/"
        self.datasets: list = []

    @retry_handler(exceptions=ConnectionError, total_tries=5)
    def _get_channel_ids(self) -> Set[str]:
        """
        Gather all available channel ids.
        """
        print("GET: channel ids.")
        url = f"https://api.falcon.io/channels?apikey={self._creds['api_key']}"
        response = self.request_session.get(url=url, params={"limit": "9999"})

        response_data = response.json()
        if response.status_code == 200:
            channel_ids = set()
            for item in response_data.get("items", []):
                channel_ids.add(item["id"])

            return channel_ids

        raise ConnectionError(
            f"Falcon API failed to return channel ids. "
            f"Status code: {response.status_code}, Reason: {response.reason}."
        )

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 2)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    @retry_handler(exceptions=TimeoutError, total_tries=5, initial_wait=900)
    def _content_by_channel_id(self, date: str, channel_id: str) -> list:

        dataset: list = []
        endpoint_url: str = (
            f"{self._config['endpoint']}?apikey={self._creds['api_key']}"
        )
        offset: int = 0
        limit = self._config.get("limit", 200)
        while True:
            req = requests.Request(
                method=self._config.get("method", "POST"),
                url=f"{self.base_url}{endpoint_url}",
                headers={"Content-Type": "application/json"},
                json={
                    "metrics": self._config.get("metrics", []),
                    "channels": [channel_id],
                    "since": date,
                    "until": date,
                    "postsSince": date,
                    "postsUntil": date,
                    "direction": self._config.get("direction", "ASC"),
                    "limit": limit,
                    "offset": offset,
                },
            )
            prepped = self.request_session.prepare_request(req)
            response = self.request_session.send(
                prepped,
            )
            status_code: int = response.status_code
            reason: str = response.reason
            if status_code == 200:
                results: dict = response.json()
                offset += limit
                if len(results) == 0:
                    break  # we will exit the loop because no data is got back
                dataset.extend(results)
                # if len(dataset) > 150:
                #     break
            elif reason == "Not Found" and status_code == 404:
                print(f"No data for channel id: {channel_id}, skipping.\n")
                break
            elif status_code == 429:
                raise TimeoutError("Rolling Window Quota [429] reached.")
            else:
                raise ConnectionError(f"Reason: {reason}, Status: {status_code}.")

        return dataset

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 2)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    @retry_handler(exceptions=TimeoutError, total_tries=5, initial_wait=900)
    def _published_posts_by_channel_id(self, date: str, channel_id: str) -> list:

        dataset: list = []
        endpoint_url: str = (
            f"{self._config['endpoint']}?apikey={self._creds['api_key']}"
        )
        while endpoint_url:
            req = requests.Request(
                method=self._config.get("method", "GET"),
                url=f"{self.base_url}{endpoint_url}",
                headers={"Content-Type": "application/json"},
                json={
                    "channels": [channel_id],
                    "since": date,
                    "until": date,
                    "networks": self._config["networks"],
                    "statuses": self._config.get("statuses", "published"),
                },
            )
            prepped = self.request_session.prepare_request(req)
            response = self.request_session.send(
                prepped,
            )
            status_code: int = response.status_code
            reason: str = response.reason
            if response.status_code == 200:
                results: dict = response.json()
                items_data: list = results.get("items", [])
                dataset.extend(items_data)

                endpoint_url = results.get("next", {"href": None}).get("href")
                # print(endpoint_url)

                if len(items_data) == 0 or endpoint_url is None:
                    break

            elif reason == "Not Found" and status_code == 404:
                print(f"No data for channel id: {channel_id}, skipping.\n")
                break
            elif status_code == 429:
                raise TimeoutError("Rolling Window Quota [429] reached.")
            else:
                raise ConnectionError(f"Reason: {reason}, Status: {status_code}.")

        return dataset

    def _query_handler(self, date: str, channel_id: str) -> list:
        endpoint = self._config.get("endpoint", None)
        if not endpoint:
            raise Exception(
                "You need to specify endpoint in the configs i.e measure/api/v1/content/metrics or publish/items"
            )
        elif "content" in endpoint:
            query = self._content_by_channel_id
        elif "publish" in endpoint:
            query = self._published_posts_by_channel_id

        return query(date, channel_id)

    def run_query(self) -> Generator[dict, None, None]:
        """
        Get metrics by channel Id context returns a request session with the ability
        to page with offsets.
        Content (or Post level) contains all metrics about your specific piece of
        content (posts). Here you will find impressions, reach, likes,
        shares and other metrics that show how well your specific post has performed.
        https://falconio.docs.apiary.io/reference/content-api/get-copied-content.
        """
        channel_ids = self._get_channel_ids()
        # channel_ids = ["114215121990330", "58283981268"]
        print(f"Attempting to gather metrics from {len(channel_ids)} channel ids.")
        for date in date_range(
            start_date=date_handler(self._config.get("since", None), "%Y-%m-%d"),
            end_date=date_handler(self._config.get("until", None), "%Y-%m-%d"),
        ):
            payload: list = []
            for idx, channel_id in enumerate(channel_ids):
                data = self._query_handler(channel_id=channel_id, date=date)
                if data and len(data) > 0:
                    payload.extend(data)

            if len(payload) > 0:
                yield {
                    "endpoint_name": self._config["endpoint_name"],
                    "networks": self._config["networks"],
                    "date": date.replace("-", ""),
                    "data": payload,
                }
            else:
                print(
                    f"No data for endpoint {self._config['endpoint_name']} for date : {date}"
                )
