"""This module contains the handler for the food API."""

from socket import timeout
import sys
import requests

# For final use, we should use the production API.
# Production: https://world.openfoodfacts.org
# For testing, we can use the staging API.
# Staging: https://world.openfoodfacts.net

# vaeterchen_host@proton.me as contact for API key
# read does not require API key, but write does.

EXAMPLE_URL = "https://world.openfoodfacts.net/api/v0/product/737628064502.json"
response = requests.api.get(EXAMPLE_URL, timeout=10)

# get product name from response
if response.status_code == 200:
    data = response.json()
    print(data["product"]["product_name"])

else:
    print(f"Fehler: {response.status_code}")

# search for a product by barcode
BARCODE = "737628064502"
SEARCH_URL = f"https://world.openfoodfacts.net/api/v0/product/{BARCODE}.json"
try:
    response = requests.api.get(SEARCH_URL, timeout=10)
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
PRODUCT_NAME = "Coca-Cola"
SEARCH_URL = f"https://world.openfoodfacts.net/cgi/search.pl?search_terms={PRODUCT_NAME}&search_simple=1&action=process&json=1"
try:
    response = requests.api.get(SEARCH_URL, timeout=10)
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
