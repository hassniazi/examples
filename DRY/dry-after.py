import json
import logging
import os
import requests

from maze.credentials import bearer_token

MAZE_URL = os.environ.get('MAZE_URL')
DEFAULT_TIMEOUT = 5.0
USE_HTTPS = False
PROXY_VARS = ['http_proxy', 'HTTP_PROXY', 'https_proxy', 'HTTPS_PROXY', 'no_proxy', 'NO_PROXY']


class MazeRequesterException(Exception):
    pass

class MazeRequester:
    def __init__(self, data={}):
      
      if not MAZE_URL:
        logging.debug('MAZE_URL not in {}'.format(os.environ.keys()))
        raise MazeRequesterException('Could not find Maze.')
      self.data = data
      token = os.environ.get('BEARER_TOKEN') 
      auth = 'Bearer {}'.format(token)
      self.headers = {
          'content-type': 'application/json',
          'authorization': auth
      }

    def get(self,url):
      full_url = MAZE_URL + url
      logging.debug('Starting GET request to {}'.format(full_url))
      try:
        response = requests.get(
            full_url,
            headers=self.headers,
            verify=USE_HTTPS,
            timeout=DEFAULT_TIMEOUT
        )
        if response.status_code >= 300:
            self.error_handler(response)
        else:
          return response.json()
      except requests.exceptions.ReadTimeout:
        self.timeout(full_url)

    def post(self, url):
      full_url = MAZE_URL + url
      logging.debug('Starting POST request to {}'.format(full_url))
      try:
        response = requests.post(
            full_url,
            headers=self.headers,
            data = json.dumps(self.data),
            verify=USE_HTTPS,
            timeout=DEFAULT_TIMEOUT
        )
        if response.status_code >= 300:
            self.error_handler(response)
        else:
          return response.json()
      except requests.exceptions.ReadTimeout:
        self.timeout(full_url)
        
    def put(self, url):
      full_url = MAZE_URL + url
      logging.debug('Starting PUT request to {}'.format(full_url))
      try:
        response = requests.put(
            full_url,
            headers=self.headers,
            data = json.dumps(self.data),
            verify=USE_HTTPS,
            timeout=DEFAULT_TIMEOUT
        )
        if response.status_code >= 300:
            self.error_handler(response)
        else:
          return response.json()
      except requests.exceptions.ReadTimeout:
        self.timeout(full_url)

    def error_handler(self,response):
      logging.warning('Response status = {}'.format(response.status_code))
      logging.warning(response.text)
      raise MazeRequesterException('Invalid response received: {}.'.format(response.text))

    def timeout(self, url):
        msg = 'Request to {} timed out'.format(url)
        logging.critical(msg)
        self.check_proxy_settings()
        raise MazeRequesterException(msg)      

    def check_proxy_settings(self):
      """
      Runs a check on values of local proxy settings
      """
      kv = ['{}={}'.format(k, os.environ.get(k)) for k in PROXY_VARS]
      logging.debug(', '.join(kv))
