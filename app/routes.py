from flask import current_app as app, render_template
from .scraper import scrape_ochaopt

@app.route('/')
def home():
    ochaopt_data = scrape_ochaopt()
    return render_template('base.html',ochadata=ochaopt_data)

