from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

# Create instance of Flask app
app = Flask(__name__)

# Flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create route that renders index.html template
@app.route("/")
def index():
    # Find one record of data from the mongo mars database
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html, mars_data=mars_data")

# Create route that triggers the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = mongo.db.mars_data
    mars_data_scrape = scrape_mars.scrape()

    # Update mongo database using update and upsert=True
    mars_data.update({}, mars_data_scrape, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug = True)