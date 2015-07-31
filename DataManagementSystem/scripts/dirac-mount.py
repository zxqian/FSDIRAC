#!/usr/bin/env python

"""
dirac-mount command to mount DIRAC FS
"""

import os
import atexit

from DIRAC.Core.Base import Script
from DIRAC import S_OK

defaultSE = "DIRAC-USER"
def setDefaultSE( value ):
  global defaultSE
  defaultSE = value
  return S_OK()

tmpDir = "/tmp/diracfs_"+os.environ['LOGNAME']
def setTmpDir( value ):
  global tmpDir
  tmpDir = value
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
Script.registerSwitch( "T:", "tmpdir=", "Directory to hold the local cache", setTmpDir )

Script.parseCommandLine( ignoreErrors = True )

@atexit.register
def goodbye():
  #os.rmdir(        tmpDir)
  import shutil
  shutil.rmtree( tmpDir )

usage = """
dirac-mount -T <cache_directory> <mount_point>
"""

if __name__ == "main":

    from FSDIRAC.DataManagementSystem.private.DiracFS import DiracFS
    from DIRAC import exit as DIRACexit

    args = Script.getPositionalArgs()
    if len( args ):
      arg = args[ 0 ]
      aarg = os.path.abspath( arg )
      if os.path.isdir(aarg):
        if os.listdir(aarg):
          print  "["+arg+"]"+" is not empty"
          Script.showHelp()
          DIRACexit( 0 )
      else:
        print "["+arg+"]"+" is not a valid directory"
        Script.showHelp()
        DIRACexit( 0 )
    else:
      print "no mount point"
      Script.showHelp()
      DIRACexit( 0 )

    if not os.path.isdir( tmpDir ):
        os.makedirs( tmpDir )

    diracFS = DiracFS( defaultSE = defaultSE,
                       tmpDir = tmpDir,
                       version = "%prog " + fuse.__version__,
                       usage = usage,
                       dash_s_do = 'setsingle' )

    diracFS.parser.add_option( mountopt = "SE",
                               metavar = "Storage Element ID",
                               default = "DIRAC-USER",
                               help = "specify the used storage element [default: %default]")
    diracFS.parse( values = diracFS, errex = 1 )
    diracFS.main()


