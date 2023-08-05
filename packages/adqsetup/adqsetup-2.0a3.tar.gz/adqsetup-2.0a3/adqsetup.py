#!/usr/bin/env python
# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022, Intel Corporation
#

import sys, os, time, socket, subprocess, pipes, re, json, math
from array import array
from struct import Struct, unpack, pack
from fcntl import ioctl
from subprocess import CalledProcessError
from tempfile import NamedTemporaryFile
from copy import copy, deepcopy
from collections import OrderedDict, namedtuple
from argparse import (
    ArgumentParser, 
    SUPPRESS,
    FileType,
    RawDescriptionHelpFormatter
)

if sys.version[:1] == '3':
    # Python 3 imports
    from configparser import ConfigParser as SafeConfigParser
    from io import StringIO
    from socket import if_nametoindex, if_indextoname
elif sys.version[:1] == '2':
    # Python 2 imports
    from ConfigParser import SafeConfigParser
    from StringIO import StringIO
    import ctypes
    import ctypes.util

    libc = ctypes.CDLL(ctypes.util.find_library('c'))

    def if_nametoindex(name): # type(str) -> int
        if not isinstance(name, str):
            raise TypeError('name must be a string.')
        ret = libc.if_nametoindex(name)
        if not ret:
            raise RuntimeError("Invalid Name")
        return ret

    def if_indextoname(index): # type: (int) -> str
        if not isinstance(index, int):
            raise TypeError ('index must be an int.')
        libc.if_indextoname.argtypes = [ctypes.c_uint32, ctypes.c_char_p]
        libc.if_indextoname.restype = ctypes.c_char_p
        ifname = ctypes.create_string_buffer(32)
        ifname = libc.if_indextoname(index, ifname)
        if not ifname:
            raise RuntimeError("Inavlid Index")
        return ifname
else:
    raise Exception("Unsupported Python version")

_VERSION_ = '2.0a3'


## public API

__all__ = [
    'Config', 'ConfigGlobals', 'ConfigSection',
    'check_depends', 'check_driver', 'check_interface'
    ]


## example config files

_examples = {}

_examples["memcached"] = '''[globals]
# change the following line to match your CVL interface name
dev = eth4
busypoll = 50000
txadapt = off
txusecs = 0
rxadapt = off
rxusecs = 500
priority = skbedit

[memcd]
# launch memcached with the following options:
# --threads=6 --napi-ids=6
queues = 6
ports = 11211
'''

_examples["nginx"] = '''[globals]
# change the following line to match your CVL interface name
dev = eth4
busypoll = 10000
txadapt = off
txusecs = 0
rxadapt = off
rxusecs = 500
priority = skbedit

[nginx]
# launch nginx with the following option:
# -g "worker_processes 6;"
pollers = 2
queues = 6
ports = 80,443
'''

_examples["redis"] = '''[globals]
# change the following line to match your CVL interface name
dev = eth4
busypoll = 10000
txadapt = off
txusecs = 0
rxadapt = off
rxusecs = 500
priority = skbedit

[redis]
# launch six redis instances on ports 6379 through 6384
mode = shared
queues = 6
ports = 6379-6384
'''

_examples["multi-app"] = '''[globals]
# change the following line to match your CVL interface name
dev = eth4
busypoll = 10000
txadapt = off
txusecs = 0
rxadapt = off
rxusecs = 500
priority = skbedit

[memcd]
# launch memcached with the following options:
# --threads=2 --napi-ids=2
queues = 2
ports = 11211

[redis]
# launch two redis instances on ports 6379 and 6380
mode = shared
queues = 2
ports = 6379-6380

[nginx]
# launch nginx with the following option:
# -g "worker_processes 2;"
queues = 2
ports = 80,443
'''

_service_unit = '''[Unit]
Description=ADQ Setup for %i
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/adqsetup --log=/var/lib/adqsetup/%i.log apply /var/lib/adqsetup/%i.conf

[Install]
WantedBy=multi-user.target
'''

## private functions

def _printhead(s):
    # type: (str) -> None
    ''' 
    Print a header line with a bold font 
    '''
    if sys.stdin.isatty():
        print("\n** \x1B[1m" + str(s) + "\x1B[0m **")
    else:
        print("\n** " + str(s) + " **")

def _hexstr(data): # type: (bytes) -> str
    if data is None:
        return 'None'
    if not isinstance(data, bytearray):
        data = bytearray(data)
    return ''.join('{:02x}'.format(x) for x in data)

def _pack_list(lst, code='B', length=None):
    # type: (list, str, int) -> bytes
    if not length:
        length = len(lst)
    else:
        lst = lst[:length]
        if len(lst) < length:
            lst = lst + [0] * (length - len(lst))
    return pack("%d%s" % (len(lst), code), *lst)

def _exec(args, shell=False, check=False, log=None, echo=False):
    # type: (list, bool, bool, any, bool) -> any
    '''
    Spawn a process, directly or through the shell and capture output
    returns output or success
    '''
    success = True
    stdout = None
    if isinstance(args, list):
        args = [str(s) for s in args]
    else:
        args = [args]

    try:
        stdout = subprocess.check_output(
            args, shell=shell, stderr=subprocess.STDOUT
        ) 
    except CalledProcessError as err:
        if sys.version[:1] == '3':
            output = err.output.decode().strip()
        else:
            output = err.output.strip()
        if not check: 
            raise
        if echo:
            print(output)
        success = False

    if log and success:
        if len(args) > 1:
            command = ' '.join([pipes.quote(s) for s in args])
        else:
            command = args[0]
        log.write("%s\n" % command)

    if stdout is not None:
        if sys.version[:1] == '3':
            stdout = stdout.decode().strip()
        else:
            stdout = stdout.strip()

    if stdout and echo:
        print(stdout)

    if check:
        return success
    else:
        return stdout

def _readfile(path): # type: (list[str]) -> str
    if not os.path.isfile(path):
        raise Exception("%r not found" % path)
    with open(path, 'r') as f:
        return f.read().strip()

def _writefile(path, data): # type(list[str], str) -> int
    if not os.path.isdir(os.path.dirname(path)):
        os.mkdirs(os.path.dirname(path))
    with open(path, 'w') as f:
        return f.write(data)

def _sysctl(key, value=None, log=None):
    # type: (str, any, any) -> str | dict[str, str]
    '''
    Get or set a sysctl value by key
    '''
    path = os.path.join(*(['/proc', 'sys'] + key.split('.')))
    if value is None:
        if os.path.isdir(path):
            results = {}
            for root, _, files in os.walk(path):
                for f in files:
                    key = '.'.join(root.replace(path, '').split(os.sep)[1:] + [f])
                    try:
                        results[key] = _readfile(os.path.join(root, f))
                    except IOError:
                        pass
            return results
        else:
            return _readfile(path)
    else:
        if log:
            log.write("+ sysctl --write %s=%s\n" % (key, str(value)))
        return _writefile(path, value)

def _uevent(dev):
    # type: (str) -> dict
    '''
    Get and parse device/uevent entry for device
    '''
    path = os.path.join(*['/sys', 'class', 'net', dev, 'device', 'uevent'])
    info = dict(re.findall('^([\w\_]+)=(.*)$', _readfile(path), re.MULTILINE))
    return {key.lower(): val for key, val in info.items()}

def _ethtool(dev, command, *args, **kwargs): 
    # type: (str, str, *str, **any) -> str
    '''
    Execute ethtool 'command' for device
    '''
    log = kwargs.pop('log', None)
    return _exec(
        ['ethtool', '--' + command, dev] + list(args),
        log=log
    )

def _devlink_param(dev, key, value=None, log=None): 
    # type: (str, str, any, any) -> str
    '''
    Get or set devlink param for device
    '''
    dev = 'pci/' + _uevent(dev)['pci_slot_name']
    if value is None:
        return _exec(
            ['devlink', 'dev', 'param', 'show', dev, 'name', key], 
            log=log
        )
    else:
        return _exec(
            ['devlink', 'dev', 'param', 'set', dev, 'name', 
              key, 'value', str(value), 'cmode', 'runtime'],
            check=True, log=log
        )

def _tc(dev, object, command, *args, **kwargs): 
    # type: (str, str, str, *str, **any) -> str
    log = kwargs.pop('log', None)
    check = kwargs.pop('check', False)
    tc = "tc"
    if os.path.isfile("/opt/iproute2/sbin/tc"):
        tc = "/opt/iproute2/sbin/tc"
    return _exec(
        [tc, object, command, 'dev', dev] + list(args), 
        log=log, check=check
    )

## nettool abstraction

class StructTemplate(object):
    struct = None
    @classmethod
    def unpack(cls, data): # type: (bytes) -> StructTemplate
        return cls(*cls.struct.unpack(data[:cls.struct.size]))
    def pack(self): # type: () -> bytes
        return self.struct.pack(*self)

