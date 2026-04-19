# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.
"""This module contains the handler for the food API."""

import sys
from socket import timeout
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable=C0413, E1120, C0301

import requests
from keys import OFF_API_USER

# For final use, we should use the production API.
# Production: https://world.openfoodfacts.org
# For testing, we can use the staging API.
# Staging: https://world.openfoodfacts.net
# read does not require API key, but write does.

# We should make small pauses between requests to avoid hitting the rate limit of the API.


# get product name from response
TEST_BARCODE = "737628064502"


def get_product_name_by_barcode(barcode=TEST_BARCODE):
    """This function fetches the product name from the OpenFoodFacts API using the given barcode."""
    url = f"https://world.openfoodfacts.net/api/v0/product/{barcode}.json"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(data["product"]["product_name"])

    else:
        print(f"Fehler: {response.status_code}")


# search for a product by barcode
TEST_BARCODE = "737628064502"


def fetch_product_name_by_barcode(barcode=TEST_BARCODE):
    """Fetches the product name from the OpenFoodFacts API using the given barcode."""
    url = f"https://world.openfoodfacts.net/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(data["product"]["product_name"])
        else:
            print(f"Fehler: {response.status_code}")
    except timeout:
        print("Error: Request timed out")
    except Exception as e:
        print(f"An error occurred: {e}")


# search for a product by name
PRODUCT_NAME = "Apfel"


def get_product_by_name(product_name=PRODUCT_NAME):
    """Fetches the product name from the OpenFoodFacts API using the given product name."""
    url = f"https://world.openfoodfacts.net/cgi/search.pl?search_terms={product_name}&search_simple=1&action=process&json=1"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for product in data["products"]:
                print(product["product_name"])
        else:
            print(f"Fehler: {response.status_code}")
    except timeout:
        print("Error: Request timed out")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":

    async def main():
        """This is the main function."""
        get_product_name_by_barcode()
        await asyncio.sleep(1)
        fetch_product_name_by_barcode()
        await asyncio.sleep(1)
        get_product_by_name()
        sys.exit(0)

    asyncio.run(main())
