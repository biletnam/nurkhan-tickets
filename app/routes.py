from app import app
from flask import render_template, send_from_directory, jsonify, request
from .models import Event


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/service-worker.js', methods=['GET'])
def serve_service_worker():
    return send_from_directory(app.static_folder + '/..', 'service-worker.js')


@app.route('/get-events', methods=['GET'])
def get_events():
    return jsonify(events=Event.get_all_serialized())


@app.route('/event/<event_url>', methods=['GET'])
def get_event(event_url):
    event = Event.get_by_url(event_url)
    if not event:
        return jsonify('Bad request')
    return jsonify(event=event.serialize())