class Ethtool(object):
    ## include/uapi/linux/if.h
    IFNAMSIZ = 16
    ## include/uapi/linux/sockios.h
    SIOCETHTOOL = 0x8946        
    ## include/uapi/linux/ethtool.h
    MAX_NUM_QUEUE = 4096
    QUEUE_MASK_SIZE = math.ceil(MAX_NUM_QUEUE / 8)
    ETH_GSTRING_LEN = 32
    ETHTOOL_GCOALESCE  = 0x0000000e # /* Get coalesce config */
    ETHTOOL_SCOALESCE  = 0x0000000f # /* Set coalesce config. */
    ETHTOOL_GRINGPARAM = 0x00000010 # /* Get ring parameters */
    ETHTOOL_SRINGPARAM = 0x00000011 # /* Set ring parameters. */
    ETHTOOL_GSTRINGS   = 0x0000001b
    ETHTOOL_GSTATS     = 0x0000001d
    ETHTOOL_RESET      = 0x00000034
    ETHTOOL_GSSET_INFO = 0x00000037
    ETHTOOL_GPFLAGS    = 0x00000027 # /* Get driver-private flags bitmap */
    ETHTOOL_SPFLAGS    = 0x00000028 # /* Set driver-private flags bitmap */
    ETHTOOL_SRXNTUPLE  = 0x00000035 # /* Add an n-tuple filter to device */
    ETHTOOL_GFEATURES  = 0x0000003a # /* Get device offload settings */
    ETHTOOL_SFEATURES  = 0x0000003b # /* Change device offload settings */
    ETHTOOL_GCHANNELS  = 0x0000003c # /* Get no of channels */
    ETHTOOL_SCHANNELS  = 0x0000003d # /* Set no of channels */    
    ETHTOOL_PERQUEUE   = 0x0000004b # /* Set per queue options */    
    ETH_SS_STATS          = 1
    ETH_SS_PRIV_FLAGS     = 2
    ETH_SS_NTUPLE_FILTERS = 3
    ETH_SS_FEATURES       = 4
    ETHTOOL_RXNTUPLE_ACTION_DROP  = -1 # /* drop packet */
    ETHTOOL_RXNTUPLE_ACTION_CLEAR = -2
    ETH_RESET_FILTER    = 1 << 3
    ETH_RESET_DEDICATED = 0x0000ffff
    ETH_RESET_ALL       = 0xffffffff
    class _ntuple_flow_spec(StructTemplate,
            namedtuple("_ntuple_flow_spec",
                "type ip4_src ip4_dst port_src port_dst tos"
                " ip4_src_mask ip4_dst_mask port_src_mask port_dst_mask"
                " tos_mask vlan_tag vlan_mask data data_mask action")):
        struct = Struct("I4s4s2HB59x2Q2HB59x2H2Qi")
    def __init__(self, ifname, log=None): # type: (str, any) -> None
        self.ifname = ifname
        self.ifindex = if_nametoindex(ifname)
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP
        )
        self.log = log
    def _ioctl(self, data): # type: (bytearray|str|bytes) -> bytearray
        buf = array('B', data)
        ioctl(
            self.socket.fileno(), self.SIOCETHTOOL, 
            pack("16sP", self.ifname.encode(), buf.buffer_info()[0])
        )
        return bytearray(buf)
    def reset(self):
        self._ioctl(pack("2I", self.ETHTOOL_RESET, self.ETH_RESET_DEDICATED))
    def _strings_get(self, id): # type: (int) -> list[str]
        results = []
        resp = self._ioctl(pack("2IQI", self.ETHTOOL_GSSET_INFO, 0, 1 << id, 0))
        mask, length = unpack("8xQI", resp)
        if mask == 0:
            length = 0
        data = bytearray(pack("3I", self.ETHTOOL_GSTRINGS, id, length))
        data.extend(b'\x00' * length * self.ETH_GSTRING_LEN)
        resp = self._ioctl(data)[12:]
        for i in range(length):
            offset = self.ETH_GSTRING_LEN * i
            s = resp[offset:offset+self.ETH_GSTRING_LEN].partition(b'\x00')[0].decode()
            # if len(s) < 1:
            #     print(_hexstr(data[offset:offset+self.ETH_GSTRING_LEN]))
            results.append(s)
        return results
    class _features_get_block(StructTemplate,
            namedtuple("_features_get_block", 
                "available requested active unchanged")):
        struct = Struct("4I")
    class _features_set_block(StructTemplate,
            namedtuple("_features_set_block", "valid requested")):
        struct = Struct("2I")
    def _features_get(self, strings=None): 
        # type: (list[str]) -> dict[str, bool]
        results = {}
        if strings is None:
            strings = self._strings_get(self.ETH_SS_FEATURES)
        blocks = int(math.ceil(len(strings) / 32.0))
        ssize = self._features_get_block.struct.size
        data = bytearray(pack('2I', self.ETHTOOL_GFEATURES, blocks))
        data.extend(bytearray(ssize * blocks))
        resp = self._ioctl(data)
        length = unpack('2I', resp[:8])[1]
        del resp[:8]
        for i in range(length):
            offset = ssize * i
            value = self._features_get_block.unpack(resp[offset:offset+ssize])
            for j in range(32):
                index = (i * 32) + j
                if index >= len(strings):
                    break
                if len(strings[index]):
                    results[strings[index]] = True if value.active & (1 << j) else False
        return results
    def _features_set(self, modify, strings=None): 
        # type: (dict[str, bool], list[str]) -> int
        if strings is None:
            strings = self._strings_get(self.ETH_SS_FEATURES)
        blocks = int(math.ceil(len(strings) / 32.0))
        mask = array('I', [0] * blocks)
        value = array('I', [0] * blocks)
        for n, v in modify.items():
            if len(n) < 1 or n not in strings:
                raise Exception("invalid feature: %r" % n)
            index = strings.index(n)
            bmask = 1 << (index % 32)
            index = int(index / 32)
            mask[index] = mask[index] | bmask
            if v:
                value[index] = value[index] | bmask
            else:
                value[index] = value[index] & ~bmask
        data = bytearray(pack('2I', self.ETHTOOL_SFEATURES, blocks))
        for i in range(blocks):
            data.extend(self._features_set_block(mask[i], value[i]).pack())
        return self._ioctl(data)
    def features(self, modify=None): # type: (dict[str, bool]) -> dict[str, bool]
        strings = self._strings_get(self.ETH_SS_FEATURES)
        if modify and len(modify):
            self._features_set(modify, strings)
            if self.log:
                for n, v in modify.items():
                    self.log.write("+ ethtool --features %s %s %s\n" % (self.ifname, n, 'on' if v else 'off'))
        return self._features_get(strings)
    def _flags_get(self, strings=None): # type: (list[str]) -> dict[str, bool]
        results = {}
        if strings is None:
            strings = self._strings_get(self.ETH_SS_PRIV_FLAGS)
        data = bytearray(pack('II', self.ETHTOOL_GPFLAGS, 0))
        resp = self._ioctl(data)
        flags = unpack('I', resp[4:])[0]
        for i in range(32):
            if i >= len(strings):
                break
            if len(strings[i]):
                results[strings[i]] = True if flags & (1 << i) else False        
        return results
    def _flags_set(self, modify, strings=None): 
        # type: (dict[str, bool], list[str]) -> None
        if strings is None:
            strings = self._strings_get(self.ETH_SS_PRIV_FLAGS)
        data = bytearray(pack('II', self.ETHTOOL_GPFLAGS, 0))
        resp = self._ioctl(data)
        flags = unpack('I', resp[4:])[0]
        for n, v in modify.items():
            if len(n) < 1 or n not in strings:
                    raise Exception("invalid private flag: %r" % n)
            index = strings.index(n)
            bmask = 1 << (index % 32)
            if v:
                flags = flags | bmask
            else:
                flags = flags & ~bmask            
        data = bytearray(pack('II', self.ETHTOOL_SPFLAGS, flags))
        self._ioctl(data)
    def flags(self, modify=None): 
        # type: (dict[str, bool]) -> dict[str, bool]
        strings = self._strings_get(self.ETH_SS_PRIV_FLAGS)
        if modify and len(modify):
            self._flags_set(modify, strings)
            if self.log:
                for n, v in modify.items():
                    self.log.write("+ ethtool --set-priv-flags %s %s %s\n" % (self.ifname, n, 'on' if v else 'off'))
        return self._flags_get(strings)
    def _queue_mask(self, queues): # type (set[int]) -> bytearray
        mask = array('I', [0] * int(self.QUEUE_MASK_SIZE / 4))
        for index in queues:
            if index > self.MAX_NUM_QUEUE:
                raise Exception(
                    "queue index cannot be more than %d" % self.MAX_NUM_QUEUE - 1
                )
            bmask = 1 << (index % 32)
            index = int(index / 32)
            mask[index] = mask[index] | bmask
        return bytearray(mask)
    class _coalesce_params(StructTemplate,
            namedtuple("_coalesce_params", 
                "rx_usecs rx_frames rx_usecs_irq rx_frames_irq"
                " tx_usecs tx_frames tx_usecs_irq tx_frames_irq"
                " stats_usecs adaptive_rx adaptive_tx rate_low"
                " rx_usecs_low rx_frames_low tx_usecs_low tx_frames_low"
                " rate_high rx_usecs_high rx_frames_high tx_usecs_high"
                " tx_frames_high rate_interval")):
        struct = Struct("22I")
    def _coalecse_get(self): 
        # type: () -> Ethtool._coalesce_params
        data = bytearray(pack('I', self.ETHTOOL_GCOALESCE))
        data.extend(bytearray(self._coalesce_params.struct.size))
        resp = self._ioctl(data)[4:]
        return self._coalesce_params.unpack(resp)
    def _coalecse_set(self, params): 
        # type: (Ethtool._coalesce_params) -> None
        data = bytearray(pack('I', self.ETHTOOL_SCOALESCE))
        data.extend(params.pack())
        self._ioctl(data)
    def coalesce(self, params=None):
        # type: (Ethtool._coalesce_params) -> Ethtool._coalesce_params
        if params is not None:
            self._coalecse_set(params)
            if self.log:
                params = params._asdict()
                for n in ['adaptive_rx', 'rx_usecs', 'adaptive_tx', 'tx_usecs']:
                    v = params[n]
                    if isinstance(v, bool):
                        v = 'on' if v else 'off'
                    self.log.write("+ ethtool --coalesce %s %s %s\n" % 
                        (self.ifname, n.replace('_', '-'), v))
        return self._coalecse_get()
    def _coalesce_queues_get(self, queues):
        # type: (set[int]) -> list[Ethtool._coalesce_params]
        ssize = self._coalesce_params.struct.size
        data = bytearray(
            pack('2I', self.ETHTOOL_PERQUEUE, self.ETHTOOL_GCOALESCE)
        )
        data.extend(self._queue_mask(queues))
        for _ in range(len(queues)):
            data.extend(pack('I', self.ETHTOOL_GCOALESCE))
            data.extend(bytearray(ssize))
        resp = self._ioctl(data)[8 + self.QUEUE_MASK_SIZE:]
        results = []
        for i in range(len(queues)):
            results.append(
                self._coalesce_params.unpack(resp[((4 + ssize) * i) + 4:])
            )
        return results
    def _coalecse_queues_set(self, queues, params):
        # type: (set[int], list[Ethtool._coalesce_params]) -> None
        data= bytearray(
            pack('2I', self.ETHTOOL_PERQUEUE, self.ETHTOOL_SCOALESCE)
        )
        data.extend(self._queue_mask(queues))
        for i in range(len(queues)):
            data.extend(pack('I', self.ETHTOOL_SCOALESCE))
            data.extend(params[i].pack())
        self._ioctl(data)
    def coalesce_queues(self, queues, params=None):
        # type: (set[int], list[Ethtool._coalesce_params]) -> list[Ethtool._coalesce_params]
        if params is not None:
            self._coalecse_queues_set(queues, params)
            if self.log:
                params = params[0]._asdict()
                for n in ['adaptive_rx', 'rx_usecs', 'adaptive_tx', 'tx_usecs']:
                    v = params[n]
                    if isinstance(v, bool):
                        v = 'on' if v else 'off'
                    mask = self._queue_mask(queues)
                    mask.reverse()
                    mask = _hexstr(mask).lstrip('0')
                    self.log.write(
                        "+ ethtool --per-queue %s queue_mask 0x%s --coalesce %s %s\n" % 
                        (self.ifname, mask, n.replace('_', '-'), v)
                    )
        return self._coalesce_queues_get(queues)
    class _ring_params(StructTemplate,
            namedtuple("_ring_params", 
                "rx_max rx_mini_max rx_jumbo_max tx_max"
                " rx rx_mini rx_jumbo tx")):
        struct = Struct("8I")
    def _rings_get(self): # type: () -> Ethtool._ring_params
        data = bytearray(pack('I', self.ETHTOOL_GRINGPARAM))
        data.extend(bytearray(self._ring_params.struct.size))
        resp = self._ioctl(data)
        return self._ring_params.unpack(resp[4:])
    def _rings_set(self, params): # type: (Ethtool._ring_params) -> None
        data = bytearray(pack('I', self.ETHTOOL_SRINGPARAM))
        data.extend(bytearray(params.pack()))
        self._ioctl(data)
    def rings(self, params=None):
        # type: (Ethtool._ring_params) -> Ethtool._ring_params
        if params is not None:
            rings = self._rings_get()
            if params.rx > rings.rx_max:
                params = params._replace(rx=rings.rx_max)
            if params.tx > rings.tx_max:
                params = params._replace(rx=rings.tx_max)
            self._rings_set(params)
            if self.log:
                self.log.write("+ ethtool --set-ring %s rx %d tx %d\n" % 
                    (self.ifname, params.rx, params.tx))
        return self._rings_get()
    def ntuples(self, modify=None):
        # type: (list[dict[str, int]]) -> list[dict[str, int]]
        if modify and len(modify):
            for n in modify:
                _ethtool(
                    self.ifname, "config-ntuple", 
                    "flow-type", n["flow-type"], 
                    "dst-port", str(n["dst-port"]), 
                    "action", str(n["action"]), log=self.log
                )
        output = _ethtool(self.ifname, "show-ntuple")
        results = []
        for m in re.findall('Filter: (\d+)\s+Rule Type: (\w+) over IPv(\d)[\s\S]+?'
                'Dest port: (\d+)[\s\S]+?Action: Direct to queue (\d+)',
                output, re.MULTILINE):
            results.append({
                "id": int(m[0]), 
                "flow-type": m[1].lower() + m[2],
                "dst-port": int(m[3]),
                "action": int(m[4])
            })
        return results
    class _channels_params(StructTemplate,
            namedtuple("_channel_params", 
                "max_rx max_tx max_other max_combined"
                " rx tx other combined")):
        struct = Struct("8I")
    def _channels_get(self): 
        # type: () -> Ethtool._channels_params
        data = bytearray(pack('I', self.ETHTOOL_GCHANNELS))
        data.extend(bytearray(self._channels_params.struct.size))
        resp = self._ioctl(data)
        return self._channels_params.unpack(resp[4:])
    def _channels_set(self, params): 
        # type: (Ethtool._channels_params) -> None
        data = bytearray(pack('I', self.ETHTOOL_SCHANNELS))
        data.extend(bytearray(params.pack()))
        self._ioctl(data)
    def channels(self, params=None): 
        # type: (Ethtool._channels_params) -> Ethtool._channels_params
        if params is not None:
            channels = self._channels_get()
            if params.combined > channels.max_combined:
                params = params._replace(combined=channels.max_combined)
            if params.rx > channels.max_rx:
                params = params._replace(rx=channels.max_rx)
            if params.tx > channels.max_tx:
                params = params._replace(tx=channels.max_tx)
            self._channels_set(params)
        return self._channels_get()
    def stats(self): # type: () -> dict[str, int]
        strings = self._strings_get(self.ETH_SS_STATS)
        results = {}
        data = bytearray(pack("II", self.ETHTOOL_GSTATS, len(strings)))
        data.extend(pack('Q', 0) * len(strings))
        resp = self._ioctl(data)[8:]
        for i in range(len(strings)):
            offset = 8 * i
            value = unpack('Q', resp[offset:offset+8])[0]
            results[strings[i]] = value
        return results

