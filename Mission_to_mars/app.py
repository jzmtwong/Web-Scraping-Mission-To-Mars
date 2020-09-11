# Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# instance of flask app
app = Flask(__name__)

# flask/ pymongo connection
app.config["MONGO_URI"] = 'mongodb://localhost:27017/MARS'
mongo = PyMongo(app)


# Create route for index.html template
@app.route("/")
def home():
    # present data
    mars_information = mongo.db.mars_data.find_one()

    # return index template and data
    return render_template("index.html", mars_data=mars_information)


# Route that will trigger scrape function
@app.route("/scrape")
def scrape():
    #run scrape function
    mars_data = mongo.db.mars_data
    mars_information = scrape_mars.scrape_news()
    mars_information = scrape_mars.scrape_image()
    mars_information = scrape_mars.scrape_facts()
    mars_information = scrape_mars.scrape_hem()
    mars_data.update({}, mars_information, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)