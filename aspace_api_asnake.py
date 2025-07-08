import json
from os import environ
from datetime import datetime

from asnake.client import ASnakeClient
from asnake.aspace import ASpace

baseURL = environ.get('ASPACE_BASEURL') or "https://sandbox.archivesspace.org/staff/api/"
user = environ.get('ASPACE_USER') or "admin"
password = environ.get('ASPACE_PASSWORD') or "admin"

# validate ASnake client

try:
    client = ASnakeClient(baseurl=baseURL, username=user, password=password)
    client.authorize()
    aspace = ASpace(baseurl=baseURL, username=user, password=password)
except Exception as e:
    print(f"Exception type: {type(e).__name__}")
    print(f"Error message: {e}")
    exit(1)

resp = aspace.client.get(f'/repositories')
response_json = json.loads(resp.text)
repositories = {repo['uri']: {'name': repo['name'], 'code': repo['repo_code']} for repo in response_json}

class NoLocationError(Exception):
    """Exception raised for invalid location.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_location(location):
    resp = aspace.client.get(f'/locations/{location}')
    if resp.status_code == 404:
        raise NoLocationError(f"Location {location} does not exist.")

    resp_json = json.loads(resp.text)
    return resp_json["title"]


def get_all_location_ids():
    resp = aspace.client.get(f'/locations?all_ids=true')
    resp_json = json.loads(resp.text)
    return resp_json

def process_container(container):
    return {
        "name": container["display_string"],
        "barcode": container.get("barcode_u_sstr"),
        "container_profile": container.get("container_profile_display_string_u_sstr"),
        "collections": container.get("collection_display_string_u_sstr"),
        "collection_identifiers": container.get("collection_identifier_stored_u_sstr"),
        "repository": container["repository"],
        "repo_code": repositories[container["repository"]]["code"],
        "uri": container["uri"]
    }


def get_container_page(location, page_number):
    query = (
        f"/search?page={page_number}"
        "&filter_query[]=primary_type:top_container"
        f'&filter_query[]=location_uri_u_sstr:"/locations/{location}"'
    )

    resp = aspace.client.get(query)
    # TODO make sure there's no error

    resp_json = json.loads(resp.text)

    containers = [process_container(c) for c in resp_json["results"]]
    return int(resp_json["this_page"]), int(resp_json["last_page"]), containers


def get_specific_container(repo, container_id):
    resp = aspace.client.get(f'/repositories/{repo}/top_containers/{container_id}')
    # TODO make sure there's no error
    return json.loads(resp.text)


def get_containers_at_location(location):
    response = aspace.client.get(f'/locations/{location}')
    if response.status_code == 404:
        raise NoLocationError(f"Location {location} does not exist.")

    (this_page, last_page, containers) = get_container_page(location, 1)

    while this_page < last_page:
        (this_page, last_page, new_containers) = get_container_page(location, this_page+1)
        containers += new_containers

    return containers


def move_container(repo, container, to_location):
    container_info = get_specific_container(repo, container)
    if len(container_info['container_locations']) != 1:
        return False, "Containers that does not have exactly one location are not currently supported."

    container_info['container_locations'][0]['start_date'] = datetime.today().strftime('%Y-%m-%d')
    container_info['container_locations'][0]['ref'] = f'/locations/{to_location}'

    resp = aspace.client.post(f'/repositories/{repo}/top_containers/{container}', json=container_info)
    if resp.status_code != 200:
        return False, resp.text

    return True, "Successfully moved container. Result may not be immediately visible as the indexer needs to catch up."


if __name__ == '__main__':
    # stuff = get_location(1)
    # stuff = get_containers_at_location(1)
    # stuff = get_specific_container(2, 258)
    # stuff = move_container(2, 258, 1)
    stuff = get_all_location_ids()
    print(stuff)