class NLAttr(object):
    ## include/uapi/linux/netlink.h
    NLA_F_NESTED        = (1 << 15)
    NLA_F_NET_BYTEORDER = (1 << 14)
    NLA_TYPE_MASK       = ~(NLA_F_NESTED | NLA_F_NET_BYTEORDER)
    NL_ATTR_TYPE_INVALID      = 0
    NL_ATTR_TYPE_FLAG         = 1
    NL_ATTR_TYPE_U8           = 2
    NL_ATTR_TYPE_U16          = 3
    NL_ATTR_TYPE_U32          = 4
    NL_ATTR_TYPE_U64          = 5
    NL_ATTR_TYPE_S8           = 6
    NL_ATTR_TYPE_S16          = 7
    NL_ATTR_TYPE_S32          = 8
    NL_ATTR_TYPE_S64          = 9
    NL_ATTR_TYPE_BINARY       = 10
    NL_ATTR_TYPE_STRING       = 11
    NL_ATTR_TYPE_NUL_STRING   = 12
    NL_ATTR_TYPE_NESTED       = 13
    NL_ATTR_TYPE_NESTED_ARRAY = 14
    NL_ATTR_TYPE_BITFIELD32   = 15
    # struct nlattr {
    #     __u16           nla_len;
    #     __u16           nla_type;
    # };
    _hdr = Struct("HH")
    def __init__(self, type, data=None): # type: (int, bytes) -> None
        self.type = type
        self.data = data
    @classmethod
    def unpack(cls, data): # type: (bytes) -> NLAttr
        length, type = cls._hdr.unpack(data[:cls._hdr.size])
        payload = None
        if len(data) >= length:
            payload = data[cls._hdr.size:length]
        return cls(type, payload)
    @staticmethod    
    def _align(len, bs=4): # type: (int, int) -> int
        return (len + bs - 1) & ~(bs - 1)
    @property
    def size(self):
        return self._hdr.size + len(self.data)
    def __len__(self):
        return self._align(self.size)
    def __str__(self):
        return (
            "NLAttr(len=%d, type=%d, data='%s')" %
            (self.size, self.type, _hexstr(self.data) if self.data else "None")
        )
    def _pack_header(self): # type: () -> bytes
        return self._hdr.pack(self.size, self.type)
    def pack(self): # type() -> bytes
        fill = bytes(b'\x00' * (len(self) - self.size))
        return self._pack_header() + self.data + fill

class RTAttr(object):
    ## include/uapi/linux/netlink.h
    # Types
    NL_ATTR_TYPE_INVALID      = 0
    NL_ATTR_TYPE_FLAG         = 1
    NL_ATTR_TYPE_U8           = 2
    NL_ATTR_TYPE_U16          = 3
    NL_ATTR_TYPE_U32          = 4
    NL_ATTR_TYPE_U64          = 5
    NL_ATTR_TYPE_S8           = 6
    NL_ATTR_TYPE_S16          = 7
    NL_ATTR_TYPE_S32          = 8
    NL_ATTR_TYPE_S64          = 9
    NL_ATTR_TYPE_BINARY       = 10
    NL_ATTR_TYPE_STRING       = 11
    NL_ATTR_TYPE_NUL_STRING   = 12
    NL_ATTR_TYPE_NESTED       = 13
    NL_ATTR_TYPE_NESTED_ARRAY = 14
    NL_ATTR_TYPE_BITFIELD32   = 15
    # struct rtattr {
    # 	unsigned short	rta_len;
    # 	unsigned short	rta_type;
    #   /* Data follows */
    # };
    _hdr = Struct("HH")
    def __init__(self, type, data=None): # type: (int, bytes) -> None
        self.type = type
        self.data = data
    @classmethod
    def unpack(cls, data): # type: (bytes) -> RTAttr
        length, type = cls._hdr.unpack(data[:cls._hdr.size])
        payload = None
        if len(data) >= length:
            payload = data[cls._hdr.size:length]
        return cls(type, payload)
    @staticmethod
    def _align(len, bs=4): # type: (int, int) -> int
        return (len + bs - 1) & ~(bs - 1)
    @property
    def size(self):
        return self._hdr.size + len(self.data)
    def __len__(self):
        return self._align(self.size)
    def __str__(self):
        return (
            "RTAttr(len=%d, type=%d, data='%s')" %
            (self.size, self.type, _hexstr(self.data) if self.data else "None")
        )
    def _pack_header(self): # type: () -> bytes
        return self._hdr.pack(self.size, self.type)
    def pack(self): # type() -> bytes
        fill = bytes(b'\x00' * (len(self) - self.size))
        return self._pack_header() + self.data + fill

class NLMessage(object):
    ## include/uapi/linux/netlink.h
    # Types
    NLMSG_NOOP     = 0x1 
    NLMSG_ERROR    = 0x2 
    NLMSG_DONE     = 0x3 
    NLMSG_OVERRUN  = 0x4 
    NLMSG_MIN_TYPE = 0x10
    # Error attrs
    NLMSGERR_ATTR_UNUSED = 0
    NLMSGERR_ATTR_MSG    = 1
    NLMSGERR_ATTR_OFFS   = 2
    NLMSGERR_ATTR_COOKIE = 3
    NLMSGERR_ATTR_POLICY = 4
    # Flags values
    NLM_F_REQUEST       = 0x01 
    NLM_F_MULTI         = 0x02 
    NLM_F_ACK           = 0x04 
    NLM_F_ECHO          = 0x08
    NLM_F_DUMP_INTR     = 0x10 # Dump was inconsistent due to sequence change
    NLM_F_DUMP_FILTERED	= 0x20 # Dump was filtered as requested
    # Modifiers to GET request
    NLM_F_ROOT   = 0x100
    NLM_F_MATCH  = 0x200
    NLM_F_DUMP   = 0x300
    NLM_F_ATOMIC = 0x400
    # Modifiers to NEW request
    NLM_F_REPLACE = 0x100   # Override existing
    NLM_F_EXCL    = 0x200   # Do not touch, if it exists
    NLM_F_CREATE  = 0x400   # Create, if it does not exist
    NLM_F_APPEND  = 0x800   # Add to end of list
    ## include/uapi/linux/rtnetlink.h
    # Routing messages
    RTM_BASE         = 16
    RTM_NEWLINK      = 16
    RTM_DELLINK      = 17
    RTM_GETLINK      = 18
    RTM_SETLINK      = 19
    RTM_NEWADDR      = 20
    RTM_DELADDR      = 21
    RTM_GETADDR      = 22
    RTM_NEWROUTE     = 24
    RTM_DELROUTE     = 25
    RTM_GETROUTE     = 26
    RTM_NEWNEIGH     = 28
    RTM_DELNEIGH     = 29
    RTM_GETNEIGH     = 30
    RTM_NEWRULE      = 32
    RTM_DELRULE      = 33
    RTM_GETRULE      = 34
    RTM_NEWQDISC     = 36
    RTM_DELQDISC     = 37
    RTM_GETQDISC     = 38
    RTM_NEWTCLASS    = 40
    RTM_DELTCLASS    = 41
    RTM_GETTCLASS    = 42
    RTM_NEWTFILTER   = 44
    RTM_DELTFILTER   = 45
    RTM_GETTFILTER   = 46
    RTM_NEWACTION    = 48
    RTM_DELACTION    = 49
    RTM_GETACTION    = 50
    RTM_NEWPREFIX    = 52
    RTM_GETMULTICAST = 58
    RTM_GETANYCAST   = 62
    RTM_NEWNEIGHTBL  = 64
    RTM_GETNEIGHTBL  = 66
    RTM_SETNEIGHTBL  = 67
    RTM_NEWNDUSEROPT = 68
    RTM_NEWADDRLABEL = 72
    RTM_DELADDRLABEL = 73
    RTM_GETADDRLABEL = 74
    RTM_GETDCB       = 78
    RTM_SETDCB       = 77
    RT_TABLE_MAIN    = 254
    # struct nlmsghdr {
    #     __u32 nlmsg_len;    /* Length of message including header. */
    #     __u16 nlmsg_type;   /* Type of message content. */
    #     __u16 nlmsg_flags;  /* Additional flags. */
    #     __u32 nlmsg_seq;    /* Sequence number. */
    #     __u32 nlmsg_pid;    /* PID of the sending process. */
    # };
    _hdr = Struct("IHHII")
    def __init__(self, type, flags=0, seq=-1, data=None): 
        # type: (int, int, int, bytes) -> None
        self.type = type
        self.flags = flags
        self.seq = seq
        self.pid = 0
        self.data = data
    @classmethod
    def unpack(cls, data): # type: (bytes) -> NLMessage
        length, type, flags, seq, _ = cls._hdr.unpack(data[:cls._hdr.size])
        payload = None
        if len(data) >= length:
            payload = data[cls._hdr.size:length]
        return cls(type, flags, seq, payload)
    @staticmethod
    def _align(len, bs=4): # type: (int, int) -> int
        return (len + bs - 1) & ~(bs - 1)
    def __len__(self):
        return self._align(self._hdr.size + len(self.data))
    def __str__(self):
        return ("NLMessage(len=%d, type=%d, flags=0x%04X, seq=%d, pid=%d)" %
            (len(self), self.type, self.flags, self.seq, self.pid))
    def _pack_header(self): # type: () -> bytes
        return self._hdr.pack(len(self), self.type, self.flags, self.seq, 0)
    def pack(self): # type() -> bytes
        return self._pack_header() + self.data

