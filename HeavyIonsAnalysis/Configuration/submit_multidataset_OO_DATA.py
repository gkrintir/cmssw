#!/usr/bin/env python
from CRABClient.UserUtilities import config

jobTag = "OO_data_filtered"
config = config()
config.section_('General')
config.General.transferOutputs = True
config.General.requestName = jobTag
config.General.workArea = 'crab_projects'

config.section_('JobType')
config.JobType.psetName = 'forest_miniAOD_run3_DATA.py'

config.JobType.pluginName = 'Analysis'
# ppRef_trigger_experiments.py
# config.JobType.outputFiles = ['Run2_pp_data_ijet.root']
# config.JobType.maxMemoryMB = 2000
config.JobType.maxMemoryMB = 3000

config.section_('Data')
config.Data.inputDataset = '/IonPhysics0/OORun2025-PromptReco-v1/MINIAOD'
# config.Data.inputDataset = '/HIMinimumBias0/HIRun2024A-PromptReco-v1/MINIAOD'
config.Data.publication = False
# config.Data.runRange = '306773-306793'
# config.Data.totalUnits = -1
# config.Data.splitting = 'FileBased'
# config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.unitsPerJob = 50000
config.Data.splitting = 'EventAwareLumiBased'
config.Data.outLFNDirBase = '/store/group/phys_top/gkrintir/' + config.General.requestName
# config.Data.outLFNDirBase ='/store/user/vavladim/' + config.General.requestName
# config.Data.outLFNDirBase = '/store/user/lcunquei/Run2_pp_data_CMT'
config.Data.lumiMask = '/afs/cern.ch/work/g/gkrintir/oxy/CMSSW_15_0_11/src/HeavyIonsAnalysis/Configuration/Cert_Collisions2025OO_394153_394217_golden.json'
config.section_('Site')
# config.Site.storageSite = 'T2_IT_Rome'
config.Site.storageSite = 'T2_CH_CERN'
config.Site.blacklist        = ['T3_UK_ScotGrid_GLA','T2_DE_DESY']
print(config)



# (Uncomment if you need extra JDL flags)
# config.section_('Debug')
# config.Debug.extraJDL       = ['+CMS_ALLOW_OVERFLOW=False']

if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    
    dataset_list_2024PbPb = [
    "/IonPhysics0/OORun2025-PromptReco-v1/MINIAOD",
    "/IonPhysics1/OORun2025-PromptReco-v1/MINIAOD",
    ]
    for dataset in dataset_list_2024PbPb:
        config.Data.inputDataset = dataset
        config.General.requestName = 'OO_filtered_' + dataset.split('/')[1]
        crabCommand('submit', config = config)
