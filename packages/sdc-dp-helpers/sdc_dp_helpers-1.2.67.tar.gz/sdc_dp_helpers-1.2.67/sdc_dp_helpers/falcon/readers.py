"""
    CUSTOM FALCON READER CLASSES
"""
import os
from typing import Generator, Callable, Set
from datetime import datetime, timedelta

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
        self.channel_id_index: int = None

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
    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=900)
    def _content_by_channel_id(self, date: str, channel_id: str) -> list:
        """Gets the content metrics by channel id
        SEE: https://falconio.docs.apiary.io/#reference/channel-api/get-facebook-and-instagram-page-insights-metrics/get-content-metrics-by-channel-ids
        :param: channel_id - integer
        :param: date - string pushed as '2022-07-20'
        :returns: list of dictionaries
        """
        dataset: list = []
        endpoint_url: str = (
            f"measure/api/v1/content/metrics?apikey={self._creds['api_key']}"
        )
        offset: int = 0
        limit = self._config.get("limit", 200)
        while True:
            print(
                f"INFO: channel id index: {self.channel_id_index}, channel id: {channel_id}, date: {date}, offset: {offset}."
            )
            req = requests.Request(
                method="POST",
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
                result_count = len(results)

                if result_count == 0:  # or result_count < limit:
                    break  # we will exit the loop because no data is got back

                if result_count < limit:
                    offset += result_count
                else:
                    offset += limit

                dataset.extend(results)

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
    @retry_handler(exceptions=ConnectionError, total_tries=5, initial_wait=900)
    def _published_posts_by_channel_id(self, date: str, channel_id: str) -> list:
        """Gets the published posts by channel id
        SEE: https://falconio.docs.apiary.io/#reference/content-api/get-content-metrics-by-channel-ids
        :param: channel_id - integer
        :param: date - string pushed as '2022-07-20' but converted to isoformat '2022-07-20T00:00:00'
        :returns: list of dictionaries
        """

        dataset: list = []
        endpoint_url: str = f"publish/items?apikey={self._creds['api_key']}"
        limit = self._config.get("limit", 200)
        start_date = datetime.strptime(date, "%Y-%m-%d").isoformat()
        end_date = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).isoformat()
        while endpoint_url:
            print(
                f"INFO: channel id index: {self.channel_id_index}, channel id: {channel_id},  date: {date}, offset: {len(dataset)}."
            )
            req = requests.Request(
                method="GET",
                url=f"{self.base_url}{endpoint_url}",
                headers={"Content-Type": "application/json"},
                params={
                    "channels": [channel_id],
                    "since": start_date,
                    "until": end_date,
                    "networks": self._config["networks"],
                    "statuses": self._config.get("statuses", "published"),
                    "limit": limit,
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
        endpoint_name = self._config.get("endpoint_name", None)
        if not endpoint_name:
            raise Exception(
                "You need to specify endpoint in the configs i.e content_metrics or published_posts"
            )
        elif endpoint_name == "content_metrics":
            query = self._content_by_channel_id
        elif endpoint_name == "published_posts":
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
                self.channel_id_index = idx
                data = self._query_handler(channel_id=channel_id, date=date)
                if data and len(data) > 0:
                    payload.extend(data)

            if len(payload) > 0:
                yield {
                    "networks": self._config["networks"],
                    "date": date.replace("-", ""),
                    "data": payload,
                }
            else:
                print(
                    f"No data for endpoint {self._config['endpoint_name']} for date : {date}"
                )
