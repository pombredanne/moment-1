from flask import render_template, jsonify, send_file, request
from moment import app, redis, q, models


@app.route('/')
def home():
    """Returns the home page, which is an overview of the project."""

    return render_template('home.html')


@app.route('/api/')
def rest_api():
    """Base route for a RESTful API service."""

    return jsonify({"error": "Not implemented. A RESTful API service."})


@app.route('/capture/')
def get_capture():
    """Directly returns captures based on valid request parameters."""

    if not request.args.get('user') or not request.args.get('token'):

        return jsonify({"error": "A valid USER and TOKEN are required."})

    if not request.args.get('url'):

        return jsonify({"error": "A valid URL is required."})

    user = models.User(request_args=request.args)

    if not user.is_valid:

        return jsonify({"error": "Either the USER or TOKEN is invalid."})

    capture = models.Capture(request_args=request.args)

    image = redis.get(capture.key())

    if image:

        return send_file(image)

    image = capture.capture()

    capture.arguments['image'] = image

    q.enqueue(models.q_capture_put, **capture.arguments)

    return send_file(image)
