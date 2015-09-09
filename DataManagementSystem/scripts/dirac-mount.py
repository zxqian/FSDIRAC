#!/usr/bin/env python

"""
dirac-mount command to mount DIRAC FS
"""

import os

from DIRAC.Core.Base import Script
from DIRAC import S_OK

defaultSE = ""
def setDefaultSE( value ):
    global defaultSE
    defaultSE = value
    return S_OK()

Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s [MountPoint]' % Script.scriptName,
                                     'Arguments:',
                                     '  MountPoint:     path to an exist mount directory',
                                     '', 'Examples:',
                                     '  $ dirac-mount /tmp/diracfs',
                                     '', 'More help:',
                                     '  https://github.com/DIRACGrid/FSDIRAC/blob/master/README.md',
                                     ] )
                        )

Script.registerSwitch( "S:", "se=", "Default Storage Element", setDefaultSE )
Script.parseCommandLine( ignoreErrors = True )

from DIRAC import exit as DIRACexit

args = Script.getPositionalArgs()
if len( args ):
    arg = args[ 0 ]
    aarg = os.path.abspath( arg )
    if os.path.isdir(aarg):
        if os.listdir(aarg):
            print  "["+arg+"]"+" is not empty"
            Script.showHelp()
            DIRAC.exit( 0 )
    else:
        print "["+arg+"]"+" is not a valid directory"
        Script.showHelp()
        DIRAC.exit( 0 )
else:
    print "no mount point"
    Script.showHelp()
    DIRAC.exit( 0 )

# call DiracFS.py

import sys
from FSDIRAC.DataManagementSystem.private import DiracFS
if defaultSE:
    for i, item in enumerate(sys.argv):
        if not item.find("--se="):
            sys.argv.pop(i)
            sys.argv.append("-o") 
            sys.argv.append("SE=" + defaultSE) 
            break
        elif not item.find("--se") or not item.find("-S"):
            sys.argv[i] = "-o"
            sys.argv[i+1] = "SE=" + defaultSE
DiracFS.main(sys.argv)

