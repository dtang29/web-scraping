# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#create instance of flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)

#conn = 'mongodb://localhost:27017'


@app.route('/')
def home():
    mars = mongo.db.marsdatas.find_one()
    print(mars)
    return render_template("index.html", mars=mars)    

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    #Run scraped functions
    #mars = scrape_mars.scrape()

    mars = mongo.db.marsdatas
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    print(mars)

    #Store results into a dictionary
    # mars_info = {
    #     "mars_title" : mars["news_title"],
    #     "mars_news" : mars["news_p"],
    #     "mars_featured_image" : mars["featured_image_url"],
    #     "mars_weather" : mars["mars_weather"],
    #     "mars_html_table" : mars["html_table"],
    #     "mars_hemisphere_images" : mars["hemisphere_image_urls"]
    # }
    # print(mars_info)
    # mongo.db.marsdata.insert_one(mars_info)

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

