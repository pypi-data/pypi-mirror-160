#! /usr/bin/env python
"""
Add all the files under specified directory to SE and DFC

Usage:
  ihepdirac_dms_add_dir [option|cfgfile] DFCDir LocalDir SE

Example:
  ihepdirac_dms_add_dir /juno/user/z/zhangxm/9743 /junofs/grid/user/z/zhangxm/9743 IHEP-JUNOEOS

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

import os
import sys

from DIRAC.Core.Base import Script
from DIRAC.Core.Utilities.DIRACScript import DIRACScript
from DIRAC import S_OK, S_ERROR, gLogger, exit

@DIRACScript()
def main():

    Script.parseCommandLine(ignoreErrors = False)
    args = Script.getPositionalArgs()

    if len(args) != 3:
        Script.showHelp()
        exit(1)

    dfcDir = args[0]
    localDir = args[1]
    toSE = args[2]

    from DIRAC.Interfaces.API.Dirac import Dirac
    dirac = Dirac()

    lfnList = []
    pfnList = []

    for root, dirs, files in os.walk(localDir):
        if not root.startswith(localDir):
            gLogger.error('Can not find corrent lfn')
            exit(1)
        relRoot = root[len(localDir):].lstrip('/')
        for f in files:
            fullFn = os.path.join(root, f)
            lfn = os.path.join(dfcDir, relRoot, f)
            lfnList.append(lfn)
            pfnList.append(fullFn)

    gLogger.notice('%s files will be added to DFC "%s"' % (len(lfnList), dfcDir))

    for lfn, pfn in zip(lfnList, pfnList):
        gLogger.debug('Add file to DFC: %s' % lfn)
        result = dirac.addFile(lfn, pfn, toSE)
        if not result['OK']:
            gLogger.error('Can not add file to DFC "%s": %s' % (lfn, result['Message']))
            exit(1)
        gLogger.debug('File upload successfully: %s' % f)
    gLogger.notice('%s files added to DFC' % len(lfnList))

if __name__ == "__main__":
    main()
