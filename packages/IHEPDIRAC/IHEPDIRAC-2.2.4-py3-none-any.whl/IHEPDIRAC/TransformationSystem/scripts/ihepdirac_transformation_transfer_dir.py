#!/usr/bin/env python
"""
Start transfer of all files under directory with transformation system
Usage:
 ihepdirac-transformation-transfer-dir [option|cfgfile] TransferName DFCDir SourceSE DestSE

Example: 
 $ihepdirac-transformation-transfer-dir transfer_jinr_ihep_2022 /juno/production/muon/prd010 IHEP-JUNOEOS JINR-EOS

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__RCSID__ = "$Id$"

from DIRAC.Core.Base import Script
from DIRAC.Core.Utilities.DIRACScript import DIRACScript
from DIRAC import S_OK, S_ERROR, gLogger, exit

import sys

from DIRAC.TransformationSystem.Client.Transformation import Transformation
from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

@DIRACScript()
def main():
    Script.parseCommandLine()
    args = Script.getPositionalArgs()
    if len(args) != 4:
        Script.showHelp()
        exit(1)

    transferName = args[0]
    inDir = args[1]
    fromSE = args[2]
    toSE = args[3]

    from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

    fcc = FileCatalogClient('DataManagement/FileCatalog')
    result = fcc.listDirectory(inDir)
    if not result['OK'] or 'Successful' not in result['Value'] or inDir not in result['Value']['Successful']:
       gLogger.error('Can not list directory %s' % inDir)
       exit(2)

    infileList = result['Value']['Successful'][inDir]['Files'].keys()
    infileList.sort()

    print('%s files to transfer' % len(infileList))

    if not infileList:
        gLogger.Info('No file to transfer')
        exit(0)

    t = Transformation( )
    tc = TransformationClient( )
    t.setTransformationName(transferName) # Must be unique
    t.setTransformationGroup("Transfer")
    t.setType("Transfer-JUNO")
    #t.setPlugin("Standard") # Not needed. The default is 'Standard'
    t.setDescription("Test Data Transfer")
    t.setLongDescription( "Long description of Data Transfer" ) # Mandatory
    t.setGroupSize(3) # Here you specify how many files should be grouped within he same request, e.g. 100

    transBody = [ ( "ReplicateAndRegister", { "SourceSE": fromSE, "TargetSE": toSE }) ]

    t.setBody ( transBody ) # Mandatory

    result = t.addTransformation() # Transformation is created here
    if not result['OK']:
        gLogger.error('Can not add transformation: %s' % result['Message'])
        exit(2)

    t.setStatus("Active")
    t.setAgentType("Automatic")
    transID = t.getTransformationID()

    result = tc.addFilesToTransformation(transID['Value'], infileList) # Files are added here
    if not result['OK']:
        gLogger.error('Can not add files to transformation: %s' % result['Message'])
        exit(2)

    result = tc.setTransformationParameter( transID['Value'], 'Status', 'Flush' )
    if not result['OK']:
        gLogger.error('Can not flush transformation: %s' % result['Message'])
        exit(2)

if __name__ == "__main__":
    main()
