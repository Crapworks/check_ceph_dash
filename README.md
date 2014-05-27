check-ceph-dash - nagios/icinga check for use with ceph-dash
============================================================

This nagios/icinga plugin simply connects to a ceph-dash instance, gather the information about the overall cluster health and outputs a nagios compatible message including several perfdata metrics.

**dependencies**

Just plain python. Uses urllib2 to gather data from the ceph-dash instance.

Usage
-----


