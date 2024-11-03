from flask import Flask, render_template, url_for, redirect
from flask import request
import os

# Create flask application to manage routes
app = Flask(__name__)


@app.route('/')
def landing_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)
