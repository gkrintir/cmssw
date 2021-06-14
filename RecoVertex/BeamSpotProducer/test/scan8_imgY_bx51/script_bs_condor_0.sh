#!/bin/tcsh

# pushd $CMSSW_BASE/src
pushd /afs/cern.ch/work/g/gkrintir/private/testt/CMSSW_9_4_13/src/
eval `scramv1 runtime -csh`
popd
# mkdir tmp
# setenv TMPDIR $PWD/tmp
# mkdir job
# cd job

cp /afs/cern.ch/work/g/gkrintir/private/testt/CMSSW_9_4_13/src/RecoVertex/BeamSpotProducer/test/scan8_imgY_bx51/filelist.py .
cmsRun /afs/cern.ch/work/g/gkrintir/private/testt/CMSSW_9_4_13/src/RecoVertex/BeamSpotProducer/test/scan8_imgY_bx51/BeamFit_LumiBased_NoRefit_Run263234_backup.py
# cp $CMSSW_BASE/src/RecoVertex/BeamSpotProducer/test/scan8_imgY_bx51/filelist_318984_scanX1_ZBAOD.py .
# cmsRun $CMSSW_BASE/src/RecoVertex/BeamSpotProducer/test/scan8_imgY_bx51/BeamFit_LumiBased_NoRefit_Template_1464336285_1464336313.py

cp -v BeamFit_LumiBased_alcareco_Run263234.txt $LS_SUBCWD
if [ $? -ne 0 ]; then
  echo 'ERROR: problem copying job directory back'
else
  echo 'job directory copy succeeded'
fi
