
import logging
import os
import sys
import platform
import time
import re
import multiprocessing
import subprocess
import socket
try:
    import resource
except ImportError:
    pass

import graphsignal
from graphsignal.proto import profiles_pb2
from graphsignal.proto_utils import parse_semver
from graphsignal import version

logger = logging.getLogger('graphsignal')

OS_LINUX = (sys.platform.startswith('linux'))
OS_DARWIN = (sys.platform == 'darwin')
OS_WIN = (sys.platform == 'win32')
CPU_NAME_REGEXP = re.compile(r'Model name:\s+(.+)$', flags=re.MULTILINE)
CPU_NAME_MAC_REGEXP = re.compile(r'machdep\.cpu\.brand_string:\s+(.+)$', flags=re.MULTILINE)
VM_RSS_REGEXP = re.compile(r'VmRSS:\s+(\d+)\s+kB')
VM_SIZE_REGEXP = re.compile(r'VmSize:\s+(\d+)\s+kB')
MEM_TOTAL_REGEXP = re.compile(r'MemTotal:\s+(\d+)\s+kB')
MEM_FREE_REGEXP = re.compile(r'MemFree:\s+(\d+)\s+kB')


class ProcessReader():
    def __init__(self):
        self._start_ms = int(time.time() * 1e3)
        self._last_read_sec = None
        self._last_cpu_time_ns = None

    def setup(self):
        pass

    def shutdown(self):
        pass

    def start(self):
        self.read(profiles_pb2.MLProfile())

    def read(self, profile):
        now = time.time()
        pid = str(os.getpid())

        node_usage = profile.node_usage
        process_usage = profile.process_usage
        process_usage.start_ms = self._start_ms

        process_usage.process_id = pid

        if OS_LINUX:
            cpu_name = _read_cpu_name()
            if cpu_name:
                process_usage.cpu_name = cpu_name
        elif OS_DARWIN:
            cpu_name = _read_cpu_name_mac()
            if cpu_name:
                process_usage.cpu_name = cpu_name

        if not OS_WIN:
            cpu_time_ns = _read_cpu_time()
            if cpu_time_ns is not None:
                if self._last_cpu_time_ns is not None:
                    cpu_diff_ns = cpu_time_ns - self._last_cpu_time_ns
                    interval_ns = (now - self._last_read_sec) * 1e9
                    cpu_usage = (cpu_diff_ns / interval_ns) * 100
                    try:
                        cpu_usage = cpu_usage / multiprocessing.cpu_count()
                    except Exception:
                        pass
                    process_usage.cpu_usage_percent = cpu_usage

                if (self._last_read_sec is None or now - self._last_read_sec > 0):
                    self._last_read_sec = now
                    self._last_cpu_time_ns = cpu_time_ns

        if not OS_WIN:
            max_rss = _read_max_rss()
            if max_rss is not None:
                process_usage.max_rss = max_rss

        if OS_LINUX:
            current_rss = _read_current_rss()
            if current_rss is not None:
                process_usage.current_rss = current_rss

            vm_size = _read_vm_size()
            if vm_size is not None:
                process_usage.vm_size = vm_size

        try:
            node_usage.hostname = socket.gethostname()
            if node_usage.hostname:
                node_usage.ip_address = socket.gethostbyname(node_usage.hostname)
        except BaseException:
            logger.debug('Error reading hostname', exc_info=True)

        mem_total = _read_mem_total()
        if mem_total is not None:
            node_usage.mem_total = mem_total
            mem_free = _read_mem_free()
            if mem_free is not None:
                node_usage.mem_used = mem_total - mem_free

        try:
            node_usage.platform = sys.platform
            node_usage.machine = platform.machine()
            if not OS_WIN:
                node_usage.os_name = os.uname().sysname
                node_usage.os_version = os.uname().release
        except BaseException:
            logger.error('Error reading node information', exc_info=True)

        try:
            process_usage.runtime = profiles_pb2.ProcessUsage.Runtime.PYTHON
            process_usage.runtime_version.major = sys.version_info.major
            process_usage.runtime_version.minor = sys.version_info.minor
            process_usage.runtime_version.patch = sys.version_info.micro
            process_usage.runtime_impl = platform.python_implementation()
            parse_semver(profile.profiler_info.version, version.__version__)
        except BaseException:
            logger.error('Error reading process information', exc_info=True)


def _read_cpu_name():
    try:
        result = subprocess.run(['lscpu'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
    except Exception:
        return None

    match = CPU_NAME_REGEXP.search(output)
    if match:
        return match.group(1)

    return None


def _read_cpu_name_mac():
    try:
        result = subprocess.run(['sysctl', '-a'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
    except Exception:
        return None

    match = CPU_NAME_MAC_REGEXP.search(output)
    if match:
        return match.group(1)

    return None


def _read_cpu_time():
    rusage = resource.getrusage(resource.RUSAGE_SELF)
    return int((rusage.ru_utime + rusage.ru_stime) * 1e9)  # ns


def _read_max_rss():
    rusage = resource.getrusage(resource.RUSAGE_SELF)

    if OS_DARWIN:
        return rusage.ru_maxrss
    else:
        return rusage.ru_maxrss * 1024


def _read_current_rss():
    pid = os.getpid()

    try:
        f = open('/proc/{0}/status'.format(os.getpid()))
        output = f.read()
        f.close()
    except Exception:
        return None

    match = VM_RSS_REGEXP.search(output)
    if match:
        return int(float(match.group(1)) * 1e3)

    return None


def _read_vm_size():
    pid = os.getpid()

    try:
        f = open('/proc/{0}/status'.format(os.getpid()))
        output = f.read()
        f.close()
    except Exception:
        return None

    match = VM_SIZE_REGEXP.search(output)
    if match:
        return int(float(match.group(1)) * 1e3)

    return None

def _read_mem_total():
    try:
        f = open('/proc/meminfo')
        output = f.read()
        f.close()
    except Exception:
        return None

    match = MEM_TOTAL_REGEXP.search(output)
    if match:
        return int(float(match.group(1)) * 1e3)

    return None

def _read_mem_free():
    try:
        f = open('/proc/meminfo')
        output = f.read()
        f.close()
    except Exception:
        return None

    match = MEM_FREE_REGEXP.search(output)
    if match:
        return int(float(match.group(1)) * 1e3)

    return None
