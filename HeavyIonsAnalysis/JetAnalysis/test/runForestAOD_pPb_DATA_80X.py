### HiForest Configuration
# Collisions: pp
# Type: MC
# Input: AOD

import FWCore.ParameterSet.Config as cms
process = cms.Process('HiForest')
process.options = cms.untracked.PSet()

#####################################################################################
# HiForest labelling info
#####################################################################################

process.load("HeavyIonsAnalysis.JetAnalysis.HiForest_cff")
process.HiForest.inputLines = cms.vstring("HiForest V3",)
import subprocess
version = subprocess.Popen(["(cd $CMSSW_BASE/src && git describe --tags)"], stdout=subprocess.PIPE, shell=True).stdout.read()

if version == '':
    version = 'no git info'
process.HiForest.HiForestVersion = cms.string(version)

#####################################################################################
# Input source
#####################################################################################

process.source = cms.Source("PoolSource",
                            duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
                            fileNames = cms.untracked.vstring(
				'file:/afs/cern.ch/work/g/gkrintir/private/HI/MET/CMSSW_8_0_23/src/HeavyIonsAnalysis/JetAnalysis/test/samples/C23C1F65-5EAE-E611-A754-02163E014256.root'
				)
)

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1))


#####################################################################################
# Load Global Tag, Geometry, etc.
#####################################################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("CondCore.DBCommon.CondDBCommon_cfi")
 
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_miniAODv2_v1', '')
process.HiForest.GlobalTagLabel = process.GlobalTag.globaltag


# Customization
from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import overrideJEC_pPb8TeV
process = overrideJEC_pPb8TeV(process)

process.GlobalTag.toGet.extend([
	cms.PSet(record = cms.string("HeavyIonRcd"),
		 #tag = cms.string("CentralityTable_HFtowersPlusTrunc200_EPOS8TeV_v80x01_mc"),
                 tag = cms.string("CentralityTable_HFtowersPlusTrunc200_EPOS5TeV_v80x01_mc"),
                 connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
                 label = cms.untracked.string("HFtowersPlusTruncEpos")
             ),
	cms.PSet(record = cms.string("L1TGlobalPrescalesVetosRcd"),
                tag = cms.string("L1TGlobalPrescalesVetos_Stage2v0_hlt"),
                connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
                )
])

#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string("HiForestAOD.root"))

#####################################################################################
# Additional Reconstruction and Analysis: Main Body
#####################################################################################

####################################################################################

#############################
# Jets
#############################

process.load("HeavyIonsAnalysis.JetAnalysis.FullJetSequence_DataPPb")

#####################################################################################

############################
# Event Analysis
############################

## temporary centrality bin
process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("pACentrality")
process.centralityBin.centralityVariable = cms.string("HFtowersPlusTrunc")
#process.centralityBin.nonDefaultGlauberModel = cms.string("Hydjet_Drum")
process.centralityBin.nonDefaultGlauberModel = cms.string("Epos")

process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cff')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_pPb_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi') #use data version to avoid PbPb MC
process.hiEvtAnalyzer.Vertex = cms.InputTag("offlinePrimaryVertices")
process.hiEvtAnalyzer.doCentrality = cms.bool(True)
process.hiEvtAnalyzer.CentralitySrc = cms.InputTag("pACentrality")
process.hiEvtAnalyzer.CentralityBinSrc = cms.InputTag("centralityBin","HFtowersPlusTrunc")
process.hiEvtAnalyzer.doEvtPlane = cms.bool(False)
process.hiEvtAnalyzer.doMC = cms.bool(True) #general MC info
process.hiEvtAnalyzer.doHiMC = cms.bool(False) #HI specific MC info

process.load('HeavyIonsAnalysis.EventAnalysis.runanalyzer_cff')
process.load("HeavyIonsAnalysis.JetAnalysis.pfcandAnalyzer_pp_cfi")
process.pfcandAnalyzer.pfPtMin = 0
process.pfcandAnalyzer.pfCandidateLabel = cms.InputTag("particleFlow")
process.pfcandAnalyzer.doVS = cms.untracked.bool(False)
process.pfcandAnalyzer.doUEraw_ = cms.untracked.bool(False)

