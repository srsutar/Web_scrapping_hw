from flask import Flask, render_template
from flask_pymongo import PyMongo
from scrapper import scrapper
app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    # mars = scrapper()
    return render_template("index.html", mars=mars)
@app.route("/scrape")
def scrape():
    print('start scrape')
    mars = mongo.db.mars
    mars_data = scrapper()
    mars.replace_one({}, mars_data, upsert=True)
    return render_template("index.html", mars=mars_data)
if __name__ == "__main__":
    app.run()