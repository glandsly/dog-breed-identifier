# Example adapted from http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
# @NOTE: The code below is for educational purposes only.
# Consider using the more secure version at the link above for production apps
import os
from flask import Flask, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request)

        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # Save the file to the uploads folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Image Saved!"

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
