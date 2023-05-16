# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import json
import base64
import requests
import argparse
import os

def get_jwt(username, password, tenant_name, api_url):

    auth_str = f'{username}:{password}'
    byte_str = auth_str.encode('ascii')
    auth_b64 = base64.b64encode(byte_str)

    headers = {
        'Authorization': 'Basic {}'.format(auth_b64.decode('ascii')),
        'tenant-name': tenant_name
    }

    try:
        print("Getting JWT")
        response = requests.get(api_url + 'v1/jwt', headers=headers)
        print(response.text if response.text else response.reason)
        jwt = json.loads(response.text)['jwt']
        return jwt
    except Exception as e:
        print("Error getting JWT", e)
        exit(1)

def run_inference(username, password, tenant_name, request, api_url):

    jwt = get_jwt(username, password, tenant_name, api_url)

    headers = {
        'Authorization': 'Bearer {}'.format(jwt),
        'Content-Type': 'text/csv'
    }

    try:
        print(f"Inference request with: {request}")
        response = requests.post(api_url + 'v2/inference', headers=headers, data=request)
        print(response.text if response.text else response.reason)
    except Exception as e:
        print("Error executing inference request", e)
        exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload Tenant ML Training Data File to S3')
    parser.add_argument('--username', type=str, help='username', required=True)
    parser.add_argument('--password', type=str, help='password', required=True)
    parser.add_argument('--tenant-name', type=str, help='tenant name', required=True)
    parser.add_argument('--request', type=str, help='request', required=True)
    parser.add_argument('--api-url', type=str, help='rest api url endpoint', required=True)
    args = parser.parse_args()

    run_inference(**vars(args))