# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

# create route that renders index.html template
from google.cloud import bigquery
client = bigquery.Client()


sql_command = f'SELECT {vistorId},{transactions}, FROM `bigquery-public-data.google_analytics_sample.ga_sessions_{input}`'


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        filtered_query = client.query("""{sql_command}""")
        results = filtered_query.results()
        return redirect("/", code=302)
    return render_template("form.html")


@app.route("/api/filtered_data")
def filtered_Data():
    filtered_query = client.query("""{sql_command}""")
    results = filtered_query.results()
    visitorId = [result[0] for result in results]
    transactions = [result[1] for result in results]

    filtered_data = [{
        "visitorId": visitorId,
        "transactions": transactions,
    }]

    return jsonify(filtered_data)


if __name__ == "__main__":
    app.run()