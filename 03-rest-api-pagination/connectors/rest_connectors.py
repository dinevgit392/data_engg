import requests
import time


class RestConnector:

    def __init__(self, base_url, page_size=10, max_retry=3):
        self.base_url = base_url
        self.page_size = page_size
        self.max_retry = max_retry

    def fetch_data(self):

        page = 1

        all_records = []

        while True:

            params = {
                "_page": page,
                "_limit": self.page_size
            }

            retry = 0

            while retry < self.max_retry:

                try:

                    print(f"Fetching Page {page}")

                    response = requests.get(
                        self.base_url,
                        params=params,
                        timeout=10
                    )

                    response.raise_for_status()

                    records = response.json()

                    if len(records) == 0:
                        print("No more data.")
                        return all_records

                    all_records.extend(records)

                    print(f"Fetched {len(records)} records")

                    page += 1

                    break

                except requests.exceptions.RequestException as e:

                    retry += 1

                    print(f"Retry {retry}")

                    time.sleep(2)

                    if retry == self.max_retry:
                        raise Exception(e)