#####################################################################################

#########################
# Track Analyzer
#########################
process.load('HeavyIonsAnalysis.JetAnalysis.ExtraTrackReco_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.TrkAnalyzers_cff')

# Use this instead for track corrections
## process.load('HeavyIonsAnalysis.JetAnalysis.TrkAnalyzers_Corr_cff')

#####################################################################################

#####################
# photons
######################
process.load('HeavyIonsAnalysis.PhotonAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.gsfElectronLabel   = cms.InputTag("gedGsfElectrons")
process.ggHiNtuplizer.recoPhotonHiIsolationMap = cms.InputTag('photonIsolationHIProducerpp')
process.ggHiNtuplizer.VtxLabel           = cms.InputTag("offlinePrimaryVertices")
process.ggHiNtuplizer.particleFlowCollection = cms.InputTag("particleFlow")
process.ggHiNtuplizer.doVsIso            = cms.bool(False)
process.ggHiNtuplizer.doElectronVID      = cms.bool(True)
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel = cms.InputTag("patPFMetT1","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_EESUp = cms.InputTag("patPFMetT1ElectronEnUp","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_EESDo = cms.InputTag("patPFMetT1ElectronEnDown","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_MESUp = cms.InputTag("patPFMetT1MuonEnUp","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_MESDo = cms.InputTag("patPFMetT1MuonEnDown","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_PESUp = cms.InputTag("patPFMetT1PhotonEnUp","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_PESDo = cms.InputTag("patPFMetT1PhotonEnDown","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_TESUp = cms.InputTag("patPFMetT1TauEnUp","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_TESDo = cms.InputTag("patPFMetT1TauEnDown","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_UESUp = cms.InputTag("patPFMetT1UnclusteredEnUp","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_UESDo = cms.InputTag("patPFMetT1UnclusteredEnDown","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_JESUp = cms.InputTag("patPFMetT1JetEnUp","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_JESDo = cms.InputTag("patPFMetT1JetEnDown","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_JERUp = cms.InputTag("patPFMetT1JetResEnUp","","HiForest")
process.ggHiNtuplizer.newCorrectedSlimmedMetLabel_JERDo = cms.InputTag("patPFMetT1JetResEnDown","","HiForest")

process.ggHiNtuplizerGED = process.ggHiNtuplizer.clone(recoPhotonSrc = cms.InputTag('gedPhotons'),
                                                       recoPhotonHiIsolationMap = cms.InputTag('photonIsolationHIProducerppGED'))

####################################################################################
#####################
# Electron ID
#####################

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format to be processed
# DataFormat.AOD or DataFormat.MiniAOD
dataFormat = DataFormat.AOD
switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce. Check here https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Working_points_for_2016_data_for
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff']

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
#####################################################################################
#####################
# Rechit analyzer
#####################
process.load('HeavyIonsAnalysis.JetAnalysis.rechitanalyzer_pp_cfi')
process.rechitanalyzer.doVS = cms.untracked.bool(False)
process.rechitanalyzer.doEcal = cms.untracked.bool(False)
process.rechitanalyzer.doHcal = cms.untracked.bool(False)
process.rechitanalyzer.doHF = cms.untracked.bool(False)
process.rechitanalyzer.JetSrc = cms.untracked.InputTag("ak4CaloJets")
process.pfTowers.JetSrc = cms.untracked.InputTag("ak4CaloJets")

#####################
# New rho analyzer
#####################
process.load('HeavyIonsAnalysis.JetAnalysis.hiFJRhoAnalyzer_cff')

#####################
# Muon Analyzer
#####################
process.load('HeavyIonsAnalysis.MuonAnalysis.hltMuTree_cfi')
process.hltMuTree.vertices = cms.InputTag("offlinePrimaryVertices")

#########################
# Main analysis list
#########################
process.ana_step = cms.Path(process.hltanalysis *
			    process.hltobject *
                            process.centralityBin *
			    process.hiEvtAnalyzer *
                            process.jetSequences +
                            process.egmGsfElectronIDSequence + #Should be added in the path for VID module
                            process.ggHiNtuplizer +
                            process.ggHiNtuplizerGED +
                            process.hiFJRhoAnalyzer +
			    process.pfcandAnalyzer +
			    process.hltMuTree +
                            process.HiForest +
			    process.trackSequencesPP +
                            process.runAnalyzer +
                            process.rechitanalyzer
)

#####################################################################################

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string("test.root"),
    #SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring(
        "keep *_*patMets_*_*",
        "keep *_*patMetPhi_*_*",
        "keep *_*patPFMetT1*_*_*"
        )
)


#########################
# Event Selection
#########################

process.load('HeavyIonsAnalysis.JetAnalysis.EventSelection_cff')
process.pHBHENoiseFilterResultProducer = cms.Path( process.HBHENoiseFilterResultProducer )
process.HBHENoiseFilterResult = cms.Path(process.fHBHENoiseFilterResult)
process.HBHENoiseFilterResultRun1 = cms.Path(process.fHBHENoiseFilterResultRun1)
process.HBHENoiseFilterResultRun2Loose = cms.Path(process.fHBHENoiseFilterResultRun2Loose)
process.HBHENoiseFilterResultRun2Tight = cms.Path(process.fHBHENoiseFilterResultRun2Tight)
process.HBHEIsoNoiseFilterResult = cms.Path(process.fHBHEIsoNoiseFilterResult)

process.PAprimaryVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2 && tracksSize >= 2"),
    filter = cms.bool(True), # otherwise it won't filter the events
)

process.NoScraping = cms.EDFilter("FilterOutScraping",
 applyfilter = cms.untracked.bool(True),
 debugOn = cms.untracked.bool(False),
 numtrack = cms.untracked.uint32(10),
 thresh = cms.untracked.double(0.25)
)

process.pPAprimaryVertexFilter = cms.Path(process.PAprimaryVertexFilter)
process.pBeamScrapingFilter=cms.Path(process.NoScraping)

process.load("HeavyIonsAnalysis.VertexAnalysis.PAPileUpVertexFilter_cff")

process.pVertexFilterCutG = cms.Path(process.pileupVertexFilterCutG)
process.pVertexFilterCutGloose = cms.Path(process.pileupVertexFilterCutGloose)
process.pVertexFilterCutGtight = cms.Path(process.pileupVertexFilterCutGtight)
process.pVertexFilterCutGplus = cms.Path(process.pileupVertexFilterCutGplus)
process.pVertexFilterCutE = cms.Path(process.pileupVertexFilterCutE)
process.pVertexFilterCutEandG = cms.Path(process.pileupVertexFilterCutEandG)

process.pAna = cms.EndPath(process.skimanalysis)

# Customization
process.o = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.ana_step,process.o  )
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)
from FWCore.ParameterSet.Utilities import cleanUnscheduled
process=cleanUnscheduled(process)



from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMETCorrectionsAndUncertainties


import PhysicsTools.PatAlgos.tools.helpers as configtools

process.load("PhysicsTools.PatAlgos.slimming.slimming_cff")
process.load("PhysicsTools.PatAlgos.producersLayer1.jetProducer_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi")
process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")
process.load("PhysicsTools.PatAlgos.cleaningLayer1.cleanPatCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.countPatCandidates_cff")

runOnData=True #data/MC switch
usePrivateSQlite=False #use external JECs (sqlite file)
useHFCandidates=False #create an additionnal NoHF slimmed MET collection if the option is set to false
redoPuppi=False # rebuild puppiMET



runMETCorrectionsAndUncertainties(process,
                                  correctionLevel=["T1"],
                                  onMiniAOD=False,
                                  runOnData=runOnData,
                                  pfCandCollection=cms.InputTag('particleFlow')
                                  )


if runOnData:
  from PhysicsTools.PatAlgos.tools.coreTools import runOnData
  runOnData( process,  outputModules = [])
