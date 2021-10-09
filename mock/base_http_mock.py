#! /usr/bin/env python
# encoding=utf-8
# Author: shuyiqing
# Date: 2017/8/20
import time
import json
import logging
import socketserver
from http.server import BaseHTTPRequestHandler

from common.config_util import getconfig

logger = logging.getLogger(__name__)

config = getconfig()
stop_flag = False


class JsonRequestMockMixin(object):
    url_scheme = None
    json_schema = None
    received_request = None
    mocked_response = None
    check_data = None
    received_url = None
    response_content_type = None

    def request_handler(self, request_url, json_request=None):
        self.received_url = request_url
        self.received_request = json_request
        logger.info("Mock Server Received URL : %s " % self.received_url)
        logger.info("Mock Server Received Request: %s", json.dumps(self.received_request, indent=2, ensure_ascii=False))
        self.mocked_response = self.mock_response(received_url=self.received_url,
                                                  received_request=self.received_request)
        self.response_content_type = self.set_content_type(received_url=self.received_url)
        logger.info("Mocked response: \n %s", json.dumps(self.mocked_response, indent=2, ensure_ascii=False))
    def mock_response(self, received_url=None, received_request=None):
        return None

    def set_content_type(self, received_url):
        return None


class RequestHandler(BaseHTTPRequestHandler):
    port = 8080
    content_type = 'application/json;charset=utf-8'
    content_type2 = 'application/json; charset=UTF-8'
    mock = None

    def do_GET(self):
        # Check the url if it matches the scheme
        logger.info('URL : %s ' % self.mock.url_scheme)
        logger.info('Received HTTP Header : %s ' % self.headers)
        self.mock.request_handler(self.path)
        if self.mock.mocked_response is not None:
            if 'send_error' in self.mock.mocked_response:
                if 'message' in self.mock.mocked_response['send_error']:
                    self.send_error(
                        self.mock.mocked_response['send_error']['code'],
                        self.mock.mocked_response['send_error']['message']
                    )
                else:
                    self.send_error(self.mock.mocked_response['send_error']['code'])
            else:
                self.send_response(200)
                self.send_header('Content-Type', self.mock.response_content_type)
                self.end_headers()
                self.wfile.write(json.dumps(self.mock.mocked_response).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', self.mock.response_content_type)
            self.end_headers()
        return

    def do_POST(self):
        json_request = None
        # Check the url if it matches the scheme
        logger.info('URL : %s ' % self.mock.url_scheme)
        logger.info('Received HTTP Header : %s ' % self.headers)
        if 'content-length' in self.headers:
            data = self.rfile.read(int(self.headers['content-length']))
            data = data.decode()
            logger.info('RowData: %s ' % data)
            json_request = json.loads(data)
            logger.info('Request: %s' % json.dumps(json_request, indent=2))
        self.mock.request_handler(self.path, json_request)
        if self.mock.mocked_response is not None:
            if 'send_error' in self.mock.mocked_response:
                if 'message' in self.mock.mocked_response['send_error']:
                    self.send_error(
                        self.mock.mocked_response['send_error']['code'],
                        self.mock.mocked_response['send_error']['message']
                    )
                else:
                    self.send_error(self.mock.mocked_response['send_error']['code'])
            else:
                self.send_response(200)
                self.send_header('Content-Type', self.mock.response_content_type)
                self.end_headers()
                self.wfile.write(json.dumps(self.mock.mocked_response).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', self.mock.response_content_type)
            self.end_headers()
        return


class BaseHttpMock(JsonRequestMockMixin):

    def listen_once(self, port=8080, timeout=None):
        self.RequestHandler = None
        self.received_request = None
        self.has_mocked = False
        if port:
            port = port
        else:
            port = config.get("mock_server_settings", "listen_port")

        self.RequestHandler = RequestHandler
        self.RequestHandler.mock = self
        httpd = socketserver.TCPServer(("0.0.0.0", port), self.RequestHandler, bind_and_activate=False)
        httpd.allow_reuse_address = True
        try:
            httpd.server_bind()
            httpd.server_activate()
        except Exception as err:
            logger.error("'Exception", err)
            httpd.server_close()
        logger.info("Mock server starts listening on port %s" % port)
        if timeout:
            httpd.timeout = timeout
        else:
            httpd.timeout = config.get("mock_server_settings", "listen_timeout")
        httpd.serve_forever()
