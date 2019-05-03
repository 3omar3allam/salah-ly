from flask import Flask, render_template, request, send_file
from flask_json import FlaskJSON, json_response
# from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv(override=True)
import os
import json
import time

from packages.pytube import YouTube

app = Flask(__name__)
FlaskJSON(app)

# client = MongoClient(os.getenv('MONGO_CONN_STR'))
# db = client['salah-ly']

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            url = request.form.get('url')
            title, path = downloadFromYoutube(url)
            return json_response(path = path, title=title)
        except Exception as error:
            print('Download error >>> ', error)
            return json_response(status_=404,data_={'message': 'Failed to get video'})

@app.route('/convert', methods=['POST'])
def convertVideo():
    try :
        from OpenCV_Processing.VideoProcessing import VideoProcessing
        data = request.json
        color1 = [
            data.get('color1').get('h')//2,
            data.get('color1').get('s')*100 // 255,
            data.get('color1').get('b')*100 // 255
        ]
        color2 = [
            data.get('color2').get('h')//2,
            data.get('color2').get('s')*100 // 255,
            data.get('color2').get('b')*100 // 255
        ]
        start = float(data.get('start'))
        end = float(data.get('end'))
        os.makedirs('videos', exist_ok=True)
        path = VideoProcessing(color1, color2, start, end)
        return json_response(path = path)
    except Exception as error:
        print('Processing error >>> ', error)
        return json_response(status_=404,data_={'message': 'An error occured'})

@app.route('/about', methods=['GET'])
def about():
    return render_template('blog.html')

@app.route('/videos/<string:filename>', methods=["GET"])
def previewVideo(filename):
    try:
        f = open(f'videos/{filename}')
        return send_file(f'videos/{filename}')
    except FileNotFoundError:
        return json_response(status_=404)

@app.route('/photos/<string:filename>', methods=["GET"])
def previewPhoto(filename):
    try:
        f = open(f'photos/{filename}')
        return send_file(f'photos/{filename}', cache_timeout=-1)
    except FileNotFoundError:
        return json_response(status_=404)

def downloadFromYoutube(url):
    os.makedirs('videos', exist_ok=True)
    yt = YouTube(url)
    title = yt.title
    yt.streams.first().download(output_path='videos' ,filename="video1")
    return title, 'videos/video1.mp4'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
