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
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from sh import uptime
import re

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

def getCpuLoad():
    psutil.cpu_percent()
    time.sleep(.1)
    return (psutil.cpu_percent())

def getMem():
    return (psutil.phymem_usage().percent)

def getDisk(path):
    #path = os.getcwd() #gets the current "working directory"
    #path = '/Volumes/Macintosh HD'
    disku=disk_usage(path)
    diskinfo={'pathused' : path,
                  'total': sizeof_fmt(disku.total),
                  'used' : sizeof_fmt(disku.used),
                'free' : sizeof_fmt(disku.free)}
    return(diskinfo)


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
    return()


def dothings2():
    #cpu=getCpuLoad()
    ram=getMem()
    disk=getDisk('/Volumes/Macintosh HD')
    #disk2=getDisk('')
    #print cpu
    print ram
    print disk


    return()

#######################################################
####seperating app from logic until files are split####
#######################################################

app = Flask(__name__)

@app.route('/')
def index():

    alldisks=['/Volumes/Macintosh HD']
    data=[]
    for d in alldisks:
        data.append(getDisk(d))

    up=str(uptime())
    up=re.split(r'[,]*',up)
    up2='Uptime is '+ up[0][10:]+up[1][:3]+' hours ' + up[1][-2:] + ' minutes'


    return render_template('index.html',data=data,up2=up2)


@app.route("/processor",methods=['GET','POST'])
def processor():
    cpu=getCpuLoad()
    return jsonify(cpu=cpu)

'''
@app.route("/uptime")
def howlong():
    up=str(uptime())
    up=re.split(r'[,]*',up)
    print up
    up2='Uptime is: '+ up[0][10:]+up[1][:3]+' hours ' + up[1][-2:] + ' minutes'

    return jsonify(up2=up2)
'''


@app.route("/disk",methods=['GET','POST'])
def diskpage():

    alldisks=['/Volumes/Macintosh HD']

    data=[]

    for d in alldisks:
        data.append(getDisk(d))

    return render_template('disk.html',data=data)



#disk_usage.__doc__ = __doc__


if __name__ == "__main__":
    #dothings2()
    app.debug = True
    app.run()






