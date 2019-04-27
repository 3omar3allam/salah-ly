from flask import Flask, render_template, redirect, request, jsonify, send_file, send_from_directory
from flask_json import FlaskJSON, json_response
from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv(override=True)
import os

import cv2
from packages.pytube import YouTube

app = Flask(__name__)
FlaskJSON(app)

client = MongoClient(os.getenv('MONGO_CONN_STR'))
db = client['salah-ly']

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            url = request.form.get('url')
            title, path = downloadFromYoutube(url)
            return json_response(path = path, title=title)
        except:
            return json_response(status_=404,data_={'message': 'Failed to get video'})


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/videos/temp/<string:url>')
def previewVideo(url):
    try:
        f = open(f'videos/temp/{url}','r')
        return send_file(f'videos/temp/{url}')
    except FileNotFoundError:
        return json_response(status_=404)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'icon'),
                               'favicon.ico', mimetype='image/png')

def downloadFromYoutube(url):
    os.makedirs('videos/temp',exist_ok=True)
    
    yt = YouTube(url)
    title = yt.title
    yt.streams.first().download(output_path='videos/temp' ,filename="video1")
    return title, '/videos/temp/video1.mp4'

if __name__ == '__main__':
    app.run()
