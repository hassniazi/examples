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
      token = bearer_token()
      auth = 'Bearer {}'.format(token)
      self.headers = {
          'content-type': 'application/json',
          'authorization': auth
      }
    
    def __request(self, url, method='get'):
      full_url = MAZE_URL + url
      logging.debug('Starting {} request to {}'.format(method.upper(), full_url))
      try:
        request = getattr(requests, method.lower())
        response = request(
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
      except requests.exceptions.ConnectTimeout:
        self.timeout(full_url)
      except AttributeError:
        raise MazeRequesterException(
          'Invalid method {} provided to request'.format(method)
        )

    def get(self, url):
      return self.__request(url, method='get')
      
    def post(self, url):
      return self.__request(url, method='post')
        
    def put(self, url):
      return self.__request(url, method='put')

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
