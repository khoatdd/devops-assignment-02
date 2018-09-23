import os

import boto3
from flask import Flask, Response, json, request

from health import HealthCheckException
from helpers.middleware import setup_metrics

app = Flask(__name__)

setup_metrics(app)

aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']


def valid_request_data(request_data):
    if ("region" in request_data and "state" in request_data):
        return True
    else:
        return False


@app.errorhandler(HealthCheckException)
def handle_health_check(error):
    message = error.to_dict()['message']
    status_code = error.status_code
    response = Response(json.dumps({'status': message}), status=status_code,
                        mimetype='application/json')
    return response


@app.route("/healthz", methods=['GET'])
def health_check():
    try:
        ec2 = boto3.resource(
            'ec2',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name="us-east-1")
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
        for instance in instances:
            print instance.id
        response = Response(json.dumps({'status': 'OK'}), status=200,
                            mimetype='application/json')
        return response
    except Exception as e:
        raise HealthCheckException('SOS', status_code=503)


@app.route("/ec2", methods=['POST'])
def list_aws_ec2_instances():
    request_data = request.get_json()
    if (valid_request_data(request_data)):
        region_name = request_data['region'].lower()
        state = request_data['state'].lower()
        try:
            ec2 = boto3.resource('ec2',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key,
                                 region_name=region_name)
            instances = ec2.instances.filter(
                Filters=[{'Name': 'instance-state-name', 'Values': [state]}])
            array = []
            for instance in instances:
                array.append(instance.id)
        except Exception:
            pass
        response = Response(json.dumps(array), status=200,
                            mimetype='application/json')
        return response
    else:
        err_message = {
            "error": "Invalid request body",
            "helpString": "Data passed in similar to this \
                           {'region': '<region_name>', \
                           'state': '<instance_state>'}"
        }
        response = Response(json.dumps(err_message),
                            status=400, mimetype='application/json')
        return response
