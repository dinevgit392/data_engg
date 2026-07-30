"""
File Name : rest_connector.py

Purpose:
    Reusable REST API connector.

Features:
    1. Authentication
    2. API Calls
    3. Pagination
    4. Retry Logic
    5. Logging
    6. Error Handling

Author : Dinesh
"""

import requests
import logging
import time


# ----------------------------------------------------
# Configure Logging
# ----------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ----------------------------------------------------
# REST Connector Class
# ----------------------------------------------------

class RestConnector:

    def __init__(self, base_url, token=None):

        """
        Constructor

        Parameters
        ----------
        base_url : API URL

        token : Authentication Token
        """

        self.base_url = base_url
        self.token = token

        logger.info("REST Connector Initialized")


    # ------------------------------------------------
    # Authentication Header
    # ------------------------------------------------

    def get_headers(self):

        """
        Creates authentication header.
        """

        headers = {
            "Content-Type": "application/json"
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers


    # ------------------------------------------------
    # GET Request
    # ------------------------------------------------

    def get_data(
            self,
            endpoint="",
            params=None,
            retries=3,
            delay=5
    ):

        """
        Calls REST API

        Parameters

        endpoint

        params

        retries

        delay
        """

        url = f"{self.base_url}{endpoint}"

        headers = self.get_headers()

        attempt = 1

        while attempt <= retries:

            try:

                logger.info(f"Calling API : {url}")

                response = requests.get(
                    url=url,
                    headers=headers,
                    params=params,
                    timeout=30
                )

                response.raise_for_status()

                logger.info("API Call Successful")

                return response.json()

            except requests.exceptions.HTTPError as e:

                logger.error(f"HTTP Error : {e}")

            except requests.exceptions.ConnectionError as e:

                logger.error(f"Connection Error : {e}")

            except requests.exceptions.Timeout as e:

                logger.error(f"Timeout Error : {e}")

            except Exception as e:

                logger.error(f"Unknown Error : {e}")

            logger.info(
                f"Retry {attempt}/{retries}"
            )

            attempt += 1

            time.sleep(delay)

        raise Exception("API failed after retries")


    # ------------------------------------------------
    # Pagination
    # ------------------------------------------------

    def get_all_data(
            self,
            endpoint="",
            limit=10
    ):

        """
        Downloads all pages.

        Example API

        page1

        page2

        page3
        """

        all_records = []

        skip = 0

        while True:

            params = {

                "limit": limit,

                "skip": skip

            }

            data = self.get_data(
                endpoint=endpoint,
                params=params
            )

            rows = data.get("products", [])

            if len(rows) == 0:
                break

            all_records.extend(rows)

            logger.info(
                f"Downloaded {len(rows)} records"
            )

            skip += limit

        logger.info(
            f"Total Records : {len(all_records)}"
        )

        return all_records


# ----------------------------------------------------
# Testing
# ----------------------------------------------------

if __name__ == "__main__":

    connector = RestConnector(

        base_url="https://dummyjson.com"

    )

    products = connector.get_all_data(

        endpoint="/products",

        limit=20

    )

    print(products[:3])
