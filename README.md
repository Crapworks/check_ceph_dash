check-ceph-dash - nagios/icinga check for use with ceph-dash
============================================================

This nagios/icinga plugin simply connects to a [ceph-dash](https://github.com/Crapworks/ceph-dash) instance, gather the information about the overall cluster health and outputs a nagios compatible message including several perfdata metrics.

**dependencies**

Just plain python. Uses urllib2 to gather data from the ceph-dash instance.

Usage
-----

```
./check-ceph-dash.py --url 'http://url.to.ceph.dash/'
OK: ceph cluster operates with no problems|bytes_used=244455534592 bytes_total=359702620323840 bytes_avail=359458164789248 data_bytes=110961570327 num_pgs=5120 op_per_sec=1 read_bytes_sec=0 write_bytes_sec=1913
```

Fancy Dashboards
----------------

By using the generated performance data and sending them to a graphite backend, you can create quite fancy metric dashboards. See the following screenshot for an example (the frontend is [Graphana](http://grafana.org/))

![screenshot01](https://github.com/crapworks/check_ceph_dash/raw/master/screenshots/ceph-grafana.png)