class NLConn(object):
    ## include/uapi/linux/netlink.h
    NETLINK_ROUTE   = 0 # ip/tc
    NETLINK_GENERIC = 16 # ethtool/devlink
    ## include/uapi/linux/genetlink.h
    GENL_ADMIN_PERM     = 0x01
    GENL_CMD_CAP_DO     = 0x02
    GENL_CMD_CAP_DUMP   = 0x04
    GENL_CMD_CAP_HASPOL = 0x08
    GENL_UNS_ADMIN_PERM = 0x10
    GENL_ID_CTRL      = NLMessage.NLMSG_MIN_TYPE
    GENL_ID_VFS_DQUOT = (NLMessage.NLMSG_MIN_TYPE + 1)
    GENL_ID_PMCRAID   = (NLMessage.NLMSG_MIN_TYPE + 2)
    # /* must be last reserved + 1 */
    GENL_START_ALLOC  = (NLMessage.NLMSG_MIN_TYPE + 3)
    CTRL_CMD_UNSPEC       = 0
    CTRL_CMD_NEWFAMILY    = 1
    CTRL_CMD_DELFAMILY    = 2
    CTRL_CMD_GETFAMILY    = 3
    CTRL_CMD_NEWOPS       = 4
    CTRL_CMD_DELOPS       = 5
    CTRL_CMD_GETOPS       = 6
    CTRL_CMD_NEWMCAST_GRP = 7
    CTRL_CMD_DELMCAST_GRP = 8
    CTRL_CMD_GETMCAST_GRP = 9 # /* unused */
    CTRL_CMD_GETPOLICY    = 10
    CTRL_ATTR_FAMILY_ID    = 1
    CTRL_ATTR_FAMILY_NAME  = 2
    CTRL_ATTR_VERSION      = 3
    CTRL_ATTR_HDRSIZE      = 4
    CTRL_ATTR_MAXATTR      = 5
    CTRL_ATTR_OPS          = 6
    CTRL_ATTR_MCAST_GROUPS = 7
    CTRL_ATTR_POLICY       = 8
    CTRL_ATTR_OP_POLICY    = 9
    CTRL_ATTR_OP           = 10
    CTRL_ATTR_OP_ID    = 1
    CTRL_ATTR_OP_FLAGS = 2
    # struct genlmsghdr {
    #     __u8	cmd;
    #     __u8	version;
    #     __u16	reserved;
    # };
    class Genlmsghdr(StructTemplate,
            namedtuple("Genlmsghdr", "cmd version reserved")
            ):
        struct = Struct("BBH")
    def __init__(self, service=0, groups=0, bufsize=16384):
        # type: (int, int, int, bool) -> None
        self.socket = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, service)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, bufsize)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, bufsize)
        self.socket.bind((0, groups))
        self.bufsize = bufsize
        self.pid, self.groups = self.socket.getsockname()
        self._seq = 0
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.socket.close()
    def sendmsg(self, msg): # type: (NLMessage) -> None
        if isinstance(msg, NLMessage):
            if msg.seq == -1: 
                msg.seq = self.seq
            msg.pid = self.pid
            # print(msg)
            msg = msg.pack()
        self.socket.send(msg)
    def recvmsgs(self): # type: () -> list[NLMessage]
        data = self.socket.recv(int(self.bufsize / 2))
        msgs = []
        while len(data) >= 16:
            msg = NLMessage.unpack(data)
            if msg.type == NLMessage.NLMSG_ERROR:
                errno = -unpack("i", msg.data[:4])[0]
                if errno != 0:
                    err = OSError("Netlink error: %s (%d)" % 
                        (os.strerror(errno), errno))
                    err.errno = errno
                    raise err
            msgs.append(msg)
            data = data[len(msg):]
        return msgs
    def send(self, msg): # type: (NLMessage) -> list[NLMessage]
        self.sendmsg(msg)
        done = False
        msgs = []
        while not done:
            for m in self.recvmsgs():
                if m.type in [NLMessage.NLMSG_DONE, NLMessage.NLMSG_ERROR]:
                    done = True
                    break
                msgs.append(m)
        return msgs
    @property
    def seq(self):
        self._seq += 1
        return self._seq

class RNLConn(NLConn):
    def __init__(self, groups=0, bufsize=16384):
        super(RNLConn, self).__init__(NLConn.NETLINK_ROUTE, groups, bufsize)

class GNLConn(NLConn):
    def __init__(self, groups=0, bufsize=16384):
        super(GNLConn, self).__init__(NLConn.NETLINK_GENERIC, groups, bufsize)
    def genindex(self):
        results = {}
        msgs = self.send(NLMessage(
            type=self.GENL_ID_CTRL,
            flags=NLMessage.NLM_F_REQUEST | NLMessage.NLM_F_ROOT | NLMessage.NLM_F_MATCH,
            data=self.Genlmsghdr(
                cmd=self.CTRL_CMD_GETFAMILY,
                version=0,
                reserved=0
            ).pack()
        ))
        for m in msgs:
            if m.type != self.GENL_ID_CTRL:
                raise Exception("Not a controller message: " + str(m))
            msg = self.Genlmsghdr.unpack(m.data)
            name = None
            pos = msg.struct.size
            if msg.cmd != self.CTRL_CMD_NEWFAMILY:
                continue
            while pos < len(m.data):
                attr = NLAttr.unpack(m.data[pos:]) 
                pos += len(attr)
                # print(attr)
                if attr.type == self.CTRL_ATTR_FAMILY_NAME:
                    name = attr.data.decode().replace('\x00', '')
                elif attr.type == self.CTRL_ATTR_FAMILY_ID:
                    if name:
                        results[name] = unpack('H', attr.data)[0]
        return results

class IPtool(object):
    ## include/uapi/linux/if_link.h
    # Address Family attrs
    IFLA_ADDRESS   = 1
    IFLA_OPERSTATE = 16
    ## iproute2/ip/ipaddress.c
    # link states
    IFLA_OPERSTATES = [
        'UNKNOWN', 'NOTPRESENT', 'DOWN', 
        'LOWERLAYERDOWN', 'TESTING', 'DORMANT', 'UP'
        ]
    class IFAddrmsg(StructTemplate,
            namedtuple("IFAddrmsg", "family prefixlen flags scope index")
            ):
        struct = Struct("BBBBI")
    class IFInfomsg(StructTemplate,
            namedtuple("IFInfomsg", "family type index flags mask")
            ):
        struct = Struct("BHiII")        
    def __init__(self, ifname): # type: (str) -> None
        self.ifname = ifname
        self.ifindex = if_nametoindex(ifname)
    def addrs(self): # type: () -> list[str]
        addrs = []
        with RNLConn() as conn:
            msgs = conn.send(NLMessage(
                type=NLMessage.RTM_GETADDR,
                flags=NLMessage.NLM_F_REQUEST | NLMessage.NLM_F_DUMP,
                data=self.IFAddrmsg(socket.AF_INET, 0, 0, 0, 0).pack()
            ))
            for m in msgs:
                msg = self.IFAddrmsg.unpack(m.data)
                if msg.index != self.ifindex:
                    continue
                pos = msg.struct.size
                while pos < len(m.data):
                    attr = RTAttr.unpack(m.data[pos:]) 
                    pos += len(attr)
                    if attr.type == self.IFLA_ADDRESS:
                        addrs.append('{}.{}.{}.{}'.format(*bytearray(attr.data)))
                        break
        return addrs
    def link_state(self): # type () -> str
        with RNLConn() as conn:
            msgs = conn.send(NLMessage(
                type=NLMessage.RTM_GETLINK,
                flags=NLMessage.NLM_F_REQUEST | NLMessage.NLM_F_DUMP,
                data=self.IFInfomsg(socket.AF_UNSPEC, 0, 0, 0, 0).pack()
            ))
            for m in msgs:
                msg = self.IFInfomsg.unpack(m.data)
                if msg.index != self.ifindex:
                    continue
                pos = msg.struct.size
                while pos < len(m.data):
                    attr = RTAttr.unpack(m.data[pos:]) 
                    pos += len(attr)
                    if attr.type == self.IFLA_OPERSTATE:
                        return self.IFLA_OPERSTATES[unpack('B', attr.data)[0]]

        
class TCtool(object):
    ## include/uapi/linux/rtnetlink.h
    # TC (qdisc) attrs
    TCA_KIND    = 1
    TCA_OPTIONS = 2
    ## include/uapi/linux/pkt_sched.h
    # TC (qdisc mqprio) nested attrs
    TCA_MQPRIO_MODE   = 1
    TCA_MQPRIO_SHAPER = 2
    # TC Handles
    TC_H_ROOT    = 0xFFFFFFFF
    TC_H_INGRESS = 0xFFFFFFF1
    TC_H_CLSACT  = TC_H_INGRESS
    TC_H_MIN_PRIORITY = 0xFFE0
    TC_H_MIN_INGRESS  = 0xFFF2
    TC_H_MIN_EGRESS   = 0xFFF3
    TC_H_MAJ_MASK = 0xFFFF0000
    TC_H_MIN_MASK = 0x0000FFFF
    TC_MQPRIO_MODE_DCB     = 0
    TC_MQPRIO_MODE_CHANNEL = 1
    TC_MQPRIO_SHAPER_DCB     = 0
    TC_MQPRIO_SHAPER_BW_RATE = 1
    @classmethod
    def _tc_h_maj(cls, h): # type: (int) -> int
        #define TC_H_MAJ(h) ((h)&TC_H_MAJ_MASK)
        return h & cls.TC_H_MAJ_MASK
    @classmethod
    def _tc_h_min(cls, h): # type: (int) -> int
        #define TC_H_MIN(h) ((h)&TC_H_MIN_MASK)
        return h & cls.TC_H_MIN_MASK
    @classmethod
    def _tc_h_make(cls, maj, min): # type: (int, int) -> int
        #define TC_H_MAKE(maj,min) (((maj)&TC_H_MAJ_MASK)|((min)&TC_H_MIN_MASK))
        return cls._tc_h_maj(maj) | cls._tc_h_min(min)
    class TCmsg(StructTemplate,
            namedtuple("TCmsg", "family index handle parent info")
            ):
        struct = Struct("B3xiIII")
    TC_QOPT_MAX_QUEUE = 16
    Clsact = namedtuple("Qdisc", "parent kind")
    Qdisc = namedtuple("Qdisc", "parent kind num_tc map hw count offset mode shaper")
    Filter = namedtuple("Filter", "prio proto src_addr src_port dst_addr dst_port")
    def __init__(self, ifname, log=None): # type: (str, any) -> None
        self.ifname = ifname
        self.ifindex = if_nametoindex(ifname)
        self.log = log
    def qdisc_list(self):
        # type: () -> list[Qdisc|Clsact]
        with RNLConn() as conn:
            msgs = conn.send(NLMessage(
                type=NLMessage.RTM_GETQDISC,
                flags=NLMessage.NLM_F_REQUEST | NLMessage.NLM_F_DUMP,
                data=self.TCmsg(socket.AF_UNSPEC, self.ifindex, 0, 0, 0).pack()
            ))
            results = []
            for m in msgs:
                if m.type == NLMessage.RTM_NEWQDISC:
                    msg = self.TCmsg.unpack(m.data)
                    if msg.index == self.ifindex:
                        kind = ''
                        pos = msg.struct.size
                        while pos < len(m.data):
                            attr = NLAttr.unpack(m.data[pos:])
                            pos += len(attr)
                            if attr.type == self.TCA_KIND:
                                kind = attr.data.partition(b'\x00')[0].decode()
                                if kind not in ['mqprio', 'clsact']:
                                    break
                            elif attr.type == self.TCA_OPTIONS:
                                # print(attr)
                                # hexdump(m.data)
                                if kind == 'mqprio':
                                    num_tc = unpack("B", attr.data[0:1])[0]
                                    pmap = unpack("16B", attr.data[1:17])
                                    hw = unpack("B", attr.data[17:18])[0]
                                    count = unpack("16H", attr.data[18:50])
                                    offset = unpack("16H", attr.data[50:82])
                                    mode = 0
                                    shaper = 0
                                    if len(attr.data) > 84:
                                        rtattr = NLAttr.unpack(attr.data[84:])
                                        if rtattr.type == self.TCA_MQPRIO_MODE:
                                            mode = unpack("H", rtattr.data)[0]
                                        if rtattr.type == self.TCA_MQPRIO_SHAPER:
                                            shaper = unpack("H", rtattr.data)[0]
                                    results.append(self.Qdisc(
                                        msg.parent, kind, num_tc, pmap, hw, 
                                        count, offset, mode, shaper
                                    ))
                                    break
                                elif kind == 'clsact':
                                    results.append(self.Clsact(msg.parent, kind))
                                    break
                            else:
                                print(attr)
            return results
    def qdisc_add(self, parent=None, kind=None, pmap=None, count=None, offset=None):
        # type: (int, str, list[int], list[int], list[int]) -> None
        with RNLConn() as conn:
            handle = 0
            if parent == self.TC_H_CLSACT:
                handle = self._tc_h_make(parent, 0)
            msg = NLMessage(
                type=NLMessage.RTM_NEWQDISC,
                flags=NLMessage.NLM_F_REQUEST | NLMessage.NLM_F_ACK | 
                    NLMessage.NLM_F_CREATE | NLMessage.NLM_F_EXCL,
                data=self.TCmsg(socket.AF_UNSPEC, self.ifindex, handle, parent, 0).pack()
            )
            msg.data = msg.data + NLAttr(self.TCA_KIND, kind.encode() + b'\x00').pack()
            if kind == 'mqprio':
                # normalize maps and limit to 16 TCs
                max_tc = self.TC_QOPT_MAX_QUEUE
                pmap = pmap[:max_tc]
                count = count[:len(pmap)]
                offset = offset[:len(pmap)]
                # nested attrs
                msg.data = msg.data + NLAttr(
                    self.TCA_OPTIONS, 
                    pack("B", len(pmap)) + _pack_list(pmap, 'B', max_tc) + pack("B", 1) +
                    _pack_list(count, 'H', max_tc) + _pack_list(offset, 'H', max_tc) + 
                    b'\x00' * 2 + # DWORD alignment padding
                    NLAttr(
                        self.TCA_MQPRIO_MODE, 
                        pack("H", self.TC_MQPRIO_MODE_CHANNEL)
                    ).pack()
                ).pack()
            # print(msg)
            # hexdump(msg.data)
            conn.send(msg)
            if self.log:
                if parent == self.TC_H_ROOT and kind == "mqprio":
                    self.log.write(
                        "+ tc qdisc add dev %s root mqprio" \
                        " num_tc %d map %s queues %s hw 1 mode channel\n" %
                        (self.ifname, len(pmap), ' '.join([str(p) for p in pmap]), 
                            ' '.join([str(count[i])+'@'+str(offset[i]) for i in range(len(pmap))]))
                    )
                elif parent == self.TC_H_CLSACT and kind == "clsact":
                    self.log.write("+ tc qdisc add dev %s clsact\n" % (self.ifname))
    def qdisc_del(self, parent=None, kind=None):
        # type: (int, str) -> None
        with RNLConn() as conn:
            handle = 0
            if parent == self.TC_H_CLSACT:
                handle = self._tc_h_make(parent, 0)
            msg = NLMessage(
                type=NLMessage.RTM_DELQDISC,
                flags=NLMessage.NLM_F_REQUEST,
                data=self.TCmsg(socket.AF_UNSPEC, self.ifindex, handle, parent, 0).pack()
            )
            msg.data = msg.data + NLAttr(self.TCA_KIND, kind.encode() + b'\x00').pack()
            # print(msg)
            # hexdump(msg.data)
            conn.sendmsg(msg)
            if self.log:
                if parent == self.TC_H_ROOT:
                    self.log.write("+ tc qdisc del dev %s root %s\n" % (self.ifname, kind))
                elif parent == self.TC_H_CLSACT and kind == "clsact":
                    self.log.write("+ tc qdisc del dev %s clsact\n" % (self.ifname))
    def filter_list(self):
        # type: () -> list[Filter]
        pass
    def filter_add(self, direction='ingress', prio=1, proto='tcp', 
            src_addr=None, src_port=None, dst_addr=None, dst_port=None, 
            tc=None, action=None, priority=None):
        # type: (str, int, str, str, int, str, int, int, str, int) -> None
        params = ['add', direction, 'prio', str(prio),
            'protocol', 'ip', 'flower', 'ip_proto', proto]
        if src_addr is not None:
            params.extend(['src_ip', src_addr])
        if src_port is not None:
            params.extend(['src_port', str(src_port)])
        if dst_addr is not None:
            params.extend(['dst_ip', dst_addr])
        if dst_port is not None:
            params.extend(['dst_port', str(dst_port)])
        if tc is not None:
            params.extend(['skip_sw', 'hw_tc', str(tc)])
        else:
            if action is not None:
                params.extend(['action', action])
            if priority is not None:
                params.extend(['priority', str(priority)])
        _tc(self.ifname, 'filter', *params, log=self.log)
    def filter_del(self, direction='ingress'):
        # type: (str) -> None
        _tc(self.ifname, 'filter', 'del', direction, check=True, log=self.log)

