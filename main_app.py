from flask import Flask, request, render_template, jsonify
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Set your API URL here
API_URL = 'http://localhost:8000/similar'  # Update this to your FastAPI endpoint

def is_valid_image_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.verify()  # Verify that this is, in fact, an image
        return True
    except (requests.RequestException, IOError):
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    similar_images = []
    input_image_url = None
    error = None
    api_key = '123'
    if request.method == 'POST':
        input_image_url = request.form.get('url')
        #api_key = request.form.get('api_key')
        

        if not is_valid_image_url(input_image_url):
            error = "The provided URL is not a valid image."
        else:
            headers = {
                'Authorization': f'Bearer {api_key}'  # Include the API key in the headers
            }
            #response = requests.post(API_URL, json={'url': input_image_url}, headers=None)
            response = requests.post(API_URL, params={'url': input_image_url})
            if response.status_code == 200:
                similar_images = response.json().get('similar_images', [])
            else:
                error = response.json().get('error', 'Error fetching similar images')
    
    return render_template('index.html', input_image_url=input_image_url, similar_images=similar_images, error=error)


