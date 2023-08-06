import os
import time
import json
import gzip
import sys
import threading
import base64
import logging
from io import BytesIO
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode
from urllib.error import URLError
from urllib.error import HTTPError

import graphsignal
from graphsignal.proto import profiles_pb2

logger = logging.getLogger('graphsignal')


class Uploader:
    MAX_BUFFER_SIZE = 2500

    def __init__(self):
        self.profile_api_url = 'https://profile-api.graphsignal.com'
        self.buffer = []
        self.buffer_lock = threading.Lock()
        self.flush_lock = threading.Lock()

    def configure(self):
        if 'GRAPHSIGNAL_PROFILE_API_URL' in os.environ:
            self.profile_api_url = os.environ['GRAPHSIGNAL_PROFILE_API_URL']

    def clear(self):
        with self.buffer_lock:
            self.buffer = []

    def upload_profile(self, profile):
        with self.buffer_lock:
            self.buffer.append(profile)
            if len(self.buffer) > self.MAX_BUFFER_SIZE:
                self.buffer = self.buffer[-self.MAX_BUFFER_SIZE:]

    def flush_in_thread(self):
        threading.Thread(target=self.flush).start()

    def flush(self):
        with self.flush_lock:
            with self.buffer_lock:
                if len(self.buffer) == 0:
                    return
                outgoing = self.buffer
                self.buffer = []
            try:
                upload_start = time.time()
                upload_request = profiles_pb2.UploadRequest()
                upload_request.ml_profiles.extend(outgoing)
                upload_request.upload_ms = int(time.time() * 1e3)
                payload = upload_request.SerializeToString()
                resp = self._post('profiles', payload)
                upload_response = profiles_pb2.UploadResponse()
                upload_response.ParseFromString(resp)
                logger.debug('Upload took %.3f sec (%dB)', time.time() - upload_start, len(payload))
            except URLError:
                logger.debug('Failed uploading profiles, will retry', exc_info=True)
                with self.buffer_lock:
                    self.buffer[:0] = outgoing
            except Exception:
                logger.error('Error uploading profiles', exc_info=True)

    def _post(self, endpoint, data):
        logger.debug('Posting data to %s/%s',
                     self.profile_api_url, endpoint)

        api_key_64 = _base64_encode(
            graphsignal._agent.api_key + ':').replace('\n', '')
        headers = {
            'Accept-Encoding': 'gzip',
            'Authorization': "Basic %s" % api_key_64,
            'Content-Type': 'application/octet-stream',
            'Content-Encoding': 'gzip'
        }

        gzip_out = BytesIO()
        with gzip.GzipFile(fileobj=gzip_out, mode="w") as out_file:
            out_file.write(data)
            out_file.close()

        gzip_out_val = gzip_out.getvalue()
        if isinstance(gzip_out_val, str):
            data_gzip = bytearray(gzip_out.getvalue())
        else:
            data_gzip = gzip_out.getvalue()
        request = Request(
            url=self.profile_api_url + '/' + endpoint,
            data=data_gzip,
            headers=headers)

        try:
            resp = urlopen(request, timeout=10)
            result_data = resp.read()
            if resp.info():
                content_type = resp.info().get('Content-Encoding')
                if content_type == 'gzip':
                    result_data = gzip.GzipFile(
                        '', 'r', 0, BytesIO(result_data)).read()
            resp.close()
            return result_data
        except HTTPError as herr:
            logger.debug('Error message from server: %s',
                         herr.read().decode('utf-8'))
            raise herr


def _base64_encode(s):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')
