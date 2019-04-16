from flask import Flask, render_template, redirect, request, jsonify, send_file
from flask_json import FlaskJSON, json_response
from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv(override=True)
import os

import cv2
from pytube import YouTube

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
            path = downloadFromYoutube(url)
            return json_response(path = path)
        except:
            return json_response(status_=404)


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


def downloadFromYoutube(url):
    yt = YouTube(url)
    yt.streams.first().download(output_path='videos/temp' ,filename="video1")
    return '/videos/temp/video1.mp4'