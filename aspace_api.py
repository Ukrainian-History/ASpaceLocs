import json

from asnake.client import ASnakeClient
from asnake.aspace import ASpace

class NoLocationError(Exception):
    """Exception raised for invalid location.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def process_container(container):
    return {
        "location_name": container["location_display_string_u_sstr"],
        "name": container["display_string"],
        "barcode": container.get("barcode_u_sstr"),
        "container_profile": container.get("container_profile_display_string_u_sstr"),
        "collections": container.get("collection_display_string_u_sstr"),
        "collection_identifiers": container.get("collection_identifier_stored_u_sstr"),
        "repository": container["repository"]
    }


def get_container_page(location, page_number, aspace):
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
    # validate ASnake client
    client = ASnakeClient()
    client.authorize()
    aspace = ASpace()

    response = aspace.client.get(f'/locations/{location}')
    if response.status_code == 404:
        raise NoLocationError(f"Location {location} does not exist.")

    (this_page, last_page, containers) = get_container_page(location, 1, aspace)

    while this_page < last_page:
        (this_page, last_page, new_containers) = get_container_page(location, this_page+1, aspace)
        containers += new_containers

    return containers

def main():
    # validate ASnake client
    client = ASnakeClient()
    client.authorize()
    aspace = ASpace()

    query = (
        "/search?page=1"
        "&filter_query[]=primary_type:top_container"
        '&filter_query[]=location_uri_u_sstr:"/locations/248"'
    )

    dum = aspace.client.get(query)
    resource_json = json.loads(dum.text)

    # print(json.dumps(resource_json, indent=2))

    with open('out.json', 'w', encoding='utf-8') as f:
        json.dump(resource_json, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    stuff = get_containers_at_location(76)
    print(stuff)
