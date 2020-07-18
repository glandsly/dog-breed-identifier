# Example adapted from http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
# @NOTE: The code below is for educational purposes only.
# Consider using the more secure version at the link above for production apps
# Load libraries
from flask import *
import os
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model

# instantiate flask 
app = flask.Flask(__name__)

# we need to redefine our metric function in order 
# to use it when loading the model 
def auc(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    keras.backend.get_session().run(tf.local_variables_initializer())
    return auc

# load the model, and pass in the custom metric function
global graph
graph = tf.get_default_graph()
model = load_model('2020-07-11_dog_breed_model.h5', custom_objects={'auc': auc})

# define a predict function as an endpoint 
@app.route("/predict", methods=["GET","POST"])
def predict():
    data = {"success": False}

    params = flask.request.json
    if (params == None):
        params = flask.request.args

    # if parameters are found, return a prediction
    if (params != None):
        x=pd.DataFrame.from_dict(params, orient='index').transpose()
        with graph.as_default():
            data["prediction"] = str(model.predict(x)[0][0])
            data["success"] = True

    # return a response in json format 
    return flask.jsonify(data)    

IMAGE_FOLDER = 'static/'
#PROCESSED_FOLDER = 'processed/'

app = Flask(__name__)  

app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
#app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

@app.route('/')  
def upload():
	return render_template("index.html")  
 
@app.route('/success', methods = ['POST'])
def success():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
		image_ext = cv2.imread(full_filename)
		img_path = full_filename
		#print(image_ext.shape)
		with graph.as_default():
			set_session(sess)
			txt = predict_image(img_path)
			#result = predict_image(img_path, model)
			#txt = result
		final_text = 'Results after Detecting Dog Breed in Input Image'
		return render_template("result.html", name = final_text, img = full_filename, out_1 = txt)
		

@app.route('/info', methods = ['POST'])  
def info():
	return render_template("info.html") 

# start the flask app, allow remote connections 
app.run(host='0.0.0.0')


if __name__ == "__main__":
    app.run(debug=True)
