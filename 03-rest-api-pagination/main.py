import json
import os

from connectors.rest_connector import RestConnector

connector = RestConnector(
    base_url="https://jsonplaceholder.typicode.com/posts",
    page_size=10
)

data = connector.fetch_data()

os.makedirs("output", exist_ok=True)

with open("output/posts.json", "w") as file:
    json.dump(data, file, indent=4)

print()

print(f"Total Records = {len(data)}")

print("Saved Successfully")
print("code changed")