## helper classes

class Inventory(object):
    def __init__(self):
        '''
        A target system inventory as a class
        '''
        self.devs = {}
        self.cpus = None
        self.cpus_online = None
        self.numa_cpus = None
        self.numa_nodes = None
        self.refresh()

    def refresh(self):
        '''
        Refresh the system inventopry
        '''
        self._get_cpus()
        self._get_devs()

    @staticmethod
    def _int_list(s): # type: (str) -> list
        '''
        Parse a comma-seperated list of integers with ranges
        '''
        l = []
        for v in str(s).split(','):
            v = v.strip()
            if '-' in v:
                # element is an x-y range
                x, y = v.split('-')
                for i in range(int(x), int(y) + 1):
                    l.append(i)
            else:
                l.append(int(v))
        # remove duplicates and sort 
        return sorted(set(l))

    def _get_cpus(self):
        # cpu topology
        lscpu = _exec(["lscpu"])
        m = re.search(r'^CPU\(s\):\s+(\d+)$', lscpu, re.MULTILINE)
        if not m:
            raise Exception("Unable to determine number of CPUs")
        self.cpus = int(m.group(1))
        m = re.search(r'^On-line CPU\(s\) list:\s+([\d,-]+)$', lscpu, re.MULTILINE)
        if not m:
            raise Exception("Unable to on-line CPUs")
        self.cpus_online = self._int_list(m.group(1))
        # cores for each numa node
        self.numa_cpus = []
        for m in re.finditer("^NUMA node(\d+) CPU\(s\):\s+([\d\-,]+)", 
                lscpu, re.MULTILINE):
            self.numa_cpus.append(self._int_list(m.group(2)))
        self.numa_nodes = len(self.numa_cpus)
        if not self.numa_nodes:
            raise Exception("Unable to determine numa topology")

    def _get_devs(self):
        # create list of all network devices
        devs = os.listdir('/sys/class/net/')
        self.devs = {}
        for dev in devs:
            try:
                # query device entry for user events
                info = _uevent(dev)
                # check device for ice driver
                if info['driver'] == 'ice':
                    # get device numa node
                    path = os.path.join(*[
                        '/sys', 'class', 'net', dev, 'device', 'numa_node'
                    ])
                    info['numa_node'] = int(_readfile(path))    
                    self.devs[dev] = info
            except:
                pass


class Settings(object):

    def __init__(self, dev, log=None): # type: (str, any) -> None
        self.dev = dev
        self.log = log
        self.tc_offload = None
        self.ntuple_filters = None
        self.flow_director = None
        self._channel_pkt = None
        self.inspect_optimize = None
        self.bp_stop = None
        self.bp_stop_cfg = None
        self.busy_poll = None
        self.busy_read = None
        self.arp_announce = None
        self.arp_ignore = None
        self.arp_notify = None
        self.ethtool = Ethtool(dev, self.log)    
        self.refresh()

    def __str__(self): # type: () -> str
        attrs = [
            'tc_offload',
            'ntuple_filters',
            'flow_director',
            'inspect_optimize',
            'bp_stop',
            'bp_stop_cfg',
            'busy_poll',
            'busy_read',
            'arp_announce',
            'arp_ignore',
            'arp_notify'
        ]
        output = []
        for a in attrs:
            output.append("%s: %r" % (a, getattr(self, a)))
        return '\n'.join(output)

    def refresh(self):
        # get network sysctls
        sysctls = _sysctl('net')
        # store in class attributes
        self.busy_poll = int(sysctls['core.busy_poll'])
        self.busy_read = int(sysctls['core.busy_read'])
        self.arp_announce = int(sysctls['ipv4.conf.' + self.dev + '.arp_announce'])
        self.arp_ignore = int(sysctls['ipv4.conf.' + self.dev + '.arp_ignore'])
        self.arp_notify = int(sysctls['ipv4.conf.' + self.dev + '.arp_notify'])
        # get device features
        features = self.ethtool.features()
        # store in class attributes
        self.tc_offload = True if features['hw-tc-offload'] == 'on' else False
        self.ntuple_filters = True if features['rx-ntuple-filter'] == 'on' else False
        # get device private flags
        flags = self.ethtool.flags()
        # store in class attributes
        key = 'channel-inline-flow-director'
        if key in flags:
            self.flow_director = True if flags[key] == 'on' else False
        self._channel_pkt = 'channel-pkt' \
            if any(['channel-pkt' in key for key in flags]) else 'channel-packet'
        key = self._channel_pkt + '-inspect-optimize'
        if key in flags:
            self.inspect_optimize = True if flags[key] == 'on' else False
        key = self._channel_pkt + '-clean-bp-stop'
        if key in flags:
            self.bp_stop = True if flags[key] == 'on' else False
        key = self._channel_pkt + '-clean-bp-stop-cfg'
        if key in flags:
            self.bp_stop_cfg = True if flags[key] == 'on' else False

    def apply(self):
        # apply network sysctls
        if self.log:
            self.log.write("## network sysctls ##\n")
        if self.busy_poll is not None:
            _sysctl('net.core.busy_poll', str(self.busy_poll), log=self.log)
        if self.busy_read is not None:
            _sysctl('net.core.busy_read', str(self.busy_read), log=self.log)
        if self.arp_announce is not None:
            _sysctl(
                'net.ipv4.conf.' + self.dev + '.arp_announce', 
                str(self.arp_announce), 
                log=self.log
            )
        if self.arp_ignore is not None:
            _sysctl(
                'net.ipv4.conf.' + self.dev + '.arp_ignore', 
                str(self.arp_ignore), 
                log=self.log
            )
        if self.arp_notify is not None:
            _sysctl(
                'net.ipv4.conf.' + self.dev + '.arp_notify', 
                str(self.arp_notify), 
                log=self.log
            )
        # apply device features
        if self.log:
            self.log.write("## device features ##\n")
        features = {}
        if self.tc_offload is not None:
            features['hw-tc-offload'] = self.tc_offload
        if self.ntuple_filters is not None:
            features['rx-ntuple-filter'] = self.ntuple_filters
        self.ethtool.features(features)
        # apply device private flags
        if self.log:
            self.log.write("## device private flags ##\n")
        flags = {}
        if self.flow_director is not None:
            flags['channel-inline-flow-director'] = self.flow_director
        if self.inspect_optimize is not None:
            flags[self._channel_pkt + '-inspect-optimize'] = self.inspect_optimize
        if self.bp_stop is not None:
            flags[self._channel_pkt + '-clean-bp-stop'] = self.bp_stop
        if self.bp_stop_cfg is not None:
            flags[self._channel_pkt + '-clean-bp-stop-cfg'] = self.bp_stop_cfg
        self.ethtool.flags(flags)        

## config classes

class ConfigBase(object):
    
    # a dictionary of callables that defines
    # the schema of the config section
    _schema = {}

    ## custom schema formats
    @staticmethod
    def _bool(s):
        '''
        Parse a <bool> on/off flag 
        '''
        try:
            s = str(s).lower()
            if s in ['on', 'true', 'yes', '1']:
                return True
            elif s in ['off', 'false', 'no', '0', None]:
                return False
            else:
                raise Exception()
        except:
            raise Exception("%r is not a valid boolean" % s)

    @staticmethod
    def _int_list(s): # type (str) -> list
        '''
        Parse a comma-seperated list of integers with ranges
        '''
        l = []
        for v in str(s).split(','):
            v = v.strip()
            if '-' in v:
                # element is an x-y range
                x, y = v.split('-')
                for i in range(int(x), int(y) + 1):
                    l.append(i)
            else:
                l.append(int(v))
        # remove duplicates and sort 
        return sorted(set(l))

    @staticmethod
    def _str_list(s): # type (str) -> list
        ''' 
        Parse a comma-seperated list of strings 
        '''
        l = []
        for v in str(s).split(','):
            l.append(v.strip())
        # remove duplicates and sort 
        return sorted(set(l))

    def __iter__(self):
        for key in sorted(vars(self)):
            yield key, getattr(self, key)

    def keys(self):
        return sorted(vars(self))
        
    def __getitem__(self, key):
        return getattr(self, key)
        
    def _parse(self, conf): # type: (dict) -> None
        ''' 
        Parse a dictionary into attributes using a schema 
        '''
        try:
            for key, value in conf.items():
                # normalize key
                # key = key.strip().lower().replace('-', '').replace('_', '')
                key = key.strip().lower().replace('-', '_')
                if isinstance(value, str):
                    # normalize value
                    value = value.strip().lower()
                    if value == 'auto' or value == '':
                        value = None
                if isinstance(value, list):
                    value = ','.join([str(v) for v in value])
                if key in self._schema:
                    if value is not None and callable(self._schema[key]):
                        # use schema callable to convert value
                        value = self._schema[key](value)
                    # assign to class attribute
                    setattr(self, key, value)
        except Exception as e:    
            raise Exception("unable to parse configuration: " + str(e))


