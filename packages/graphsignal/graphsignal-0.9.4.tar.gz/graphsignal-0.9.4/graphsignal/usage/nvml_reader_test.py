import unittest
import logging
import sys
from unittest.mock import patch, Mock
import torch
from google.protobuf.json_format import MessageToJson
import pprint
import time

import graphsignal
from graphsignal.usage.nvml_reader import NvmlReader
from graphsignal.proto import profiles_pb2

logger = logging.getLogger('graphsignal')


class NvmlReaderTest(unittest.TestCase):
    def setUp(self):
        if len(logger.handlers) == 0:
            logger.addHandler(logging.StreamHandler(sys.stdout))
        graphsignal.configure(
            api_key='k1',
            workload_name='w1',
            debug_mode=True)

    def tearDown(self):
        graphsignal.shutdown()

    def test_read(self):
        profile = profiles_pb2.MLProfile()

        x = torch.arange(-50, 50, 0.1).view(-1, 1)
        y = -5 * x + 0.1 * torch.randn(x.size())
        model = torch.nn.Linear(1, 1)
        if torch.cuda.is_available():
            x = x.to('cuda:0')
            y = y.to('cuda:0')
            model = model.to('cuda:0')
        criterion = torch.nn.MSELoss()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

        reader = graphsignal._agent.nvml_reader
        reader.read(profile)

        time.sleep(0.2)

        reader.read(profile)

        #pp = pprint.PrettyPrinter()
        # pp.pprint(MessageToJson(profile))

        if len(profile.device_usage) > 0:
            self.assertTrue(profile.node_usage.num_devices > 0)

            device_usage = profile.device_usage[0]
            self.assertEqual(device_usage.device_type, profiles_pb2.DeviceType.GPU)
            self.assertNotEqual(device_usage.device_id, '')
            self.assertNotEqual(device_usage.device_name, '')
            self.assertNotEqual(device_usage.architecture, '')
            self.assertTrue(device_usage.compute_capability.major > 0)
            self.assertTrue(device_usage.mem_total > 0)
            self.assertTrue(device_usage.mem_used > 0)
            self.assertTrue(device_usage.mem_free > 0)
            self.assertTrue(device_usage.gpu_utilization_percent > 0)
            #self.assertTrue(device_usage.mem_access_percent > 0)
            self.assertTrue(device_usage.gpu_temp_c > 0)
            self.assertTrue(device_usage.power_usage_w > 0)
            #self.assertTrue(device_usage.fan_speed_percent > 0)
            self.assertTrue(device_usage.gpu_temp_c > 0)
            self.assertTrue(device_usage.power_usage_w > 0)
