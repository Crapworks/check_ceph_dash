check-ceph-dash - nagios/icinga check for use with ceph-dash
============================================================

This nagios/icinga plugin simply connects to a ceph-dash instance, gather the information about the overall cluster health and outputs a nagios compatible message including several perfdata metrics.

**dependencies**

Just plain python. Uses urllib2 to gather data from the ceph-dash instance.

Usage
-----

```
./check-ceph-dash.py --url 'http://url.to.ceph.dash/'
OK: ceph cluster operates with no problems|bytes_used=244455534592 bytes_total=359702620323840 bytes_avail=359458164789248 data_bytes=110961570327 num_pgs=5120 op_per_sec=1 read_bytes_sec=0 write_bytes_sec=1913
```


