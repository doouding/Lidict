"""
Test util to help write test efficiently
"""
import json
from rest_framework.test import APIClient

def test_request(url, method='POST', data=None, content_type='application/json', auth=None, **extra):
    client = APIClient()
    encoder = json.JSONEncoder()
    
    encoded_data = encoder.encode(data) if data else None

    if auth:
        client.force_authenticate(auth)

    if method == 'POST':
        return client.post(url, encoded_data, content_type=content_type, **extra)
    elif method == 'GET':
        return client.get(url, data)
    elif method == 'PUT':
        return client.put(url, encoded_data, content_type=content_type, **extra)
    elif method == 'DELETE':
        return client.delete(url, encoded_data, content_type=content_type, **extra)
    else:
        raise TypeError('Invalid http method')
