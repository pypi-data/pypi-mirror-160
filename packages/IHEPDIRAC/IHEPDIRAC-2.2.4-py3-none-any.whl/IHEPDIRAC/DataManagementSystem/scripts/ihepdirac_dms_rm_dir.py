#! /usr/bin/env python
"""
Remove all the files and directories from SE and DFC under specified directory

Usage:
  ihepdirac-dms-rm-dir [option|cfgfile] DFCDir

Example:
  ihepdirac-dms-rm-dir /juno/user/z/zhangxm/9743
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

import os

from DIRAC import exit as DIRACExit, gLogger
from DIRAC.Core.Base import Script
from DIRAC.Core.Utilities.DIRACScript import DIRACScript
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC.DataManagementSystem.Client.DataManager import DataManager
counterFile = 0
counterDir = 0

def removeDir(d):
    global counterFile, counterDir
    fcc = FileCatalogClient('DataManagement/FileCatalog')
    dm = DataManager()
    result = fcc.listDirectory(d)
    if not result['OK']:
        gLogger.error('Failed to list directory %s: %s' %
                      (d, result['Message']))
        return

    gLogger.notice('Removing dir: %s' % d)

    if result['Value']['Successful'][d]['Files']:
        files = result['Value']['Successful'][d]['Files']
        fileNumber = len(files)
        gLogger.notice(
            'Removing {0} files from dir "{1}"'.format(fileNumber, d))
        counterFile += fileNumber
        dm.removeFile(files)

    if result['Value']['Successful'][d]['SubDirs']:
        for subdir in result['Value']['Successful'][d]['SubDirs']:
            removeDir(subdir)

    counterDir += 1
    fcc.removeDirectory(d)

@DIRACScript()
def main():
    Script.parseCommandLine()

    args = Script.getPositionalArgs()
    if len(args) != 1:
        Script.showHelp(exitCode=1)
    dfcDir = args[0]
    fcc = FileCatalogClient('DataManagement/FileCatalog')
    dm = DataManager()
    retVal = 0
    removeDir(dfcDir)

    gLogger.notice('%s directories and %s files deleted' %
                  (counterDir, counterFile))

    DIRACExit(retVal)


if __name__ == "__main__":
    main()
