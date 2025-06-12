import secrets

from flask import Flask, render_template, session

import aspace_api_alt

app = Flask(__name__)
app.secret_key = secrets.token_hex()

@app.route('/')
def hello_world():
    return render_template('index.html',
                           message='Welcome to the ArchivesSpace location browser tool.',
                           second_message='Scan a location QR code to proceed.')

@app.route("/locations/<int:location>")
def locations(location):
    action = session.pop("action", None)
    if action == "move":
        container_id = session['container_id']
        repo = session['container_repo']
        from_location = session['last_location']

        return render_template('move-container.html',
                               message=(f"Move container {container_id} in repository {repo} "
                                        f"from location {from_location} to {location}")
                               )

    try:
        location_name = aspace_api_alt.get_location(location)
    except aspace_api_alt.NoLocationError:
        return render_template("index.html", message=f"Location {location} does not exist!")

    session["last_location"] = location
    containers = aspace_api_alt.get_containers_at_location(location)
    if containers:
        return render_template("container-list.html",
                               message=f"Contents of {location_name}:",
                               containers=containers, location=location)
    else:
        return render_template("index.html", message=f"Location {location_name} has no containers.")


@app.route("/move/repositories/<int:repo>/top_containers/<int:container>")
def move_container(repo, container):
    session["action"] = "move"
    session["container_repo"] = repo
    session["container_id"] = container

    return render_template("index.html",
                           message=f"Moving container {container} in repository {repo}",
                           second_message="Scan the QR code of the destination location.")
    #TODO provide a means of cancelling?


if __name__ == '__main__':
    app.run(debug=True)
