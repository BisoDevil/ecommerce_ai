from flask import Flask, request, jsonify,render_template
from joblib import load
import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import g4f
import rem_background
import os
from werkzeug.utils import secure_filename
from PIL import Image
import requests

nltk.download('stopwords')

app = Flask(__name__,template_folder='templates')

app.config['UPLOAD_FOLDER'] = 'static/uploads'



# # Load the saved model
# model = load('model.joblib')
# vectorizer = load('vectorizer.joblib')

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))




def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = BeautifulSoup(text, "lxml").text 
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwors from text
    return text

# Define the API route
@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({'category': "Test"})
    # # Get the text input from the request
    # texts = request.json['texts']
    # # Preprocess the text
    # preprocessed_texts = []
    # for text in texts:
    #     preprocessed_texts.append(clean_text(text))

    # # Vectorize the preprocessed text
    # text_vector = vectorizer.transform(preprocessed_texts)
    

    # # Make the prediction
    # categories = model.predict(text_vector)
    # ex = []
    # for i in categories:
    #     ex.append(str(i))
    # # Return the predicted category as JSON response
    # return jsonify({'category': ex})


@app.route('/generate', methods=['POST'])
async def generate():
    text = request.json['text']
    bullets = request.json['bullet']
   
    
    prefix = f'As a professional product content specialist at amazon ecommerce, I would like to generate a three product titles based on ِAmazon title guidelines in 150 characters, {bullets} marketing feature bullets, rich description over 2000 character, product attributes. Based on the below info:'    
#     body = {
#     "contents": [
#         {
#             "parts": [
#                 {
#                     "text": f'{prefix}\n{text}'
#                 }
#             ]
#         }
#     ]
# }
#     res = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyASi5HIYqtFix7TSYHgimaMuYiXIyJhH_U',json=body)
#     chunks = []
#     for item in res.json()['candidates']:
#         for part in item['content']['parts']:
#             chunks.append(part['text'])




    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=[
            {
                    "role": "user",
                    "content":  f'{prefix} {text}'
                }
        ],
        stream=True,
        ignore_stream_and_auth=True
    )

    chunks = []

    for chunk in response:
        chunks.append(chunk)

    return jsonify({'message': ''.join(chunks).strip()})


@app.route('/remove_background', methods=['POST'])
def remove_background():
    # Get the image file from the request
    image_file = request.files['image']
    # Preprocess the image
    image,pred = rem_background.removeBackground(Image.open(image_file))
    
    filename = secure_filename(image_file.filename) # Generate a unique filename
    file_path = os.path.join('static', 'uploads', filename)
    
    
    image.save(file_path) # Save the file to the specified path
    download_url = request.host_url + file_path 
    # Return the image as a response
    return jsonify({'image':download_url,'pred':pred})
    





@app.route('/', methods=['GET'])
def index():
    
    return render_template('index.html')
    



if __name__ == '__main__':
    
    # app.run(debug=True,)
    app.run(host='0.0.0.0',port=5000,use_reloader=True, threaded=True)
