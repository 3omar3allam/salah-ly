from flask import Flask, render_template, redirect, request, jsonify, send_file, send_from_directory
from flask_json import FlaskJSON, json_response
# from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv(override=True)
import os
import json

import cv2
from packages.pytube import YouTube

app = Flask(__name__)
FlaskJSON(app)

# client = MongoClient(os.getenv('MONGO_CONN_STR'))
# db = client['salah-ly']

start = None
end = None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            url = request.form.get('url')
            title, path = downloadFromYoutube(url)
            start = request.form.get('start')
            end = request.form.get('end')
            if start:
                start = int(start)
            if end:
                end = int(end)
            return json_response(path = path, title=title)
        except Exception as error:
            print('Upload error >>> ', error)
            return json_response(status_=404,data_={'message': 'Failed to get video'})

@app.route('/videos/<string:filename>', methods=["GET"])
def previewVideo(filename):
    try:
        return send_file(f'videos/{filename}')
    except FileNotFoundError:
        return json_response(status_=404)


@app.route('/convert', methods=['POST'])
def convertVideo():
    from OpenCV_Processing.VideoProcessing import VideoProcessing
    data = request.json
    color1 = [
        data.get('color1').get('h')//2,
        data.get('color1').get('s')*255 // 100,
        data.get('color1').get('b')*255 // 100
    ]
    color2 = [
        data.get('color2').get('h')//2,
        data.get('color2').get('s')*255 // 100,
        data.get('color2').get('b')*255 // 100
    ]
    try:
        VideoProcessing(color1, color2, start, end)
        return json_response(path = 'videos/temp/video1.mp4')
    except Exception as error:
        print('Processing error >>> ', error)
        return json_response(status_=404,data_={'message': 'An error occured'})

@app.route('/about', methods=['GET'])
def about():
    return render_template('blog.html')

def downloadFromYoutube(url):
    os.makedirs('videos', exist_ok=True)
    yt = YouTube(url)
    title = yt.title
    yt.streams.first().download(output_path='videos' ,filename="video1")
    return title, 'videos/video1.mp4'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
