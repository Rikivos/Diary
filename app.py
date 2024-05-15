from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]
app = Flask(__name__)

# Connect to MongoDB
diary_collection = db.diary  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(diary_collection.find({}, {'_id': 0}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title = request.form.get('title_give')
    content = request.form.get('content_give')
    
    file = request.files.get('file_give')
    profile = request.files.get('profile_give')

    if file:
        extension = file.filename.split('.')[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'file-{mytime}.{extension}'
        file.save(os.path.join(app.root_path, 'static', filename))
    else:
        filename = 'default-image.jpg'

    if profile:
        extension = profile.filename.split('.')[-1]
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        profilename = f'profile-{mytime}.{extension}'
        profile.save(os.path.join(app.root_path, 'static', profilename))
    else:
        profilename = 'default-profile.jpg'
    
    time = today.strftime('%Y.%m.%d')
    
    doc = {
        'file': filename,
        'profile': profilename,
        'title': title,
        'content': content,
        'time' : time,
    }
    diary_collection.insert_one(doc)
    
    return jsonify({'msg': 'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=600, debug=True)
