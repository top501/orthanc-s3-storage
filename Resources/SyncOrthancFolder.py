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
PLUGIN_SDK_VERSION = '1.3.2'
REPOSITORY = 'https://bitbucket.org/sjodogne/orthanc/raw'

FILES = [
    'Core/Cache/LeastRecentlyUsedIndex.h',
    'Core/Endianness.h',
    'Core/Enumerations.cpp',
    'Core/Enumerations.h',
    'Core/Logging.cpp',
    'Core/Logging.h',
    'Core/OrthancException.h',
    'Core/PrecompiledHeaders.cpp',
    'Core/PrecompiledHeaders.h',
    'Core/Toolbox.cpp',
    'Core/Toolbox.h',
    'Plugins/Samples/Common/ExportedSymbols.list',
    'Plugins/Samples/Common/OrthancPluginCppWrapper.cpp',
    'Plugins/Samples/Common/OrthancPluginCppWrapper.h',
    'Plugins/Samples/Common/OrthancPluginException.h',
    'Plugins/Samples/Common/VersionScript.map',
    'Resources/CMake/AutoGeneratedCode.cmake',
    'Resources/CMake/BoostConfiguration.cmake',
    'Resources/CMake/Compiler.cmake',
    'Resources/CMake/DownloadPackage.cmake',
    'Resources/CMake/JsonCppConfiguration.cmake',
    'Resources/EmbedResources.py',
    'Resources/MinGW-W64-Toolchain32.cmake',
    'Resources/MinGW-W64-Toolchain64.cmake',
    'Resources/MinGWToolchain.cmake',
    'Resources/ThirdParty/VisualStudio/stdint.h',
    'Resources/ThirdParty/base64/base64.cpp',
    'Resources/ThirdParty/base64/base64.h',
]

SDK = [
    'orthanc/OrthancCPlugin.h',
]   

EXE = [
    'Resources/EmbedResources.py',
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
    commands.append([ 'default', f, f ])

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

