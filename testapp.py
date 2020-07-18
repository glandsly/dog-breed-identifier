from flask import *
import os
import pandas as pd
# import tensorflow as tf
# import keras
# from keras.models import load_model
# instantiate flask 
app = Flask(__name__)
@app.route("/")
def home():
    # Return template and data
    return render_template("index.html")
@app.route("/result")
def result():
    # Return template and data
    return render_template("result.html")

@app.route("/graphs")
def graphs():
# Return template and data
    return render_template("graphs.html")

@app.route("/csv")
def csv():
# Return template and data
    return render_template("csv.html")

if __name__ == "__main__":
    app.run(debug=True)