############################################################
#
# dirac-mount command to mount FUSE based DIRAC FS
#
############################################################

import os

if __name__ == "main":
  from DIRAC.Core.Base import Script
  Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s [MountPoint]' % Script.scriptName,
                                     'Arguments:',
                                     '  MountPoint:     path to an exist mount directory',
                                     '', 
                                     'Examples:',
                                     '  $ dirac-mount /tmp/diracfs', 
                                     ] ) )

  Script.parseCommandLine( ignoreErrors = True )
