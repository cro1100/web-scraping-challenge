import scrape_mars
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")
mongo.db.facts.drop()

@app.route("/")
def push_data():
    
    # send list to index.html using data from mongo
    mars_data_app = mongo.db.facts.find_one()
    print(f"mars_data_app :: {mars_data_app}")

    # Return data back to index for use
    return render_template("index.html", mars_data=mars_data_app)

@app.route("/pull_data")
def pull_data():

    #Run scrape function and get the 4 pieces of data
    mars_collections = scrape_mars.scrape()

    # Pass data to mongo db
    mongo.db.facts.update({}, mars_collections, upsert=True)

    # Redirect to route"/" to send the data back to tshe index
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)