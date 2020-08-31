import os

from flask import Flask, request, jsonify, make_response
from lib import browser

app = Flask(__name__)

port = int(os.environ.get('PORT', 5000))


@app.route('/solve', methods=['POST'])
def index():
    response_payload = {}

    response_payload['sitekey'] = request.json['sitekey']
    response_payload['action'] = request.json['action']
    response_payload['site'] = request.json['site']

    response_payload['errors'] = []

    status = 0

    response_payload['errors'] = add_error(
        response_payload.get('sitekey'),
        response_payload['errors'],
        'Site key is required'
    )

    response_payload['errors'] = add_error(
        response_payload.get('action'),
        response_payload['errors'],
        'Action is required'
    )

    response_payload['errors'] = add_error(
        response_payload.get('site'),
        response_payload['errors'],
        'Site is required'
    )

    if len(response_payload.get('errors')) > 0:
        status = 422
    else:
        status = 200

    if status is 200:
        response_payload['solution'] = browser.solve(
            response_payload.get('sitekey'),
            response_payload.get('action'),
            response_payload.get('site')
        )

    return make_response(jsonify(response_payload), status)


def add_error(val, errors, message):
    if val is None or len(val) is 0:
        errors.append(message)

    return errors


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
