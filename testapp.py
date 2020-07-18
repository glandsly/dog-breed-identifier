from flask import *
import os
import pandas as pd
from shutil import copyfile


from keras.preprocessing import image
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

app.config['UPLOAD_FOLDER'] = 'uploads'
def prepare_image(img):
    # Convert the image to a numpy array
    img = image.img_to_array(img)
    # Scale from 0 to 255
    img /= 255
    return img
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request)
        if request.files.get('file'):
            # read the file
            file = request.files['file']
            # read the filename
            filename = file.filename
            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Save the file to the uploads folder
            file.save(filepath)
            # Load the saved image using Keras and resize it to the
            # mnist format of 28x28 pixels
            image_size = (28, 28)
            im = image.load_img(filepath, target_size=image_size,
                                grayscale=True)
            # Convert the 2D image to an array of pixel values
            image_array = prepare_image(im)
            copyfile(filepath, f"static/{filename}")
            print(image_array)
            return render_template("result.html", filename = filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)