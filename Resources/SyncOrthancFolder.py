#!/usr/bin/python

#
# This maintenance script updates the content of the "Orthanc" folder
# to match the latest version of the Orthanc source code.
#

import multiprocessing
import os
import stat
import urllib2

TARGET = os.path.join(os.path.dirname(__file__), 'Orthanc')
PLUGIN_SDK_VERSION = '1.4.0'
REPOSITORY = 'https://bitbucket.org/sjodogne/orthanc/raw'

FILES = [
    'DownloadOrthancFramework.cmake',
    'LinuxStandardBaseToolchain.cmake',
    'MinGW-W64-Toolchain32.cmake',
    'MinGW-W64-Toolchain64.cmake',
    'MinGWToolchain.cmake',
]

SDK = [
    'orthanc/OrthancCPlugin.h',
    'orthanc/OrthancCDatabasePlugin.h',
    #'orthanc/OrthancCppDatabasePlugin.h',
]   

EXE = [
    #'Resources/EmbedResources.py',
    #'Resources/WindowsResources.py',
]


def Download(x):
    branch = x[0]
    source = x[1]
    target = os.path.join(TARGET, x[2])
    print target

    try:
        os.makedirs(os.path.dirname(target))
    except:
        pass

    url = '%s/%s/%s' % (REPOSITORY, branch, source)

    try:
        with open(target, 'w') as f:
            f.write(urllib2.urlopen(url).read())
    except:
        print 'Cannot download %s' % url
        raise


commands = []

for f in FILES:
    commands.append([ 'default',
                      os.path.join('Resources', f),
                      f ])

for f in SDK:
    commands.append([ 
        'Orthanc-%s' % PLUGIN_SDK_VERSION, 
        'Plugins/Include/%s' % f,
        'Sdk-%s/%s' % (PLUGIN_SDK_VERSION, f) 
    ])


pool = multiprocessing.Pool(10)  # simultaneous downloads
pool.map(Download, commands)


for exe in EXE:
    path = os.path.join(TARGET, exe)
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)

