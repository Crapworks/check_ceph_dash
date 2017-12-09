#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import json
import argparse

from urllib2 import Request
from urllib2 import urlopen

__version__ = '0.1'

class CephClusterStatus(dict):
    def __init__(self, url):
        dict.__init__(self)
        req = Request(url)
        req.add_header('Content-Type', 'application/json')
        try:
            self.update(json.load(urlopen(req)))
        except Exception as err:
            print "UNKNOWN: %s" % (str(err), )
            sys.exit(3)

    def _map(self, status):
        _map = {
            'HEALTH_OK': ('OK', 0),
            'HEALTH_WARN': ('WARNING', 1),
            'HEALTH_ERR': ('CRITICAL', 2),
        }
        if status in _map:
            return _map[status]
        else:
            return ('UNKNOWN', 3)

    def get_perf_data(self):
        if 'status' in self['health']:
            nagios_str, nagios_exit = self._map(self['health']['status'])
        else:
            nagios_str, nagios_exit = self._map(self['health']['overall_status'])
        if nagios_exit == 3:
            return ""

        # perfdata to fetch
        perf_values = {
            'pgmap': ['bytes_used', 'bytes_total', 'bytes_avail', 'data_bytes', 'num_pgs', 'read_bytes_sec', 'write_bytes_sec'],
            'osdmap': ['num_osds', 'num_up_osds', 'num_in_osds']
        }

        if 'op_per_sec' in self['pgmap']:
            # pre Jewel
            perf_values['pgmap'].append('op_per_sec')
        else:
            # >= Jewel
            perf_values['pgmap'].append('write_op_per_sec')
            perf_values['pgmap'].append('read_op_per_sec')

        perfdata = dict()
        for map_type, values in perf_values.iteritems():
            for value in values:
                # the json structure is horrible...
                if map_type == 'osdmap':
                    perfdata[value] = self['osdmap'][map_type].get(value, 0)
                else:
                    perfdata[value] = self[map_type].get(value, 0)

        perfdata=' '.join(['%s=%s' % (key, val) for key, val in perfdata.iteritems()])

        return perfdata

    def get_exit_code(self):
        if 'status' in self['health']:
            nagios_str, nagios_exit = self._map(self['health']['status'])
        else:
            nagios_str, nagios_exit = self._map(self['health']['overall_status'])
        return int(nagios_exit)

    def get_nagios_string(self):
        if 'status' in self['health']:
            nagios_str, nagios_exit = self._map(self['health']['status'])
        else:
            nagios_str, nagios_exit = self._map(self['health']['overall_status'])
        if nagios_exit == 0:
            summary = 'ceph cluster operates with no problems'
        else:
            if 'checks' in self['health']:
                summary = '\n'.join([ "{severity}: {summary[message]}".format(**problems) for problems in self['health']['checks'].values()])
            elif 'summary' in self['health']:
                summary = '\n'.join([ "{severity}: {summary}".format(**problems) for problems in self['health']['summary']])
            else:
                summary = 'Unable to fetch healt details. Please check cluster directly'

        return "%s: %s" % (nagios_str, summary)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-u', '--url', help='url of ceph-dash instance', required=True)
    args = parser.parse_args()

    status = CephClusterStatus(args.url)
    print "%s|%s" % (status.get_nagios_string(), status.get_perf_data())
    sys.exit(status.get_exit_code())

if __name__ == '__main__':
    main()
