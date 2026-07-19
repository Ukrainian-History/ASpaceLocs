# aspacelocs

A mobile-friendly Flask web application for managing storage locations and top containers in [ArchivesSpace](https://archivesspace.org/). Designed for use in a stacks setting, staff scan QR codes posted at each physical location to view and move containers between locations.


## Features

- **Scan-to-view**: Each physical location (shelf, bay, etc.) has a QR code. Scanning it shows all top containers currently assigned to that location in ArchivesSpace, including container profile and associated collections.
- **Move containers**: Select a container at one location, scan the QR code at the destination, and confirm to update the container's location in ArchivesSpace.
- **QR code label generation**: A standalone script (`genlabels.py`) generates printable QR code PNG labels for all defined locations.

## How it works

1. Staff scans a QR code at a physical location with a phone or tablet.
2. The app queries the ArchivesSpace API for all top containers across all repositories at that location.
3. Containers are displayed with details (name, repository, profile, associated collections).
4. To move a container, staff taps "Move" on a container card, then scans the QR code at the destination location and confirms the move.

## Project structure

```
application.py           Flask app and routes
aspace_api_asnake.py     ArchivesSpace API client (ArchivesSnake)
aspace_api.py            ArchivesSpace API client (raw requests, unused)
genlabels.py             Standalone QR code label generator
templates/
  index.html             Base template (Bootstrap 5)
  container-list.html    Container card grid
  move-container.html    "Scan destination" prompt
  execute-move.html      Move confirmation screen
qrcodes/                 Pre-generated QR code PNGs
```

## Configuration

The app connects to ArchivesSpace via environment variables:

| Variable | Default | Description |
|---|---|---|
| `ASPACE_BASEURL` | `https://sandbox.archivesspace.org/staff/api/` | ArchivesSpace API URL |
| `ASPACE_USER` | `admin` | ArchivesSpace username |
| `ASPACE_PASSWORD` | `admin` | ArchivesSpace password |

## Running locally

```bash
uv run application.py
```

The app starts on `http://localhost:5000` in debug mode.

## Running with Docker

```bash
docker build -t aspacelocs .
docker run -d -p 8000:8000 aspacelocs
```

The production server (gunicorn) listens on port 8000.

## Generating QR code labels

```bash
python genlabels.py
```

This fetches all location IDs from ArchivesSpace and saves QR code PNGs to `qrcodes/`. Each QR code encodes a URL like `https://locs.ukrhec.org/locations/{id}`.

## Notes

- The ArchivesSpace Solr indexer may lag behind API changes, so moved containers may not appear at their new location immediately.
- The Flask secret key is regenerated on each restart, which invalidates all active sessions.
