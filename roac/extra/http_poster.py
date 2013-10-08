# vim: set fileencoding=utf-8 :

from roac import Result
import requests
import socket
import json
import logging


logger = logging.getLogger(__name__)


class ResultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Result):
            return {'name': obj.name,
                    'path': obj.path,
                    'data': obj.data}
        return json.JSONEncoder.default(self, obj)


class HTTPPoster(object):
    """Posts the scripts' data to an aggregator"""
    def __init__(self, app=None):
        if app:
            self.init_app(app)
        self.node_name = socket.gethostname()
        self.encoder = ResultEncoder()

    def init_app(self, app):
        self.app = app
        app.after_handlers(self.post_to_service)

    def post_to_service(self):
        url_template = self.app.config['aggregator_url']
        url = url_template.format(node_name=self.node_name)
        logger.debug('Posting data to %s' % url)
        try:
            r = requests.post(url, 
                          data=self.encoder.encode(self.app.last_output),
                          headers={'Content-Type': 'application/json'})
        except Exception as e:
            logger.exception("Couldn't post data: %s" % e)

