

# <img src="https://user-images.githubusercontent.com/6889489/161647661-5e3a1c62-b7b9-4f5c-88ee-4a1b74ec1921.png" width="100"> Cloudinary and Media Uploads Primer
Learn how to use the [Cloudinary API (Python SDK)](https://cloudinary.com/documentation/django_integration) with a [Flask](https://flask.palletsprojects.com/) app in order to save user-uploaded media. 


## Who is this guide for?
The guide, instructions, and demos are designed with new developers in mind, specifically students at the coding bootcamp <img src="https://user-images.githubusercontent.com/6889489/161647778-800ee782-70a1-40cc-883b-6bc598288849.png" width="15"> Hackbright Academy.


## Why include media uploads in a project?
Images make your web pages more exciting. Does your web app have user accounts? Why not let your users upload a profile photo!? Does your web app have log entries? Make entries more interesting by allowing users to attach a photo. 


## Why image-hosting?
We don’t want to save entire image files in our databases. Images are large! Our web servers (currently, our personal computers) would run out of storage if we saved all that data in our databases or on our servers. Instead, we can use a third-party service that will store the images for us on their servers. Then, we can simply save the image URLs as strings in our database. Strings take up way less storage space than entire image files. 

There are many image-hosting services to choose from, but [Cloudinary](https://cloudinary.com/) has a free tier and is easy to use.


## Discussion of Approaches
The demo code includes two approaches to handling user-uploaded media.

### Simple Media Upload
This approach uses the browser's default form action on submit.

The browser makes a request to the server (Flask backend), providing the data in the form. Then the server makes a request to the Cloudinary API, passing along the form data. After receiving the response from Cloudinary, the server sends a response to the browser (frontend) and the browser displays the response after reloading the page.

The tutorial below explains this approach in more detail.

### Asynchronous Media Upload
This approach uses the JavaScript [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) to process the form submission asynchronously. 

On the frontend (browser), JavaScript prevents the default form action and instead sends the form data to the server (Flask backend) using a [`fetch`](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#uploading_a_file) request. Just as before, the server makes a request to the Cloudinary API, passing along the form data. After receiving the response from Cloudinary, the server sends a response to the browser (frontend), but this time the browser uses JavaScript to display the response and the page does not reload.

While this approach is not covered in this primer, the demo code is available in this repository.

### Other Cloudinary Approaches
In both demos, the Flask server uses the [Cloudinary Python SDK](https://cloudinary.com/documentation/django_integration) and acts as an intermediary between the browser and the Cloudinary API. (This is a useful technique in cases where the browser is not allowed to make requests to an API directly due to [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) restrictions.)

[Cloudinary's REST API](https://cloudinary.com/documentation/upload_images#uploading_with_a_direct_call_to_the_rest_api) can be called directly via JavaScript, however it requires generating authentication signatures, which adds some complexity.

Alternatively, Cloudinary offers a [JavaScript SDK](https://cloudinary.com/documentation/javascript_image_and_video_upload), which allows the browser to make requests to the Cloudinary API directly (via JavaScript), but this approach requires the assistance of frontend tooling and frameworks.

Lastly, Cloudinary provides a premade [upload widget](https://cloudinary.com/documentation/upload_widget), which can be configured with JavaScript, to assist with media uploads.


## Walkthough Guide of the Simple Media Upload Approach

### Part 1: Make a FREE Cloudinary account

#### Step 1: Go to [cloudinary.com](https://cloudinary.com/) and create a free account. 
Since we're primarily using Cloudinary to save and display images, select **Programmable Media** from the Product dropdown menu.

#### Step 2: Create your Cloud Name.
During the signup process, you will also make your **Cloud Name**. Your **Cloud Name** will be part of the URL that Cloudinary creates for your image uploads.


### Part 2: Get Your API Credentials

#### Step 1: Locate your credentials.
On your Cloudinary Dashboard, locate your:
- **Cloud Name**
- **API Key**
- **API Secret**

You need these three pieces of information to make requests to the Cloudinary API.

⚠️ **WARNING: NEVER COMMIT your API Key or API Secret to git/Github.**

#### Step 2: Keep your credentials secret.
Add **secrets.sh** to your **.gitignore** file. 
Put your **API Key** and **API Secret** in your **secrets.sh** file in your project directory.

![.gitignore and secrets.sh screenshot](https://user-images.githubusercontent.com/6889489/161648490-94dd067b-06c4-4e15-aec1-c362f888f44b.png)

#### Step 3: Load your secrets
In the terminal, load your API credentials as shell environment variables by running the command:

`source secrets.sh`

(**Note**: Similar to the way you must activate your virtual environment whenever you start working on your project in a new terminal, you must also re-load your secrets by re-running the command above.)

### Part 3: Make a Form
Below is a snippet of an HTML page that contains a simple form for uploading an image.

![form screenshot](https://user-images.githubusercontent.com/6889489/161648731-1d0565d5-8b50-4ca9-bb30-31750b5cfc49.png)

To upload an image, your form must include:
- An `input` tag with the attribute `type=”file”` and a `name` attribute.
- The `action` attribute specifying a route that will handle the request from this form. Additionally, the method used should be `“post”` because we plan to create data on the backend when this form is submitted. 
- The `enctype` attribute specifying that the data will be encoded as `“multipart/form-data”`.


### Part 4: Install and Import

#### Step 1: Install the Cloudinary SDK for Python.
⚠️ **WARNING: Make sure you have activated your virtual environment!**

Cloudinary has a Python library that makes it easier to use the Cloudinary API.

In the terminal, run the command:

`pip3 install cloudinary`

#### Step 2: Update your project requirements
Now that you’ve installed `cloudinary`, you’ll want to make sure it’s included in your **requirements.txt** file. 

In the terminal, run the command:

`pip3 freeze > requirements.txt`

#### Step 3: Import libraries and access secrets
In your **server.py** file, 
- import the `os` module from the Python standard library.
- import `cloudinary.uploader` from the `cloudinary` library.
- use the `os` module to access your API credentials (shell environment variables).
- Replace `“YOUR-CLOUD-NAME-HERE”` with your actual **Cloud Name** as a string.

![server screenshot](https://user-images.githubusercontent.com/6889489/161649291-2a45d1e4-6556-4d16-aeee-d0408067217d.png)


### Part 5: Make the API request

#### Step 1: Make a route that handles the form from Part 3. 
In your **server.py**, you need two routes:
- One to show the form from Part 3
- One to process the form from Part 3

You already know how to create routes that render HTML, so these instructions will not include how to create the first route, which simply shows the form.

For the second route (the one that processes the form), start by creating a route that accepts POST requests. 

#### Step 2: Get the form data
Your route needs to access the uploaded file and save it to a variable. Use the Flask `request` object to get this information. 

`my_file = request.files['my-file']`
   
💡 **Debugging Tip**: Make sure the key you are using to access the file matches the `name` attribute you used in Part 3.

#### Step 3: Make the Cloudinary API request
Next, we need to save the uploaded file to Cloudinary by making an API request. 

Make sure you store the result of the request in a variable! It contains important information.
```
result = cloudinary.uploader.upload(my_file,
         api_key=CLOUDINARY_KEY,
         api_secret=CLOUDINARY_SECRET,
         cloud_name=CLOUD_NAME)
```

#### Step 4: Save the generated URL to your database
The `result` variable is a dictionary of information about the file and the API request. When Cloudinary saved the image file to its servers, it created a URL for the file. You can use this URL to access the image later. 

`img_url = result['secure_url']`

Save this URL to your database so that you can display the image back to the user later. 

For example, if you have a user record from a users table with the column/field profile_url, you could use the user record in your jinja template to display the user’s profile photo like this:

`<img src="{{ user.profile_url }}">`

That’s it! Now you know how to use the Cloudinary API to save images that users upload to your web app.









