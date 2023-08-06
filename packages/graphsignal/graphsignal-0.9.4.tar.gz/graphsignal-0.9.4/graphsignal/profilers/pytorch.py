from typing import Optional
import logging
import os
import sys
import time
import gzip
import torch
from torch.autograd import DeviceType
import torch.distributed

import graphsignal
from graphsignal.proto_utils import parse_semver
from graphsignal.proto import profiles_pb2
from graphsignal.inference_span import InferenceSpan
from graphsignal.profilers.operation_profiler import OperationProfiler
from graphsignal.profilers.profiler_utils import create_log_dir, remove_log_dir

logger = logging.getLogger('graphsignal')


class PyTorchProfiler(OperationProfiler):
    def __init__(self):
        self._torch_prof = None
        self._log_dir = None
        self._pytorch_version = None
        self._global_rank = None
        self._world_size = None
        self._comm_backend = None

    def start(self, profile, context):
        logger.debug('Activating PyTorch profiler')

        if not self._torch_prof:
            # Initialization
            def _schedule_func(step):
                return torch.profiler.ProfilerAction.RECORD

            self._torch_prof = torch.profiler.profile(
                schedule=_schedule_func,
                record_shapes=False,
                profile_memory=True,
                with_stack=False,
                with_flops=True)

            self._pytorch_version = profiles_pb2.SemVer()
            parse_semver(self._pytorch_version, torch.__version__)

            if torch.distributed.is_available():
                if torch.distributed.is_initialized():
                    self._global_rank = torch.distributed.get_rank()
                    self._world_size = torch.distributed.get_world_size()
                    self._comm_backend = torch.distributed.get_backend()

        # Profiler info
        profile.profiler_info.operation_profiler_type = profiles_pb2.ProfilerInfo.ProfilerType.PYTORCH_PROFILER

        # Framework info
        framework = profile.frameworks.add()
        framework.type = profiles_pb2.FrameworkInfo.FrameworkType.PYTORCH_FRAMEWORK
        framework.version.CopyFrom(self._pytorch_version)

        # Process info
        if self._global_rank is not None and self._global_rank >= 0:
            if graphsignal._agent.global_rank == -1:
                profile.process_usage.global_rank = self._global_rank

        # Step stats
        if self._world_size is not None and self._world_size > 0:
            profile.inference_stats.world_size = self._world_size
            graphsignal.log_param('world_size', self._world_size)

        # Communication info
        if self._comm_backend:
            if self._comm_backend == 'nccl':
                profile.comm_usage.backend_type = profiles_pb2.CommunicationUsage.CommunicationBackendType.NCCL
            if self._comm_backend == 'gloo':
                profile.comm_usage.backend_type = profiles_pb2.CommunicationUsage.CommunicationBackendType.GLOO
            if self._comm_backend == 'mpi':
                profile.comm_usage.backend_type = profiles_pb2.CommunicationUsage.CommunicationBackendType.MPI

        self._torch_prof.start()

    def stop(self, profile, context):
        logger.debug('Deactivating PyTorch profiler')

        self._torch_prof.stop()

        self._convert_operations(profile)

        self._read_chrome_trace(profile)

    def _convert_operations(self, profile):
        # Operation stats
        for event_avg in self._torch_prof.key_averages():
            if event_avg.key and event_avg.key.startswith('ProfilerStep'):
                continue
            op_stats = profile.op_stats.add()
            op_stats.op_name = event_avg.key
            op_stats.count = _uint(event_avg.count)
            op_stats.total_host_time_us = _uint(event_avg.cpu_time_total)
            op_stats.total_device_time_us = _uint(event_avg.cuda_time_total)
            op_stats.self_host_time_us = _uint(event_avg.self_cpu_time_total)
            op_stats.self_device_time_us = _uint(event_avg.self_cuda_time_total)
            op_stats.total_host_memory = _uint(event_avg.cpu_memory_usage)
            op_stats.total_device_memory = _uint(event_avg.cuda_memory_usage)
            op_stats.self_host_memory = _uint(event_avg.self_cpu_memory_usage)
            op_stats.self_device_memory = _uint(event_avg.self_cuda_memory_usage)
            op_stats.flops = _uint(event_avg.flops)
            if event_avg.device_type in (DeviceType.CUDA, DeviceType.HIP)  or op_stats.self_device_time_us > 0:
                op_stats.device_type = profiles_pb2.DeviceType.GPU
            else:
                op_stats.device_type = profiles_pb2.DeviceType.CPU

        # Kernel stats
        kernel_index = {}
        for event in self._torch_prof.events():
            for kernel in event.kernels:
                key = (event.key, kernel.name, kernel.device)
                if key in kernel_index:
                    kernel_stats = kernel_index[key]
                    kernel_stats.count += 1
                    kernel_stats.duration_ns += _uint(kernel.duration * 1000)
                else:
                    kernel_stats = kernel_index[key] = profile.kernel_stats.add()
                    kernel_stats.device_type = profiles_pb2.DeviceType.GPU
                    kernel_stats.device_id = str(kernel.device)
                    kernel_stats.op_name = event.name
                    kernel_stats.kernel_name = kernel.name
                    kernel_stats.count = 1
                    kernel_stats.duration_ns = _uint(kernel.duration * 1000)

        for kernel_stats in kernel_index.values():
            profile.kernel_stats.append(kernel_stats)

        logger.debug(
            'Converted %d PyTorch operation statistics', len(profile.op_stats))

    def _read_chrome_trace(self, profile):
        try:
            self._log_dir = create_log_dir()

            trace_path = os.path.join(self._log_dir, 'trace.json')
            self._torch_prof.export_chrome_trace(trace_path)

            if os.path.getsize(trace_path) > 50 * 1e6:
                raise Exception('Trace file too big')

            with open(trace_path) as f:
                trace_json = f.read()
                profile.trace_data = gzip.compress(trace_json.encode())
        except Exception as e:
            logger.error('Error exporting Chrome trace', exc_info=True)
        finally:
            remove_log_dir(self._log_dir)

def _uint(val):
    return max(int(val), 0)


_profiler = PyTorchProfiler()

def profile_inference(
        batch_size: Optional[int] = None,
        ensure_profile: Optional[bool] = False) -> InferenceSpan:
    graphsignal._check_configured()

    return InferenceSpan(
        batch_size=batch_size,
        ensure_profile=ensure_profile,
        operation_profiler=_profiler)
