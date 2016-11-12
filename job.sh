#!/bin/sh
echo
echo
echo 'START---------------'
echo 'WORKDIR ' ${PWD}
source /afs/cern.ch/cms/cmsset_default.sh
cd /afs/cern.ch/work/g/gkrintir/private/HI/CMSSW_7_5_8_patch3/src
cmsenv
cmsRun miniAOD-prod_PAT.py outputFile='res/miniAOD-prod_PAT_2.root' inputFiles_clear inputFiles_load='tmp/2/list.txt'
echo 'STOP---------------'
echo
echo
