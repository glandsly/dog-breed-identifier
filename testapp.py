from flask import *
import os
import pandas as pd
from shutil import copyfile
from keras.models import load_model
from keras.preprocessing import image
import matplotlib.pyplot as plt
import numpy as np


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
            df = pd.read_csv('labels.csv')
            selected_breed_list = list(df.groupby('breed').count().sort_values(by='id', ascending=False).head(120).index)
            model = load_model('2020-07-11_dog_breed_model.h5')
            img = image.load_img(filepath, target_size=(299, 299))
            img_tensor = image.img_to_array(img)                    # (height, width, channels)
            img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
            img_tensor /= 255.                                      # imshow expects values in the range [0, 1]
            
            pred = model.predict(img_tensor)
            sorted_breeds_list = sorted(selected_breed_list)
            prediction = sorted_breeds_list[np.argmax(pred)]
 
            # model = load_model('2020-07-15_dog_breed_model.h5')
            
            return render_template("result.html", filename = filename, prediction = prediction)
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <p><input type=file name=file>
    #      <input type=submit value=Upload>
    # </form>
    # '''



if __name__ == "__main__":
    app.run(debug=True)