#!/usr/bin/env python

"""
Return disk usage statistics about the given path as a (total, used, free)
namedtuple.  Values are expressed in bytes.
"""
# Author: adopted from Giampaolo Rodola
# License: MIT

import os
import collections
import psutil
import time

_ntuple_diskusage = collections.namedtuple('usage', 'total used free')

if hasattr(os, 'statvfs'):  # POSIX
    def disk_usage(path):
        st = os.statvfs(path)
        #free = st.f_bavail * st.f_frsize
        free = st.f_bfree * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return _ntuple_diskusage(total, used, free)



def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1000.0:
            return "%3.3f%s%s" % (num, unit, suffix)
        num /= 1000.0
    return "%.3f%s%s" % (num, 'Yi', suffix)

def dothings():
    path = os.getcwd()
    #print path
    disku=disk_usage(path)
    #print disku
    psutil.cpu_percent()
    time.sleep(5)
    print "total space", sizeof_fmt(disku.total)
    print "used space", sizeof_fmt(disku.used)
    print "free space", sizeof_fmt(disku.free)
    print "CPU P usage", psutil.cpu_percent()
    print "Phys mem usage", psutil.phymem_usage().percent
    print "Virt mem usage", psutil.virtual_memory().percent




disk_usage.__doc__ = __doc__

if __name__ == '__main__':
    dothings()






