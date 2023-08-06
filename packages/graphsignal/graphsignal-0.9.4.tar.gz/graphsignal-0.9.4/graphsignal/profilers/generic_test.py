import unittest
import logging
import sys
import time
from unittest.mock import patch, Mock
from google.protobuf.json_format import MessageToJson
import pprint

import graphsignal
from graphsignal.profilers.generic import profile_inference
from graphsignal.proto import profiles_pb2
from graphsignal.uploader import Uploader

logger = logging.getLogger('graphsignal')


class GenericProfilerTest(unittest.TestCase):
    def setUp(self):
        if len(logger.handlers) == 0:
            logger.addHandler(logging.StreamHandler(sys.stdout))
        graphsignal.configure(
            api_key='k1',
            workload_name='w1',
            debug_mode=True)

    def tearDown(self):
        graphsignal.shutdown()

    @patch.object(Uploader, 'upload_profile')
    def test_profile_inference(self, mocked_upload_profile):
        def slow_method():
            time.sleep(0.1)

        graphsignal.profilers.generic._profiler._exclude_path = 'donotmatchpath'
        with profile_inference():
            slow_method()
            slow_method()

        graphsignal.upload()
        profile = mocked_upload_profile.call_args[0][0]

        #pp = pprint.PrettyPrinter()
        #pp.pprint(MessageToJson(profile))

        foundOp = False
        for op_stats in profile.op_stats:
            if op_stats.op_name.startswith('slow_method') and op_stats.count == 2 and op_stats.total_host_time_us > 200000:
                foundOp = True
                break
        self.assertTrue(foundOp)
