# CRAB3 config template for flashgg
# More options available on the twiki :
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial
# To actually prepare the jobs, please execute prepareCrabJobs.py

from WMCore.Configuration import Configuration
config = Configuration()
import os

config.section_("General")
config.General.requestName = "CMSSW_7_6_1_PCC_ZeroBias4"
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = "Analysis"
config.JobType.psetName = "Run_PixVertex_Event.py"

## to include local file in the sendbox, this will put the file in the directory where cmsRun runs
#config.JobType.inputFiles   = [ os.environ['CMSSW_BASE'] + '/src/'+ 'flashgg/MetaData/data/PY8_RunIISpring15DR74_bx50_MC.db' ]

## incrase jobs time wall, maximum 2750 minutes (~46 hours)
config.JobType.maxJobRuntimeMin = 2750

## config.JobType.maxMemoryMB = 3000 # For memory leaks. NB. will block jobs on many sites
## config.JobType.scriptExe = "cmsWrapper.sh"
#config.JobType.pyCfgParams = ['datasetName=/ZeroBias4/Run2015E-PromptReco-v1/RECO', 'globalTag=74X_mcRun2_asymptotic_v2', 'processType=data']
#config.JobType.sendPythonFolder = True

config.section_("Data")
config.Data.inputDataset = "/ZeroBias4/Run2015E-PromptReco-v1/RECO"
config.Data.inputDBS = 'global'
config.Data.splitting = "LumiBased"
config.Data.unitsPerJob = 10
config.Data.publication = False
config.Data.publishDBS = 'phys03'
#config.Data.outputDatasetTag = 'Run2015E-PromptReco-v1-CMSSW_7_6_1-1-g1613304-v0-Run2015E-PromptReco-v1'
config.Data.outLFNDirBase = "/store/group/comm_luminosity/5TeV/PCC"

config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"
#config.Site.blacklist = ["T2_CH_CERN"]
#config.Site.blacklist = ["T2_UK_London_Brunel","T1_US_FNAL","T2_US_MIT"]

config.Data.lumiMask = "/afs/cern.ch/user/g/gkrintir/github/PCCTools/CMSSW_7_6_1/src/RecoLuminosity/LumiProducer/test/analysis/test/jsondummy_262164.json"
