import secrets

from flask import Flask, render_template, session

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

    location_name = 'fake location name'

    session["last_location"] = location
    containers = [{'name': 'Box 11: Series 3', 'barcode': None, 'container_profile': ['Legal Document Box [15.25d, 10.25h, 5w inches] extent measured by width'], 'collections': ['Krispy Kreme Corporation Records'], 'collection_identifiers': ['NMAH.AC.0594'], 'repository': '/repositories/2', 'uri': '/repositories/2/top_containers/274'}, {'name': 'Box 12: Series 3', 'barcode': None, 'container_profile': ['Legal Document Box [15.25d, 10.25h, 5w inches] extent measured by width'], 'collections': ['Krispy Kreme Corporation Records'], 'collection_identifiers': ['NMAH.AC.0594'], 'repository': '/repositories/2', 'uri': '/repositories/2/top_containers/275'}, {'name': 'Box 7: Series 2; Series 3', 'barcode': None, 'container_profile': ['Legal Document Box [15.25d, 10.25h, 5w inches] extent measured by width'], 'collections': ['Krispy Kreme Corporation Records'], 'collection_identifiers': ['NMAH.AC.0594'], 'repository': '/repositories/2', 'uri': '/repositories/2/top_containers/267'}, {'name': 'Box 8: Series 3', 'barcode': None, 'container_profile': ['Legal Document Box [15.25d, 10.25h, 5w inches] extent measured by width'], 'collections': ['Krispy Kreme Corporation Records'], 'collection_identifiers': ['NMAH.AC.0594'], 'repository': '/repositories/2', 'uri': '/repositories/2/top_containers/270'}, {'name': 'Box 9: Series 3', 'barcode': None, 'container_profile': ['Legal Document Box [15.25d, 10.25h, 5w inches] extent measured by width'], 'collections': ['Krispy Kreme Corporation Records'], 'collection_identifiers': ['NMAH.AC.0594'], 'repository': '/repositories/2', 'uri': '/repositories/2/top_containers/272'}, {'name': 'Box 10: Series 3', 'barcode': None, 'container_profile': ['Legal Document Box [15.25d, 10.25h, 5w inches] extent measured by width'], 'collections': ['Krispy Kreme Corporation Records'], 'collection_identifiers': ['NMAH.AC.0594'], 'repository': '/repositories/2', 'uri': '/repositories/2/top_containers/273'}]
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
