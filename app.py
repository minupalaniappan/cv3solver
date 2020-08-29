from flask import Flask, request, jsonify, make_response

app = Flask(__name__)


@app.route('/solve', methods=['POST'])
def index():
    response_payload = {}

    response_payload['sitekey'] = request.json['sitekey']
    response_payload['action'] = request.json['action']

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

    if len(response_payload.get('errors')) > 0:
        status = 422
    else:
        status = 200

    return make_response(jsonify(response_payload), status)


def add_error(val, errors, message):
    if val is None or len(val) is 0:
        errors.append(message)

    return errors
