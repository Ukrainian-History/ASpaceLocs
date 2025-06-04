import secrets

from flask import Flask, render_template, sessions

import aspace_api

# see https://flask.palletsprojects.com/en/stable/quickstart/#sessions for sessions info

app = Flask(__name__)
app.secret_key = secrets.token_hex()

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route("/locations/<int:location>")
def locations(location):
    try:
        location_name = aspace_api.get_location(location)
    except aspace_api.NoLocationError:
        return render_template("index.html", message=f"Location {location} does not exist!")

    containers = aspace_api.get_containers_at_location(location)
    if containers:
        return render_template("container-list.html",
                               message=f"Contents of {location_name}:",
                               containers=containers, location=location)
    else:
        return render_template("index.html", message=f"Location {location_name} has no containers.")


@app.route("/move/repositories/<int:repo>/top_containers/<int:container>")
def move_container(repo, container):
    return render_template("index.html", message=f"Moving container {container} in repository {repo}")


if __name__ == '__main__':
    app.run(debug=True)
