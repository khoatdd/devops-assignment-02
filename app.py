from flask import Flask, request, Response, json
import os
import boto3

app = Flask(__name__)

aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']


def valid_request_data(request_data):
    if ("region" in request_data and "state" in request_data):
        return True
    else:
        return False


@app.route("/ec2", methods=['POST'])
def list_aws_ec2_instances():
    request_data = request.get_json()
    if (valid_request_data(request_data)):
        region_name = request_data['region'].lower()
        state = request_data['state'].lower()
        ec2 = boto3.resource('ec2', aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key, region_name=region_name)
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': [state]}])

        array = []

        for instance in instances:
            array.append(instance.id)

        response = Response(json.dumps(array), status=200,
                            mimetype='application/json')
        return response
    else:
        err_message = {
            "error": "Invalid request body",
            "helpString": "Data passed in similar to this {'region': '<region_name>', 'state': '<instance_state>'}"
        }
        response = Response(json.dumps(err_message),
                            status=400, mimetype='application/json')
        return response

if __name__ == "__main__":
    app.run(ssl_context='adhoc')