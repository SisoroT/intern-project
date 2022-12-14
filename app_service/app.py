from flask import Flask
from flask import render_template, request, flash, redirect, url_for

import requests

app = Flask(__name__)
app.secret_key = b"U2hI]w1dKiD8NKGgxTUMaw5Deftwr3K7"
function_url = "https://gavanade-function-windows.azurewebsites.net/api"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/statelist")
def statelist():
    response = requests.get(
        f"{function_url}/price_table",
    )
    flash(response.text)
    return render_template("statelist.html")


@app.route("/legal")
def legal():
    return render_template("legal.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/privacypolicy")
def privacypolicy():
    return render_template("privacypolicy.html")


@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/zip")
def zip():
    return render_template("zip.html")


@app.route("/search/zipcode", methods=("POST",))
def search_zipcode():
    zipcode = request.form["zipcode"]
    try:
        zipcode = int(zipcode)
        if 501 <= zipcode <= 99950:
            response = requests.get(
                f"{function_url}/gasprices?zipcode={zipcode}",
            )
            flash(response.text)
        else:
            zipcode = -2
            flash("Please enter a valid US zipcode.")
    except BaseException:
        zipcode = -2

    return redirect(url_for("zip"))


@app.route("/search/coordinates", methods=("GET", "POST"))
def search_coordinates():
    lat = request.args.get("latitude", type=float)
    lon = request.args.get("longitude", type=float)
    lon = (lon + 180) % 360 - 180

    try:
        response = requests.get(
            f"{function_url}/gasprices?latitude={lat}&longitude={lon}",
        )
        flash(response.text)
    except BaseException:
        lat = -2
        lon = -2

    return redirect(url_for("map"))


@app.route("/concerns/update", methods=("GET", "POST"))
def concerns_update():
    email = request.form["email"]
    msg = request.form["concerns"]

    error = ""
    if email == "":
        error += "Must include an email"
    if msg == "":
        error += "; " if error != "" else ""
        error += "Must include a message"

    if error != "":
        flash(error)
        return redirect(url_for("contact"))

    requests.get(
        f"{function_url}/database?table=concerns&write=write&email={email}&msg={msg}",
    )

    return redirect(url_for("contact"))


@app.route("/contact/update", methods=("GET", "POST"))
def contact_info_update():
    first_name = request.form["fname"]
    last_name = request.form["lname"]
    email = request.form["email"]

    error = ""
    if first_name == "":
        error += "Must include first name"
    if last_name == "":
        error += "; " if error != "" else ""
        error += "Must include last name"
    if email == "":
        error += "; " if error != "" else ""
        error += "Must include an email"

    if error != "":
        flash(error)
        return redirect(url_for("contact"))

    requests.get(
        f"{function_url}/database?table=contactInformation&write=write&firstName={first_name}&lastName={last_name}&email={email}",
    )
    print("Processed Contact Info.")

    return redirect(url_for("contact"))


if __name__ == "__main__":
    app.run()
