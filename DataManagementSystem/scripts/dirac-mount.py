############################################################
#
# dirac-mount command to mount DIRAC FS
#
############################################################

from DIRAC.Core.Base import Script
Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s <pilot reference>' % Script.scriptName ] ) )

Script.parseCommandLine( ignoreErrors = True )

if __name__ == "main":
  print "The code goes here"