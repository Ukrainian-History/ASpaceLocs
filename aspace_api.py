import json

from asnake.client import ASnakeClient
from asnake.aspace import ASpace


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
    main()
