import json
from os import environ

from asnake.client import ASnakeClient
from asnake.aspace import ASpace

# validate ASnake client

try:
    client = ASnakeClient(baseurl=environ.get('ASPACE_BASEURL'),
                          username=environ.get('ASPACE_USER'),
                          password=environ.get('ASPACE_PASSWORD'))
    client.authorize()
    aspace = ASpace()
except Exception as e:
    print(f"Exception type: {type(e).__name__}")
    print(f"Error message: {e}")


class NoLocationError(Exception):
    """Exception raised for invalid location.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_location(location):
    response = aspace.client.get(f'/locations/{location}')
    if response.status_code == 404:
        raise NoLocationError(f"Location {location} does not exist.")

    response_json = json.loads(response.text)
    return response_json["title"]



def process_container(container):
    return {
        "name": container["display_string"],
        "barcode": container.get("barcode_u_sstr"),
        "container_profile": container.get("container_profile_display_string_u_sstr"),
        "collections": container.get("collection_display_string_u_sstr"),
        "collection_identifiers": container.get("collection_identifier_stored_u_sstr"),
        "repository": container["repository"],
        "uri": container["uri"]
    }


def get_container_page(location, page_number):
    query = (
        f"/search?page={page_number}"
        "&filter_query[]=primary_type:top_container"
        f'&filter_query[]=location_uri_u_sstr:"/locations/{location}"'
    )

    response = aspace.client.get(query)
    # TODO make sure there's no error

    response_json = json.loads(response.text)

    containers = [process_container(c) for c in response_json["results"]]
    return int(response_json["this_page"]), int(response_json["last_page"]), containers


def get_containers_at_location(location):
    response = aspace.client.get(f'/locations/{location}')
    if response.status_code == 404:
        raise NoLocationError(f"Location {location} does not exist.")

    (this_page, last_page, containers) = get_container_page(location, 1)

    while this_page < last_page:
        (this_page, last_page, new_containers) = get_container_page(location, this_page+1)
        containers += new_containers

    return containers

if __name__ == '__main__':
    stuff = get_location(76)
    stuff = get_containers_at_location(76)
    print(stuff)
