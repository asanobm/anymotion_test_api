from flask import Flask, request, jsonify, send_file, Response
import anymotion_sdk
import os
import glob
import pandas as pd
import json

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

teaching_videos = []

ANYMOTION_CLIENT_ID = os.getenv('ANYMOTION_CLIENT_ID')
ANYMOTION_CLIENT_SECRET = os.getenv('ANYMOTION_CLIENT_SECRET')

anymotion = anymotion_sdk.Client(
    client_id=ANYMOTION_CLIENT_ID,
    client_secret=ANYMOTION_CLIENT_SECRET)


def res(data):
    response = jsonify({"data": data})
    # response.headers['Content-Type: Application/json']
    return response, 201


def res_from_dataframe(data):
    response = Response(json.dumps(json.loads(data.to_json(orient='records'))))
    response.headers['Content-Type'] = 'Application/json'
    return response


@app.route('/teaching_videos', methods=['GET'])
def get_teaching_videos():

    ls = glob.glob('./.sample_videos/*')
    mp4 = [file for file in ls if file.endswith('.mp4')]

    for file in mp4:
        teaching_videos.append({
            "title": file.title().split("/")[2].split('.Mp4')[0],
            "path": file
        })

    data = pd.DataFrame(teaching_videos)
    print(data)
    return res_from_dataframe(data)


@app.route('/download_teaching_video')
def download_teaching_video():
    path = request.args.get('path')
    return send_file(path)


@app.route('/movies')
def get_movies():
    data = anymotion.get_movies()
    return res(data)


@app.route('/movie')
def get_movie():
    id = request.args.get('id')
    print(id)
    data = anymotion.get_movie(id)
    return res(data)


@app.route('/get_keypoints')
def get_keypoints():
    keypoints = anymotion.get_keypoints()
    return res(keypoints)


@app.route('/get_drawings')
def get_drawings():
    drawings = anymotion.get_drawings()
    return res(drawings)


@app.route('/drawing')
def draw():
    keypoint_id = request.args.get('keypoint_id')
    draw_id = anymotion.draw_keypoint(keypoint_id)
    return res(anymotion.get_drawing(draw_id))


@app.route('/download_drawing')
def download_drawing():
    drawing_id = request.args.get('drawing_id')
    os.remove(".downloads/current.mp4")
    data = anymotion.download(drawing_id, path=".downloads/current.mp4")
    print(data)
    return send_file(".downloads/current.mp4")


if __name__ == "__main__":
    app.run(debug=True)
