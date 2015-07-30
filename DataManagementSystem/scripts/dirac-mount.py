#!/usr/bin/env python

"""
dirac-mount command to mount DIRAC FS
"""

from DIRAC.Core.Base import Script

Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s [MountPoint]' % Script.scriptName,
                                     'Arguments:',
                                     '  MountPoint:     path to an exist mount directory',
                                     '', 'Examples:',
                                     '  $ dirac-mount /tmp/diracfs',
                                     ] )
                        )

Script.registerSwitch( "se", "se=", "Set SE disk" )
Script.parseCommandLine( ignoreErrors = True )

import os
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
newarg = []
for a in sys.argv:
  if not a.find("--se"):
    ss = a.split("=")
    newarg.append("-o SE="+ss[1])
  else:
    newarg.append(a)

newcmd = "DiracFS.py"
for index, item in enumerate(newarg):
  if not index==0:
    newcmd += " "
    newcmd += item
os.system(newcmd)