class ConfigGlobals(ConfigBase):

    # a dictionary of callables that defines
    # the schema of the config dict/file
    _schema = {
        'dev': str, 
        'queues': int, 
        'cpus': ConfigBase._int_list,
        'numa': str,
        'optimize': ConfigBase._bool, 
        'bpstop': ConfigBase._bool,
        'bpstop_cfg': ConfigBase._bool,
        'busypoll': int, 
        'busyread': int, 
        'rxadapt': ConfigBase._bool, 
        'txadapt': ConfigBase._bool, 
        'rxusecs': int, 
        'txusecs': int, 
        'rxring': int, 
        'txring': int,
        'arpfilter': ConfigBase._bool, 
        'priority': str
    }

    def __init__(self, source=None): # type: (dict) -> None
        '''
        Create a new ConfigGlobals instance 
        optionally from a dictionary
        '''
        # attributes
        self.dev = None
        self.queues = None
        self.cpus = None
        self.numa = None
        self.optimize = None
        self.bpstop = None
        self.bpstop_cfg = None
        self.busypoll = None
        self.busyread = None
        self.rxadapt = None
        self.rxusecs = None
        self.rxring = None
        self.txadapt = None
        self.txusecs = None
        self.txring = None
        self.arpfilter = False
        self.priority = None

        # initialize section with source
        if source is not None:
            if not isinstance(source, dict):
                raise Exception("source must be a dictionary")
            self._parse(source)

    def __str__(self): # type () -> str
        return str(dict(self))

    def _validate(self, inv): # type: (Inventory) -> None
        '''
        Validate the config global section against a target system inventory
        '''
        # fill in 'auto' values
        if self.dev is None:
            devs = inv.devs.keys()
            devs.sort()
            self.dev = devs[0]
        self.queues = 2 if self.queues is None else self.queues
        self.cpus = 'auto' if self.cpus is None else self.cpus
        self.numa = 'all' if self.numa is None else self.numa

        # determine cpu list for section
        devnode = inv.devs[self.dev]['numa_node']
        if self.cpus == 'auto':
            if self.numa == 'local':
                # only local node
                self.cpus = inv.numa_cpus[devnode][:self.queues]
            elif self.numa == 'remote':
                # only remote node
                self.cpus = inv.numa_cpus[(devnode + 1) % inv.numa_nodes][:self.queues]
            elif self.numa == 'all':
                # local node first
                cpus = []
                for i in range(inv.numa_nodes):
                    cpus += inv.numa_cpus[(devnode + i) % inv.numa_nodes]
                self.cpus = cpus[:self.queues]
            else:
                # specific node
                node = int(self.numa)
                self.cpus = inv.numa_cpus[node][:self.queues]
        else:
            if len(self.cpus) != self.queues:
                raise Exception("cpus must equal the number of queues")

        # remove assigned cpus from inventory
        for cpu in self.cpus:
            for numa in inv.numa_cpus:
                if cpu in numa:
                    numa.remove(cpu)

        # check if cgroupv1 netprio is available
        if self.priority and self.priority == 'netprio':
            if not os.path.isdir("/sys/fs/cgroup/net_prio"):
                raise Exception("netprio is not currently available")
        

class ConfigSection(ConfigBase):

    # a dictionary of callables that defines
    # the schema of the config dict/file
    _schema = {
        'mode': str, 
        'queues': int, 
        'pollers': int,
        'poller_timeout': int,
        'protocol': str,
        'ports': ConfigBase._int_list, 
        'addrs': ConfigBase._str_list,
        'remote_ports': ConfigBase._int_list, 
        'remote_addrs': ConfigBase._str_list,
        'cpus': ConfigBase._int_list, 
        'numa': str
    }

    def __init__(self, source=None): # type (dict) -> None
        '''
        Create a new ConfigSection instance 
        optionally from a dictionary
        '''
        # attributes
        self.mode = None
        self.queues = None
        self.pollers = 0
        self.poller_timeout = 10000
        self.protocol = None
        self.ports = None
        self.addrs = None
        self.remote_ports = None
        self.remote_addrs = None
        self.cpus = None
        self.numa = None

        # initialize section with source
        if source is not None:
            if not isinstance(source, dict):
                raise Exception("source must be a dictionary")
            self._parse(source)

    def __str__(self): # type () -> str
        return str(dict(self))

    def _validate(self, inv, dev): # type: (Inventory, str) -> None
        '''
        Validate the config section against a target system inventory
        '''
        # fill in 'auto' values
        self.mode = 'exclusive' if self.mode is None else self.mode
        self.protocol = 'tcp' if self.protocol is None else self.protocol
        self.ports = [] if self.ports is None else self.ports
        self.remote_ports = [] if self.remote_ports is None else self.remote_ports
        self.queues = len(self.ports) if self.queues is None and self.mode == 'shared' else self.queues
        self.cpus = 'auto' if self.cpus is None else self.cpus
        self.numa = 'all' if self.numa is None else self.numa

        # determine cpu list for section
        devnode = inv.devs[dev]['numa_node']
        if self.cpus == 'auto':
            if self.numa == 'local':
                # only local node
                self.cpus = inv.numa_cpus[devnode][:self.queues]
            elif self.numa == 'remote':
                # only remote node
                self.cpus = inv.numa_cpus[(devnode + 1) % inv.numa_nodes][:self.queues]
            elif self.numa == 'all':
                # local node first
                cpus = []
                for i in range(inv.numa_nodes):
                    cpus += inv.numa_cpus[(devnode + i) % inv.numa_nodes]
                self.cpus = cpus[:self.queues]
            else:
                # specific node
                node = int(self.numa)
                self.cpus = inv.numa_cpus[node][:self.queues]
        else:
            if len(self.cpus) != self.queues:
                raise Exception("cpus must equal the number of queues")

        # remove assigned cpus from inventory
        for cpu in self.cpus:
            for numa in inv.numa_cpus:
                if cpu in numa:
                    numa.remove(cpu)

        # check for valid protocol
        if self.protocol not in ['tcp', 'udp']:
            raise Exception("invalid protocol")

        # check for valid cpu list
        if len(set(inv.cpus_online).intersection(self.cpus)) != len(self.cpus):
            raise Exception("invalid CPU list")

        # check for a valid port list
        for v in self.ports:
            if v > 65535:
                raise Exception("invalid port value: %r" % v)

        # check if config section is a valid TC description
        if not self.queues:
            raise Exception("invalid number of queues")


