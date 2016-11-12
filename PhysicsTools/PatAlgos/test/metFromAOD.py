from PhysicsTools.PatAlgos.patTemplate_cfg import *
#from PhysicsTools.PatAlgos.patTemplate_cfg import cms, process


# Set the process options -- Display summary at the end, enable unscheduled execution
process.options.allowUnscheduled = cms.untracked.bool(True)
process.options.wantSummary = cms.untracked.bool(False) 

# Load the standard set of configuration modules
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# How many events to process
process.maxEvents = cms.untracked.PSet( 
   input = cms.untracked.int32(100)
)

#configurable options =======================================================================
runOnData=False #data/MC switch
usePrivateSQlite=False #use external JECs (sqlite file)
useHFCandidates=False #create an additionnal NoHF slimmed MET collection if the option is set to false
redoPuppi=False # rebuild puppiMET
#===================================================================
print "here 0"
from Configuration.AlCa.GlobalTag import GlobalTag
if runOnData:
  process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
else:
  process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

print "here 1"
'''
from CondCore.DBCommon.CondDBSetup_cfi import *
##___________________________External JER file________________________________||
##https://github.com/cms-jet/JRDatabase/tree/master/SQLiteFiles
process.jer = cms.ESSource("PoolDBESSource",CondDBSetup,
                           #connect = cms.string( "frontier://FrontierPrep/CMS_COND_PHYSICSTOOLS"),
                           #connect = cms.string( "frontier://FrontierPrep/CMS_CONDITIONS"),
                           connect = cms.string("sqlite:PhysicsTools/PatUtils/data/Summer15_25nsV6_MC.db"),
                           toGet =  cms.VPSet(
    cms.PSet(
      record = cms.string('JetResolutionRcd'),
      #tag    = cms.string('JR_MC_PtResolution_Summer15_25nsV6_AK4PF'),
      tag    = cms.string('JR_Fall15_25nsV2_MC_PtResolution_AK4PFchs'),
      label  = cms.untracked.string('AK4PFchs_pt')
      ),
    cms.PSet(
      record = cms.string("JetResolutionRcd"),
      #tag = cms.string("JR_MC_PhiResolution_Summer15_25nsV6_AK4PF"),
      tag = cms.string("JR_Fall15_25nsV2_MC_PhiResolution_AK4PFchs"),
      label= cms.untracked.string("AK4PFchs_phi")
      ),
    cms.PSet(
      record = cms.string('JetResolutionScaleFactorRcd'),
      #tag    = cms.string('JR_DATAMCSF_Summer15_25nsV6_AK4PFchs'),
      tag    = cms.string('JR_Fall15_25nsV2_MC_SF_AK4PFchs'),
      label  = cms.untracked.string('AK4PFchs')
      ),
    
    ) )
process.es_prefer_jer = cms.ESPrefer("PoolDBESSource",'jer')
'''
### =====================================================================================================
# Define the input source
if runOnData:
  #fname = '/store/relval/CMSSW_8_0_20/JetHT/RAW-RECO/HighMET-80X_dataRun2_relval_Candidate_2016_09_02_10_27_40_RelVal_jetHT2016B-v1/00000/187EA7A4-BA7A-E611-AC32-0025905B85EE.root'
  fname = 'file:/afs/cern.ch/work/g/gkrintir/private/HI/CMSSW_7_5_8_patch3/src/PhysicsTools/PatAlgos/test/4A649A7F-308E-E511-BB4A-02163E013859.root'
else:
  fname = 'file:/afs/cern.ch/work/g/gkrintir/private/HI/CMSSW_7_5_8_patch3/src/B4EF099A-DDE3-E511-8C66-D4856459BE56.root'
    
# Define the input source
process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring([ fname ])
)

print "here 2"
#process.load('METStudies.PU100Run.CfiFileAOD_cfi')
#process.dump=cms.EDAnalyzer('EventContentAnalyzer')

import PhysicsTools.PatAlgos.tools.helpers as configtools
process.load("PhysicsTools.PatAlgos.slimming.slimming_cff")
process.load("PhysicsTools.PatAlgos.producersLayer1.jetProducer_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi")
process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")
process.load("PhysicsTools.PatAlgos.cleaningLayer1.cleanPatCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.countPatCandidates_cff")

print "here 3"
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMETCorrectionsAndUncertainties
runMETCorrectionsAndUncertainties(process,
                                  correctionLevel=["T1"],
                                  onMiniAOD=False,
                                  runOnData=runOnData
                                  #pfCandCollection=cms.InputTag('particleFlow')
                                  )
print "here 4"
if runOnData:
  from PhysicsTools.PatAlgos.tools.coreTools import runOnData
  runOnData( process,  outputModules = [])

print "here 5"
#if not useHFCandidates:
#  process.noHFCands = cms.EDFilter("CandPtrSelector",
#                                   src=cms.InputTag("packedPFCandidates"),
#                                   cut=cms.string("abs(pdgId)!=1 && abs(pdgId)!=2 && abs(eta)<3.0")
#                                   )
    
#if not useHFCandidates:
#print "here"
#runMETCorrectionsAndUncertainties(process,
#                                  runOnData=runOnData,
#                                  pfCandCollection=cms.InputTag("noHFCands"),
                                  #reclusterJets=True, #needed for NoHF
                                  #recoMetFromPFCs=True, #needed for NoHF
                                  #postfix="Test"
#                                  )    



process.out.outputCommands = cms.untracked.vstring( "keep *_*pfMet_*_*",                                                                       
                                                    "keep *_*patPFMet*_*_*",                                                                    
                                                    ) 

process.out.fileName = cms.untracked.string('corMETMiniAOD.root')
#process.p = cms.Path(process.demo)
process.MINIAODSIMoutput_step = cms.EndPath(process.out)


