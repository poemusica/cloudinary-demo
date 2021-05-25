from flask import Flask, render_template, request, redirect, url_for
import cloudinary.uploader
import os

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_KEY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "YOUR_CLOUD_NAME_GOES_HERE"

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/show-image')
def show_image():
    img_url = request.args.get('imgURL')
    return render_template('results.html', img_src=img_url)

@app.route('/media-upload-form')
def show_upload_form():
    return render_template('form.html')

@app.route('/post-form-data', methods=['POST'])
def post_form_data():

    my_file = request.files['my-file']

    result = cloudinary.uploader.upload(my_file, 
                                        api_key=CLOUDINARY_KEY, 
                                        api_secret=CLOUDINARY_KEY_SECRET, 
                                        cloud_name=CLOUD_NAME)

    img_url = result['secure_url']
    print('*' * 20)
    print("SAVE THIS url to your database!!")
    # Save this url to your database, so that you can show the image to the user later.
    print(img_url)
    print('*' * 20)
    return redirect(url_for('show_image', imgURL=img_url))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')