class Config(object):

    def __init__(self, source=None, log=None): # type: (any, str, any) -> None
        '''
        Create a new Config instance 
        optionally from a file-like object, a string, or a dictionary
        '''
        # attributes
        self.globals = ConfigGlobals()
        self._sections = OrderedDict()
        self._log = log

        # initialize config with source
        if source is not None:
            if hasattr(source, 'readline'):
                self._load(source)
            if isinstance(source, str):
                self._load(StringIO(source))
            elif isinstance(source, dict):
                self._parse(source)

    def __getattr__(self, attr): # type: (str) -> ConfigSection
        return self._sections[attr]

    def __iter__(self):
        yield 'globals', self.globals
        for key, value in self._sections.items():
            yield key, value

    def keys(self):
        return ['globals'] + sorted([k for k in self._sections])
        
    def __getitem__(self, key):
        if key == 'globals':
            return OrderedDict(self.globals)
        else:
            return OrderedDict(self._sections[key])

    def __str__(self): # type: () -> str
        return self._dumps()
    
    def _load(self, fp): # type: (any) -> None
        '''
        Loads then parses a config from a file-like object
        '''
        try:
            # load filepath as config file
            conf = SafeConfigParser()
            conf.readfp(fp)
        except:
            # raise Exception("unable to load %r" % filepath)
            raise
        # convert ConfigParser object to a dict
        config = {}
        for key in conf.sections():
            config[key] = dict(conf.items(key))
        # parse config
        self._parse(config)

    def _parse(self, object): # type: (dict) -> None
        ''' 
        Parse a dictionary into mutiple config sections
        '''
        try:
            # parse global section
            if 'globals' in object:
                self.globals._parse(object['globals'])
                del(object['globals'])
            # parse traffic class sections
            for key in object:
                self._sections[key] = ConfigSection(object[key])
        except Exception as e:
            raise Exception("invalid configuration file: " + str(e))

    def _dumps(self): # type: () -> str
        '''
        Outputs the current config as an INI-formatted string
        '''
        # create ConfigParser object from config dictionary
        conf = SafeConfigParser()
        config = dict(self)
        conf.add_section('globals')
        for key, value in config['globals'].items():
            if value is not None:
                if isinstance(value, list) or isinstance(value, set):
                    value = ','.join([str(v) for v in value])
                conf.set('globals', key, str(value).lower())
        del(config['globals'])
        for name, section in config.items():
            conf.add_section(name)
            for key, value in section.items():
                if value is not None:
                    if isinstance(value, list) or isinstance(value, set):
                        value = ','.join([str(v) for v in value])
                    conf.set(name, key, str(value).lower())
        buf = StringIO()
        conf.write(buf)
        return buf.getvalue().strip()

    @staticmethod
    def _cpu_mask(cpu): # type(int) -> str
        '''
        Create CPU mask for a specific core
        '''
        mask = "0"
        if cpu >= 32:
            fill = ""
            zero = "00000000"
            for i in range(cpu // 32):
                fill = fill + ",00000000"
            cpu -= 32 * (cpu // 32)
            mask = "%X%s" % (1 << cpu, fill)
        else:
            mask = "%X" % (1 << cpu)
        return mask

    @property
    def _queues(self): # type () -> int
        '''
        Returns the currently configured number of Combined queues on the NIC
        '''
        return Ethtool(self.globals.dev).channels().combined

    def _check_queues(self): # type() -> None
        '''
        Check if queue list is valid for system
        '''
        # total up the queue list
        requested = self.globals.queues
        for name, sec in self._sections.items():
            # TODO: check for proper power-of-two queue counts for each TC
            requested += sec.queues
        if requested > self._queues:
            raise Exception("Not enough queues available")
        
    def _set_sysctls(self):
        # global polling
        if self.globals.busypoll is not None:
            self.settings.busy_poll = self.globals.busypoll
        if self.globals.busyread is not None:
            self.settings.busy_read = self.globals.busyread
        # adjust arp filtering
        if self.globals.arpfilter:
            self.settings.arp_announce = 2
            self.settings.arp_ignore = 1
            self.settings.arp_notify = 1

    def _set_interface_flags(self):
        # enable tc offload
        self.settings.tc_offload = True
        # check if any sections are using the 'shared' mode
        shared = False
        for name, section in self:
            if name != 'globals' and section.mode == 'shared':
                shared = True
                break
        # if no sections are 'shared', enable global flow director if available
        if not shared and self.settings.flow_director is not None:
            self.settings.flow_director = True
        # set various tunables
        if self.globals.optimize is not None:
            self.settings.inspect_optimize = self.globals.optimize
        if self.globals.bpstop is not None:
            self.settings.bp_stop = self.globals.bpstop
        if self.globals.bpstop is not None:
            self.settings.bp_stop_cfg = self.globals.bpstop_cfg

    def _cleanup(self):
        '''
        Attempt to cleanup setup from previous run
        '''
        _printhead("Cleaning up any existing traffic classes and filters")
        tc = TCtool(self.globals.dev, self._log)
        # # clear any potentially conflicting qdisc filters
        tc.filter_del('ingress')
        tc.filter_del('egress')
        # clear any potentially conflicting qdiscs
        tc.qdisc_del(tc.TC_H_CLSACT, 'clsact')
        tc.qdisc_del(tc.TC_H_ROOT, 'mqprio')

        # disable any existing pollers
        try:
            _devlink_param(self.globals.dev, 'num_qps_per_poller', 0, log=self._log)
        except CalledProcessError:
            pass
        # clear any settings
        settings = Settings(self.globals.dev, self._log)
        settings.ntuple_filters = False
        settings.arp_announce = 0
        settings.arp_ignore = 0
        settings.arp_notify = 0
        settings.apply()

    def _set_tcs(self, echo=False): # type(bool) -> None
        _printhead("Setting traffic classes")
        if self._log:
            self._log.write("## qdisc and tc setup ##\n")

        num_tcs = len(self.keys())
        tc = TCtool(self.globals.dev, self._log)

        # create root mqprio qdisc
        count = [section.queues for _, section in self]
        pmap = [i for i in range(len(count))]
        offset = [sum(count[:i]) for i in range(len(count))]
        tc.qdisc_add(tc.TC_H_ROOT, 'mqprio', pmap, count, offset)
        
        # create classifier (ingress+egress) qdisc
        tc.qdisc_add(tc.TC_H_CLSACT, 'clsact')

        # display results
        if echo:
            output = _tc(self.globals.dev, "qdisc", "show")
            for line in output.split('\n'):
                if 'fq_code' not in line:
                    print(line)

        _printhead("Creating traffic filters")

        # create ingress & egress filters for TCs
        tc_idx = 0
        for name, section in self:
            if name != 'globals':
                if section.mode == 'exclusive' and self.settings.flow_director is None:
                    _devlink_param(
                        self.globals.dev, 'tc%d_inline_fd' % tc_idx, 'true',
                        log=self._log
                    )
                for port in section.ports:
                    if section.addrs is not None and len(section.addrs):
                        for addr in section.addrs:
                            if '/' not in addr:
                                addr = addr + '/32'
                            tc.filter_add(
                                'ingress', tc_idx, section.protocol, 
                                dst_addr=addr, dst_port=port, tc=tc_idx
                            )
                            if self.globals.priority and self.globals.priority == 'skbedit':
                                tc.filter_add(
                                    'egress', tc_idx, section.protocol, 
                                    src_addr=addr, src_port=port, 
                                    action='skbedit', priority=1
                                )
                    else:
                        tc.filter_add(
                            'ingress', tc_idx, section.protocol,
                            dst_port=port, tc=tc_idx
                        )
                        if self.globals.priority and self.globals.priority == 'skbedit':
                            tc.filter_add(
                                'egress', tc_idx, section.protocol, 
                                src_port=port, action='skbedit', priority=1
                            )
                for port in section.remote_ports:
                    if section.remote_addrs is not None and len(section.remote_addrs):
                        for addr in section.remote_addrs:
                            if '/' not in addr:
                                addr = addr + '/32'
                            tc.filter_add(
                                'ingress', tc_idx, section.protocol, 
                                src_addr=addr, src_port=port, tc=tc_idx
                            )
                            if self.globals.priority and self.globals.priority == 'skbedit':
                                tc.filter_add(
                                    'egress', tc_idx, section.protocol, 
                                    dst_addr=addr, dst_port=port, 
                                    action='skbedit', priority=1
                                )
                    else:
                        tc.filter_add(
                            'ingress', tc_idx, section.protocol,
                            src_port=port, tc=tc_idx
                        )
                        if self.globals.priority and self.globals.priority == 'skbedit':
                            tc.filter_add(
                                'egress', tc_idx, section.protocol, 
                                dst_port=port, action='skbedit', priority=1
                            )
            tc_idx += 1
                
        # check if any sections are using the 'shared' mode
        # create ntuple sideband filters as needed
        queue_idx = 0
        sideband = False
        ntuples = []
        for name, section in self:
            if name != 'globals' and section.mode == 'shared':
                if not sideband:
                    self.settings.ethtool.features({"rx-ntuple-filter": True})
                    sideband = True
                for i, port in enumerate(section.ports):
                    ntuples.append({
                        "flow-type": section.protocol + '4', 
                        "dst-port": port, "action": queue_idx
                    })
                    queue_idx += 1
                ntuples = self.settings.ethtool.ntuples(ntuples)
            else:
                queue_idx += section.queues

        # display setup
        # print("* Results")
        if echo:
            print(_tc(self.globals.dev, "filter", "show", "ingress"))
            if self.globals.priority and self.globals.priority == 'skbedit':
                print(_tc(self.globals.dev, "filter", "show", "egress"))
            if sideband:
                print("\nN-Tuple Filters:")
                for n in ntuples:
                    print(
                        "  Filter %d: %s port %d -> queue %d" % 
                        (n['id'], n['flow-type'].upper(), n['dst-port'], n['action'])
                    )

    def _set_options(self, echo=False): # type (bool) -> None
        _printhead("Setting interface options")
        if self._log:
            self._log.write("## network interface options ##\n")

        # set coalesce options
        modify = {}
        if self.globals.rxadapt is not None:
            modify["adaptive_rx"] = self.globals.rxadapt
        if self.globals.rxusecs is not None:
            modify["rx_usecs"] = int(self.globals.rxusecs)
        if self.globals.txadapt is not None:
            modify["adaptive_tx"] = self.globals.txadapt
        if self.globals.txusecs is not None:
            modify["tx_usecs"] = int(self.globals.txusecs)
        if len(modify):
            queues = sum([o.queues for _, o in self])
            queues = set(range(self.globals.queues, queues))
            try:
                # try to set coalesce just for application queues
                params = self.settings.ethtool.coalesce_queues(queues)
                params = [p._replace(**modify) for p in params]
                coalesce = self.settings.ethtool.coalesce_queues(queues, params)
            except:
                raise
                # if not able to, set globally
                params = self.settings.ethtool.coalesce()
                params = params._replace(**modify)
                coalesce = self.settings.ethtool.coalesce(params)
        else:
            try:
                coalesce = self.settings.ethtool.coalesce_queues(queues)
            except:
                raise
                coalesce = self.settings.ethtool.coalesce()
        
        # set ring size
        modify = {}
        if self.globals.rxring is not None:
            modify["rx"] = self.globals.rxring
        if self.globals.txring is not None:
            modify["tx"] = self.globals.txring
        params = None
        if len(modify):
            params = self.settings.ethtool.rings()
            params = params._replace(**modify)
        rings = self.settings.ethtool.rings(params)

        # display setup
        if echo:
            print("\nCoalesce Settings:")
            if isinstance(coalesce, list):
                coalesce = coalesce[0]
            print("  adaptive-rx: %s" % "on" if coalesce.adaptive_rx else "off")
            print("  rx-usecs: %d" % coalesce.rx_usecs)
            print("  adaptive-tx: %s" % "on" if coalesce.adaptive_tx else "off")
            print("  tx-usecs: %d" % coalesce.tx_usecs)
            print("\nRing Parameters:")
            print("  RX: %d\n  TX: %d" % (rings.rx, rings.tx))

    def _set_affinity(self): # type () -> None
        _printhead("Setting interrupt affinity")
        if self._log:
            self._log.write("## queue affinity ##\n")

        # get nic interrupts
        # named: ice-<dev>-TxRx-<queue>
        irqs = _exec("grep -i 'ice-%s-TxRx-' /proc/interrupts | cut -f1 -d:" % self.globals.dev, shell=True)
        irqs = [int(s.strip()) for s in irqs.split("\n")]
        if len(irqs) < 1:
            raise Exception("Unable to find interrupts for %s" % self.globals.dev)
        
        # get a list of assigned cpus
        cpus = []
        for _, section in self:
            cpus.extend(section.cpus)

        # affinitize interrupts to cores
        for i, irq in enumerate(irqs):
            mask = self._cpu_mask(cpus[i % len(cpus)])
            _writefile("/proc/irq/%d/smp_affinity" % irq, mask)
            if self._log:
                self._log.write("+ echo %s > /proc/irq/%d/smp_affinity\n" % (mask, irq))

        # display setup
        print("- Affinitized %d interrupts" % len(irqs))

    def _set_symmetry(self): # type () -> None
        _printhead("Setting symmetric queueing")
        if self._log:
            self._log.write("## symmetric queues ##\n")

        queues = self._queues
        for i in range(queues):
            mask = self._cpu_mask(i)
            _writefile("/sys/class/net/%s/queues/tx-%d/xps_rxqs" % (self.globals.dev, i), mask)
            if self._log:
                self._log.write("+ echo %s > /sys/class/net/%s/queues/tx-%d/xps_rxqs\n" % (mask, self.globals.dev, i))
        for i in range(queues):
            _writefile("/sys/class/net/%s/queues/tx-%d/xps_cpus" % (self.globals.dev, i), '0')
            if self._log:
                self._log.write("+ echo 0 > /sys/class/net/%s/queues/tx-%d/xps_cpus\n" % (self.globals.dev, i))

        # display setup
        print("- Aligned %d queues" % queues)

    def _set_pollers(self): # type () -> None
        _printhead("Setting independent pollers")
        if self._log:
            self._log.write("## independent pollers ##\n")
        tc_idx = 0
        for name, section in self:
            if name != 'globals' and section.pollers > 0:
                num_queues = int(math.ceil(float(section.queues) / section.pollers))
                _devlink_param(
                    self.globals.dev, 'tc%d_qps_per_poller' % tc_idx, num_queues,
                    log=self._log
                )
                _devlink_param(
                    self.globals.dev, 'tc%d_poller_timeout' % tc_idx, int(section.poller_timeout),
                    log=self._log
                )
            tc_idx += 1


    def add(self, name, object=None): # type(str, dict) -> None
        ''' 
        Adds the section to the config from a dictionary
        '''
        if name not in self._sections:
            self._parse({name: object})

    def validate(self): # type() -> None
        '''
        Validates the current config against the target system
        '''
        self.inventory = Inventory()
        self.globals._validate(self.inventory)
        for key in self._sections:
            self._sections[key]._validate(self.inventory, self.globals.dev)
        # TODO: check for total queue count

    def apply(self, echo=False): # type(bool) -> None
        '''
        Applies the current config to the target system
        '''
        self.validate()
        if self._log:
            self._log.write("### cleanup ###\n")
        self._cleanup()
        self._check_queues()
        self.settings = Settings(self.globals.dev, self._log)
        self._set_sysctls()
        self._set_interface_flags()
        _printhead("Modifying system and network settings")
        if self._log:
            self._log.write("\n### configuration ###\n")
        print(self.settings)
        self.settings.apply()
        self._set_tcs(echo=echo)
        if sum([section.pollers if name != 'globals' else 0 for name, section in self]):
            self._set_pollers()
        self._set_options(echo=echo)
        if self._log:
            self._log.write("\n### affinitization ###\n")
        self._set_affinity()
        self._set_symmetry()


## Check functions

def check_depends(log=None, echo=False): # type (any, bool) -> None
    '''
    Check for and install any needed dependencies
    '''
    # TODO: add distro check, adapt commands/output as needed
    _printhead("Checking for needed packages")

    packages = []
    packages.append('libcgroup-tools')

    needed = []

    for package in packages:
        if not _exec(['rpm', '-q', package], check=True, ):
            needed.append(package)

    if len(needed):
        _printhead("Installing missing packages")
        _exec(["yum", "-y", "install"] + needed, log=log, echo=echo, )


def check_services(log=None, echo=False): # type (any, bool) -> None
    '''
    Check for potentially troublesome system services
    '''
    _printhead("Checking system services")

    if _exec(['systemctl', 'status', 'irqbalance'], check=True, echo=echo, ):
        print('Warning: irqbalance is installed and running. This may impact performance.')
        time.sleep(2)


def reload_driver(driver=None, log=None, echo=False): # (str, bool, any, bool) -> None
    '''
    Reload device driver for the NIC
    '''
    _printhead("Reloading device driver")
    print("- Unloading current driver...")
    _exec(['modprobe', '-vr', 'ice'], log=log, echo=echo, )
    time.sleep(2)
    if log:
        log.write('sleep 2\n')

    print("- Loading driver...")
    if driver is None:
        _exec(['modprobe', '-v', 'ice'], log=log, echo=echo, )
    else:
        _exec(['insmod', driver], log=log, echo=echo, )
    time.sleep(3)
    if log:
        log.write('sleep 3\n')


# def check_driver(dev, log=None, echo=False): # type (str, any, bool) -> None
#     '''
#     Check ICE driver and version
#     '''
#     _printhead("Checking ICE driver and version")

#     # check ice driver version
#     ver = _exec(['modinfo', '--field=version', 'ice' if driver is None else driver], )
#     print("- Version: %s" % (ver if ver else "not available",))
    
#     if ver:
#         ver = re.match("(\d+)\.(\d+)\.(\d+).*", ver)
#         if not ver:
#             raise Exception("unknown driver version, please install the OOT ice driver")
#         else:
#             ver = ver.groups()
#             if (int(ver[0]) < 1) or (int(ver[1]) < 2):
#                 raise Exception("old ice driver version, please update")

#     verbiage = []

def check_interface(dev, log=None, echo=False): # type (str, any, bool) -> None
    '''
    Check if interface is functioning and up
    '''
    _printhead("Checking interface %r" % dev)

    if dev is None:
        # TODO: detect first CVL NIC
        #     search /sys/class/net/*/device/driver/module/drivers 
        #     look for a 'pci:ice' symbolic link
        raise Exception("you must provide a network dev")
    else:
        # check if net dev exists
        if not os.path.isdir("/sys/class/net/%s" % dev):
            raise Exception("%r net dev does not exist" % dev)
        # check if net dev is using the ice driver
        if not os.path.islink("/sys/class/net/%s/device/driver/module/drivers/pci:ice" % dev):
            raise Exception("%r net dev is not using the ice driver" % dev)
        ice_version = _readfile("/sys/class/net/%s/device/driver/module/drivers/pci:ice/module/version" % dev)
        ice_srcversion = _readfile("/sys/class/net/%s/device/driver/module/drivers/pci:ice/module/srcversion" % dev)
        print("- Driver: ice v%s (%s)" % (ice_version, ice_srcversion))

    ip = IPtool(dev)

    # check link status
    status = ip.link_state()
    if status != 'UP':
        raise Exception("network device %s status is currently %r" % (dev, status))
    print("- Link Status: %s" % status)
    
    # check ip addressing
    addresses = ip.addrs()
    if not addresses or not len(addresses):
        raise Exception("unable to determine address of %s" % dev)
    print("- IP Addresses: %s" % addresses)


def _load(filename=None, isjson=False, log=None): # type (str, bool, any) -> Config
    '''
    Loads a config from a file or stdin and returns a Config object
    '''
    fp = None
    if not filename:
        if not sys.stdin.isatty():
            fp = sys.stdin
        else:
            raise Exception("you must provide a config file")
    else:
        if filename == '-':
            fp = sys.stdin
        elif os.path.isfile(filename):
            fp = open(filename)
        else:
            raise Exception("config file %r not found" % filename)
    _printhead("Loading config from %r" % fp.name)
    if isjson:
        return Config(json.load(fp), log=log)
    else:
        return Config(fp, log=log)


def _install():
    '''
    Install this script as /usr/local/bin/adqsetup
    '''
    filename = os.path.realpath(__file__)
    if filename == '/usr/local/bin/adqsetup':
        return
    _printhead("Installing this script in the command path")
    _exec(["install", "--backup", filename, "/usr/local/bin/adqsetup"])
    print("- This script has been installed as /usr/local/bin/adqsetup")


def _main():
    ''' 
    Main function for CLI
    '''
    if sys.stdin.isatty():
        prolog = [
            "\x1B[33m***\x1B[1m ADQ Setup Tool v%s \x1B[0m\x1B[33m***\x1B[0m" % _VERSION_,
            "\x1B[90mWebsite: https://www.intel.com/content/www/us/en/architecture-and-technology/ethernet/adq-resource-center.html\x1B[0m",
            "\x1B[90mSPDX-License-Identifier: BSD-3-Clause\x1B[0m",
            "\x1B[90mCopyright (c) 2022, Intel Corporation\x1B[0m"
        ]
    else:
        prolog = [
            "*** ADQ Setup Tool v%s ***" % _VERSION_,
            "Website: https://www.intel.com/content/www/us/en/architecture-and-technology/ethernet/adq-resource-center.html",
            "SPDX-License-Identifier: BSD-3-Clause",
            "Copyright (c) 2022, Intel Corporation"
        ]
    prolog.append("For use with Intel Ethernet E810 Controllers and Network Adapters ONLY\n")

    for line in prolog: print(line)

    parser = ArgumentParser(
        prog="adqsetup",
        formatter_class=RawDescriptionHelpFormatter, 
        epilog="\n".join([
            "examples:",
            "  %(prog)s apply mysetup.conf -> applies the setup from a config file",
            "  %(prog)s create nginx queues 6 ports 80,443 -> creates a traffic class of 6 queues for ports 80 and 443",
            "  %(prog)s create redis mode shared ports 6379-6382 cpus 2,4,6,8 -> creates a traffic class of 4 queues",
            "      for ports 6379 through 6382, affinitized to specific cpus",
            " "
        ])
    )

    # parameters
    parser.add_argument('command', metavar='COMMAND', choices=['apply', 'create', 'reset', 'persist', 'examples', 'install', 'help'], 
        help="'apply', 'create', 'reset', 'persist', 'examples', 'install', or 'help'")    
    parser.add_argument('params', metavar='PARAMS', type=str, nargs='*', help="parameters for the command")

    # global options
    parser.add_argument('--dev', '-d', metavar="<NETDEV>", type=str, help="network device", default=SUPPRESS)
    parser.add_argument('--queues', '-q', type=int, help="number of queues for non-ADQ traffic", default=SUPPRESS)
    parser.add_argument('--optimize', '-o', nargs='?', const=True, help="set channel-pkt-inspect-optimize (on/off)", default=SUPPRESS)
    parser.add_argument('--bpstop', '-s', nargs='?', const=True, help="set channel-packet-clean-bp-stop (on/off)", default=SUPPRESS)
    parser.add_argument('--bpstop-cfg', nargs='?', const=True, help="set channel-packet-clean-bp-stop-cfg (on/off)", default=SUPPRESS)
    parser.add_argument('--busypoll', '-b', metavar='<INT>', type=int, help="busy_poll value", default=SUPPRESS)
    parser.add_argument('--busyread', metavar='<INT>', type=int, help="busy_read value", default=SUPPRESS)
    parser.add_argument('--rxadapt', dest='rxadapt', nargs='?', const=True, help="set adaptive rx coalesce (on/off)", default=SUPPRESS)
    parser.add_argument('--rxusecs', dest='rxusecs', metavar='<INT>', type=int, help="rx coalesce usec value", default=SUPPRESS)
    parser.add_argument('--rxring', dest='rxring', metavar='<INT>', type=int, help="rx ring size", default=SUPPRESS)
    parser.add_argument('--txadapt', dest='txadapt', nargs='?', const=True, help="set adaptive tx coalesce (on/off)", default=SUPPRESS)
    parser.add_argument('--txusecs', dest='txusecs', metavar='<INT>', type=int, help="tx coalesce usec value", default=SUPPRESS)
    parser.add_argument('--txring', dest='txring', metavar='<INT>', type=int, help="tx ring size", default=SUPPRESS)
    parser.add_argument('--arpfilter', '-f', action='store_true', help="enable selective ARP activity in order to properly "
        "use more then one interface on the same subnet", default=SUPPRESS)
    parser.add_argument('--priority', '-p', metavar='<METHOD>', choices=['skbedit'], help="method to use for setting socket priority, "
        "possible values are 'skbedit'", default=SUPPRESS)    

    # runtime options
    parser.add_argument('--debug', '-D', action='store_true', help="enable debug mode")
    parser.add_argument('--verbose', '-v', action='store_true', help="enable verbose mode")
    parser.add_argument('--driver', metavar="<FILEPATH>", type=str, help="path for device driver to use", default=None)
    parser.add_argument('--log', '-l', metavar="<FILEPATH>", type=FileType('w'), help="command log file", default=None)
    parser.add_argument('--json', '-j', action='store_true', help="use json for configuration format")
    parser.add_argument('--reload', '-r', action='store_true', help="reload device driver")
    parser.add_argument('--version', '-V', action='version', version='%(prog)s ' + _VERSION_)

    args = parser.parse_args()
    if args.debug:
        args.verbose = True

    try:
        if args.command in ['apply', 'persist']:
            filename = None
            if len(args.params):
                filename = args.params[0]
            config = _load(filename, args.json, args.log)
        elif args.command == 'create':
            params = copy(args.params)
            if not len(params):
                raise Exception("not enough parameters")
            name = params.pop(0)
            group = {}
            while len(params):
                n = params.pop(0).replace('-', '_')
                if n not in set(vars(ConfigSection())):
                    raise Exception("Invalid parameter %r" % n)
                try:
                    v = params.pop(0)
                except:
                    raise Exception("Missing value for parameter %r" % n)
                group[n] = v
            config = Config({name: group}, log=args.log)
        elif args.command == 'reset':
            config = Config({}, log=args.log)
            config._parse({'globals': vars(args)})
            config._cleanup()
            return 0
        elif args.command == 'examples':
            _printhead("Creating example config files")
            fpath = os.path.join(os.getcwd(), 'examples')
            if os.path.exists(fpath):
                raise Exception("The directory %r already exists, unable to create example config files" % fpath)
            os.mkdir(fpath)
            for name, data in _examples.items():
                _writefile(os.path.join(fpath, name + ".conf"), data)
            print("- Example config files have been created in the directory %r" % fpath)
            return 0
        elif args.command == 'install':
            _install()
            return 0
        elif args.command == 'help':
            parser.print_help()
            return 0

        config._parse({'globals': vars(args)})

        # print configuration
        print("- Python: %s" % sys.version.split()[0])
        print("- Host: %s" % _exec(['hostname']))
        print("- Kernel: %s" % _exec(['uname', '-r']))

        _printhead("Configuration")
        print(str(config).strip())
        check_services(args.log, args.verbose)

        if args.command in ['apply', 'create']:
            if args.reload:
                reload_driver(args.driver, args.log, args.verbose)

        check_interface(config.globals.dev, args.log, args.verbose)

        if args.command in ['apply', 'create']:
            config.apply(args.verbose)
        elif args.command == 'persist':
            config.validate()
            if not os.path.isfile('/usr/local/bin/adqsetup'):
                _install()
            _printhead("Creating a systemd service for %r using the current config" % config.globals.dev)
            _writefile("/var/lib/adqsetup/%s.conf" % config.globals.dev, config._dumps())
            _writefile("/etc/systemd/system/adqsetup@.service", _service_unit)
            _exec(["systemctl", "daemon-reload"])
            print("- Persisted the current config as a systemd service")
            print("- Use the 'systemctl enable --now adqsetup@%s' command to enable this service on boot" % config.globals.dev)
    except Exception as err:
        if args.log: 
            args.log.close()
        if args.debug:
            raise
        else:
            _printhead("\x1B[91mError occurred! Exiting now...\x1B[0m")
            print("-> " + str(err))
            if isinstance(err, subprocess.CalledProcessError):
                if sys.version[:1] == '3':
                    print(err.output.decode().strip())
                else:
                    print(err.output.strip())
            return 1
    return 0


## CLI Entrypoint

if __name__ == "__main__": 
    sys.exit(_main())
