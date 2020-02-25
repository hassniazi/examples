import json
import logging
import os
import requests

from maze.credentials import bearer_token

MAZE_URL = os.environ.get('MAZE_URL')
DEFAULT_TIMEOUT = 5.0
USE_HTTPS = False
PROXY_VARS = ['http_proxy', 'HTTP_PROXY', 'https_proxy', 'HTTPS_PROXY', 'no_proxy', 'NO_PROXY']

DOCUMENTATION="""
TODO make the functions on this page far more DRY
"""

class MazeRequesterException(Exception):
    pass

def get(url):
    if not MAZE_URL:
        raise MazeRequesterException('Could not find Maze.')
    full_url = MAZE_URL + url
    logging.debug('Starting GET request to {}'.format(full_url))
    token = bearer_token()
    auth = 'Bearer {}'.format(token)
    headers = {
        'authorization': auth,
        'content-type': 'application/json'
    }
    try:
        response = requests.get(
            full_url,
            headers=headers,
            verify=USE_HTTPS,
            timeout=DEFAULT_TIMEOUT
        )
        if response.status_code < 300:
            return response.json()
        else:
            logging.warning('Response status = {}'.format(response.status_code))
            logging.warning(response.text)
            raise MazeRequesterException('Invalid response received: {}.'.format(response.text))
    except requests.exceptions.ReadTimeout:
        msg = 'Request to {} timed out'.format(url)
        logging.critical(msg)
        check_proxy_settings()
        raise MazeRequesterException(msg)

def post(url, data=None):
    if not MAZE_URL:
        raise MazeRequesterException('Could not find Maze.')
    full_url = MAZE_URL + url
    logging.debug('Starting POST request to {}'.format(full_url))
    token = bearer_token()
    auth = 'Bearer {}'.format(token)
    headers = {
        'authorization': auth,
        'content-type': 'application/json'
    }
    try:
        response = requests.post(
            full_url,
            data=json.dumps(data),
            headers=headers,
            verify=USE_HTTPS,
            timeout=DEFAULT_TIMEOUT
        )
        if response.status_code < 300:
            return response.json()
        else:
            logging.warning('Response status = {}'.format(response.status_code))
            logging.warning(response.text)
            raise MazeRequesterException('Invalid response received: {}.'.format(response.text))
    except requests.exceptions.ReadTimeout:
        msg = 'Request to {} timed out'.format(url)
        logging.critical(msg)
        check_proxy_settings()
        raise MazeRequesterException(msg)

def put(url, data=None):
    if not MAZE_URL:
        raise MazeRequesterException('Could not find Maze.')
    full_url = MAZE_URL + url
    logging.debug('Starting PUT request to {}'.format(full_url))
    token = bearer_token()
    auth = 'Bearer {}'.format(token)
    headers = {
        'authorization': auth,
        'content-type': 'application/json'
    }
    try:
        response = requests.put(
            full_url,
            data=json.dumps(data),
            headers=headers,
            verify=USE_HTTPS,
            timeout=DEFAULT_TIMEOUT
        )
        if response.status_code < 300:
            return response.json()
        else:
            logging.warning('Response status = {}'.format(response.status_code))
            logging.warning(response.text)
            raise MazeRequesterException('Invalid response received: {}.'.format(response.text))
    except requests.exceptions.ReadTimeout:
        msg = 'Request to {} timed out'.format(url)
        logging.critical(msg)
        check_proxy_settings()
        raise MazeRequesterException(msg)

def check_proxy_settings():
    """
    Runs a check on values of local proxy settings
    """
    kv = ['{}={}'.format(k, os.environ.get(k)) for k in PROXY_VARS]
    logging.debug(', '.join(kv))
