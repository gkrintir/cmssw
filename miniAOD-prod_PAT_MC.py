# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: miniAOD-prod -s PAT --eventcontent MINIAODSIM --runUnscheduled --mc --filein /store/relval/CMSSW_7_4_1/RelValTTbar_13/GEN-SIM-RECO/PU50ns_MCRUN2_74_V8_gensim71X-v1/00000/06ACC5B7-7FEC-E411-8CB1-0025905964BA.root --conditions MCRUN2_74_V8 -n 100 --no_exec
import FWCore.ParameterSet.Config as cms

process = cms.Process('PAT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/afs/cern.ch/work/g/gkrintir/private/HI/CMSSW_7_5_8_patch3/src/B4EF099A-DDE3-E511-8C66-D4856459BE56.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('miniAOD-prod nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('miniAOD-prod_PAT.root'),
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

# Additional output definition


from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '75X_mcRun2_asymptotic_ppAt5TeV_v3', '')

# Customization                                                                                                                                                                                             
from CondCore.DBCommon.CondDBSetup_cfi import *
##___________________________External JEC file________________________________||

process.jec = cms.ESSource("PoolDBESSource",CondDBSetup,
                           #connect = cms.string( "frontier://FrontierPrep/CMS_COND_PHYSICSTOOLS"),
                           #connect = cms.string( "frontier://FrontierPrep/CMS_CONDITIONS"),
                           #connect = cms.string("sqlite:PhysicsTools/PatUtils/data/Summer15_25nsV6_MC.db"),
                           connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
                           #DBParameters = cms.PSet(
                           #  messageLevel = cms.untracked.int32(0)
                           #  ),
                           toGet =  cms.VPSet(
        cms.PSet(record = cms.string("JetCorrectionsRecord"),
                 tag = cms.string("JetCorrectorParametersCollection_HI_PythiaCUETP8M1_5020GeV_753p1_v12_AK4PF_offline"),
                 #connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
                 label = cms.untracked.string("AK4PF_offline")
                 ),
                 ))

process.es_prefer_jec = cms.ESPrefer("PoolDBESSource",'jec')


process.jer = cms.ESSource("PoolDBESSource",CondDBSetup,
                           connect = cms.string("sqlite:Fall15_25nsV2_MC.db"), #PhysicsTools/PatUtils/data
                           toGet =  cms.VPSet(
    cms.PSet(
      record = cms.string('JetResolutionRcd'),
      #tag    = cms.string('JR_MC_PtResolution_Summer15_25nsV6_AK4PF'),
      tag    = cms.string('JR_Fall15_25nsV2_MC_PtResolution_AK4PFchs'),
      label  = cms.untracked.string('AK4PFchs_pt')
      ),
    cms.PSet(
      record = cms.string('JetResolutionRcd'),
      #tag = cms.string("JR_MC_PhiResolution_Summer15_25nsV6_AK4PF"),
      tag = cms.string('JR_Fall15_25nsV2_MC_PhiResolution_AK4PFchs'),
      label= cms.untracked.string('AK4PFchs_phi')
      ),
    cms.PSet(
      record = cms.string('JetResolutionScaleFactorRcd'),
      #tag    = cms.string('JR_DATAMCSF_Summer15_25nsV6_AK4PFchs'),
      tag    = cms.string('JR_Fall15_25nsV2_MC_SF_AK4PFchs'),
      label  = cms.untracked.string('AK4PFchs')
      ),
    
    ) )
process.es_prefer_jer = cms.ESPrefer("PoolDBESSource",'jer')

# Path and EndPath definitions
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_CSCTightHalo2015Filter = cms.Path(process.CSCTightHalo2015Filter)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_CSCTightHaloTrkMuUnvetoFilter = cms.Path(process.CSCTightHaloTrkMuUnvetoFilter)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.Flag_HBHENoiseFilter,process.Flag_HBHENoiseIsoFilter,process.Flag_CSCTightHaloFilter,process.Flag_CSCTightHaloTrkMuUnvetoFilter,process.Flag_CSCTightHalo2015Filter,process.Flag_hcalLaserEventFilter,process.Flag_EcalDeadCellTriggerPrimitiveFilter,process.Flag_EcalDeadCellBoundaryEnergyFilter,process.Flag_goodVertices,process.Flag_eeBadScFilter,process.Flag_ecalLaserCorrFilter,process.Flag_trkPOGFilters,process.Flag_trkPOG_manystripclus53X,process.Flag_trkPOG_toomanystripclus53X,process.Flag_trkPOG_logErrorTooManyClusters,process.Flag_METFilters,process.endjob_step,process.MINIAODSIMoutput_step)

#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)
process.load('Configuration.StandardSequences.PATMC_cff')
from FWCore.ParameterSet.Utilities import cleanUnscheduled
process=cleanUnscheduled(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 

#call to customisation function miniAOD_customizeAllMC imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)

# End of customisation functions
