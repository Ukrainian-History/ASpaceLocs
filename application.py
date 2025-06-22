import secrets

from flask import Flask, render_template, session, request, redirect, url_for

import aspace_api

app = Flask(__name__)
app.secret_key = secrets.token_hex()

@app.route('/')
def hello_world():
    return render_template('index.html',
                           message='Welcome to the ArchivesSpace location browser tool.',
                           second_message='Scan a location QR code to proceed.')

@app.route("/locations/<int:location>")
def locations(location):
    try:
        location_name = aspace_api.get_location(location)
    except aspace_api.NoLocationError:
        # TODO clean up after ourselves
        return render_template("index.html", message=f"Location {location} does not exist!")

    action = session.pop("action", None)
    if action == "move":
        container_id = session['container_id']
        repo = session['container_repo']
        from_location = session['last_location']
        from_name = session['last_location_name']
        to_name = location_name

        return render_template('execute-move.html',
                               container=session['container_name'],
                               from_name=from_name,
                               to_name=to_name)

    session["last_location"] = location
    session["last_location_name"] = location_name

    containers = aspace_api.get_containers_at_location(location)
    if containers:
        for container in containers:
            collections = [f'{cname} ({cid})' for cname, cid in zip(
                container['collections'],
                container['collection_identifiers'])]
            container['colls_with_ids'] = collections

        return render_template("container-list.html",
                               message=location_name,
                               containers=containers, location=location)
    else:
        return render_template("index.html", message=f"Location {location_name} has no containers.")


@app.route("/move/repositories/<int:repo>/top_containers/<int:container>", methods=['GET', 'POST'])
def move_container(repo, container):
    if request.method == 'POST':
        session.pop("action")
        session.pop("container_repo")
        session.pop("container_id")
        return redirect(url_for('locations', location=session['last_location']))
    else:
        container_info = aspace_api.get_specific_container(repo, container)

        session["action"] = "move"
        session["container_repo"] = repo
        session["container_id"] = container
        session["container_name"] = container_info['long_display_string']

        return render_template("move-container.html",
                               container=container_info['long_display_string'],
                               from_name=session['last_location_name'])


if __name__ == '__main__':
    app.run(debug=True)
