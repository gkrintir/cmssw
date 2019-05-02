### HiForest Configuration
# Collisions: PbPb
# Type: Embedded Monte Carlo
# Input: AOD

import FWCore.ParameterSet.Config as cms
process = cms.Process('HiForest')

###############################################################################
# HiForest labelling info
###############################################################################

process.load("HeavyIonsAnalysis.JetAnalysis.HiForest_cff")
process.HiForest.inputLines = cms.vstring("HiForest 103X")
import subprocess, os
version = subprocess.check_output(['git',
    '-C', os.path.expandvars('$CMSSW_BASE/src'), 'describe', '--tags'])
if version == '':
    version = 'no git info'
process.HiForest.HiForestVersion = cms.string(version)

###############################################################################
# Input source
###############################################################################

process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
        "file:/afs/cern.ch/work/r/rbi/public/forest/HINPbPbAutumn18DR_Pythia8_Ze10e10_TuneCP5_5p02TeV_AODSIM.root"
        ),
    )

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
    )

###############################################################################
# Load Global Tag, Geometry, etc.
###############################################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2018_realistic_hi', '')
process.HiForest.GlobalTagLabel = process.GlobalTag.globaltag

print('\n\033[31m~*~ USING CENTRALITY TABLE FOR Hydjet Drum5F ~*~\033[0m\n')
process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
process.GlobalTag.toGet.extend([
    cms.PSet(record = cms.string("HeavyIonRcd"),
        # tag = cms.string("CentralityTable_HFtowers200_HydjetDrum5Ev8_v1030pre5x02_mc"),
        tag = cms.string("CentralityTable_HFtowers200_HydjetDrum5F_v1032x01_mc"),
        connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
        label = cms.untracked.string("HFtowers")
        ),
    ])

from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import overrideJEC_PbPb5020
process = overrideJEC_PbPb5020(process)

process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")

###############################################################################
# Define tree output
###############################################################################

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("HiForestAOD.root"))

###############################################################################
# Additional Reconstruction and Analysis: Main Body
###############################################################################

#############################
# Jets
#############################
# jet reco sequence
process.load('HeavyIonsAnalysis.JetAnalysis.fullJetSequence_pponAA_JEC_cff')

# temporary (all 4 because its the only correction that loads
process.ak1Calocorr.payload = "AK4Calo"
process.akPu1Calocorr.payload = "AK4Calo"
process.ak1PFcorr.payload = "AK4PF"
process.akPu1PFcorr.payload = "AK4PF"
process.akCs1PFcorr.payload = "AK4PF"

process.ak2Calocorr.payload = "AK4Calo"
process.akPu2Calocorr.payload = "AK4Calo"
process.ak2PFcorr.payload = "AK4PF"
process.akPu2PFcorr.payload = "AK4PF"
process.akCs2PFcorr.payload = "AK4PF"

process.ak3Calocorr.payload = "AK4Calo"
process.akPu3Calocorr.payload = "AK4Calo"
process.ak3PFcorr.payload = "AK4PF"
process.akPu3PFcorr.payload = "AK4PF"
process.akCs3PFcorr.payload = "AK4PF"

process.ak4Calocorr.payload = "AK4Calo"
process.akPu4Calocorr.payload = "AK4Calo"
process.ak4PFcorr.payload = "AK4PF"
process.akPu4PFcorr.payload = "AK4PF"
process.akCs4PFcorr.payload = "AK4PF"
process.akPu4PFJets.jetPtMin = 1

process.ak5Calocorr.payload = "AK4Calo"
process.akPu5Calocorr.payload = "AK4Calo"
process.ak5PFcorr.payload = "AK4PF"
process.akPu5PFcorr.payload = "AK4PF"
process.akCs5PFcorr.payload = "AK4PF"

process.ak6Calocorr.payload = "AK4Calo"
process.akPu6Calocorr.payload = "AK4Calo"
process.ak6PFcorr.payload = "AK4PF"
process.akPu6PFcorr.payload = "AK4PF"
process.akCs6PFcorr.payload = "AK4PF"

# Add a second hiFJRhoProducer and hiFJGridEmptyAreaCalculator with finer binning 
process.hiFJRhoProducerFiner = process.hiFJRhoProducer.clone()
process.hiFJRhoProducerFiner.etaRanges = cms.vdouble(-5., -4., -3, -2.5, -2.0, -0.8, 0.8, 2.0, 2.5, 3., 4., 5.)
process.hiFJGridEmptyAreaCalculatorFiner = process.hiFJGridEmptyAreaCalculator.clone()
process.hiFJGridEmptyAreaCalculatorFiner.mapEtaEdges = cms.InputTag('hiFJRhoProducerFiner','mapEtaEdges')
process.hiFJGridEmptyAreaCalculatorFiner.mapToRho = cms.InputTag('hiFJRhoProducerFiner','mapToRho')
process.hiFJGridEmptyAreaCalculatorFiner.mapToRhoM = cms.InputTag('hiFJRhoProducerFiner','mapToRhoM')

process.load('HeavyIonsAnalysis.JetAnalysis.hiFJRhoAnalyzer_cff')
# Run a second hiFJRhoAnalyzer using as input the modified hiFJRhoProducer and hiFJGridEmptyAreaCalculator
process.hiFJRhoAnalyzer2 = process.hiFJRhoAnalyzer.clone()
process.hiFJRhoAnalyzer2.etaMap        = cms.InputTag('hiFJRhoProducerFiner','mapEtaEdges','HiForest')
process.hiFJRhoAnalyzer2.rho           = cms.InputTag('hiFJRhoProducerFiner','mapToRho')
process.hiFJRhoAnalyzer2.rhom         = cms.InputTag('hiFJRhoProducerFiner','mapToRhoM')
process.hiFJRhoAnalyzer2.ptJets        = cms.InputTag('hiFJRhoProducerFiner','ptJets')
process.hiFJRhoAnalyzer2.etaJets       = cms.InputTag('hiFJRhoProducerFiner','etaJets')
process.hiFJRhoAnalyzer2.areaJets      = cms.InputTag('hiFJRhoProducerFiner','areaJets')
process.hiFJRhoAnalyzer2.rhoCorr       = cms.InputTag('hiFJGridEmptyAreaCalculatorFiner','mapToRhoCorr')
process.hiFJRhoAnalyzer2.rhomCorr      = cms.InputTag('hiFJGridEmptyAreaCalculatorFiner','mapToRhoMCorr')
process.hiFJRhoAnalyzer2.rhoCorr1Bin   = cms.InputTag('hiFJGridEmptyAreaCalculatorFiner','mapToRhoCorr1Bin')
process.hiFJRhoAnalyzer2.rhomCorr1Bin  = cms.InputTag('hiFJGridEmptyAreaCalculatorFiner','mapToRhoMCorr1Bin')
process.hiFJRhoAnalyzer2.rhoGrid       = cms.InputTag('hiFJGridEmptyAreaCalculatorFiner','mapRhoVsEtaGrid')
process.hiFJRhoAnalyzer2.meanRhoGrid   = cms.InputTag('hiFJGridEmptyAreaCalculatorFiner','mapMeanRhoVsEtaGrid')
process.hiFJRhoAnalyzer2.etaMaxRhoGrid = cms.InputTag('hiFJGridEmptyAreaCalculatorFiner','mapEtaMaxGrid')
process.hiFJRhoAnalyzer2.etaMinRhoGrid = cms.InputTag('hiFJGridEmptyAreaCalculatorFiner','mapEtaMinGrid')

process.load("HeavyIonsAnalysis.JetAnalysis.pfcandAnalyzer_cfi")
process.pfcandAnalyzer.doTrackMatching  = cms.bool(True)

###############################################################################

#############################
# Gen Analyzer
#############################
process.load('HeavyIonsAnalysis.EventAnalysis.runanalyzer_cfi')
process.load('HeavyIonsAnalysis.TrackAnalysis.HiGenAnalyzer_cfi')
# making cuts looser so that we can actually check dNdEta
process.HiGenParticleAna.ptMin = cms.untracked.double(0.4) # default is 5
process.HiGenParticleAna.etaMax = cms.untracked.double(5.) # default is 2

###############################################################################

############################
# Event Analysis
############################
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_mc_cfi')
process.hiEvtAnalyzer.doMC = cms.bool(True) # general MC info
process.hiEvtAnalyzer.doHiMC = cms.bool(True) # HI specific MC info
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')

###############################################################################

#########################
# Track Analyzer
#########################
process.load('HeavyIonsAnalysis.TrackAnalysis.ExtraTrackReco_cff')
process.load('HeavyIonsAnalysis.TrackAnalysis.TrkAnalyzers_cff')

# Use this instead for track corrections
# process.load('HeavyIonsAnalysis.TrackAnalysis.TrkAnalyzers_Corr_cff')

###############################################################################

#####################
# Photons
#####################
process.load('HeavyIonsAnalysis.PhotonAnalysis.ggHiNtuplizer_cfi')

###############################################################################

#######################
# B-tagging
######################
# replace pp CSVv2 with PbPb CSVv2 (positive and negative taggers unchanged!)
process.load('RecoBTag.CSVscikit.csvscikitTagJetTags_cfi')
process.load('RecoBTag.CSVscikit.csvscikitTaggerProducer_cfi')
process.akPu4PFCombinedSecondaryVertexV2BJetTags = process.pfCSVscikitJetTags.clone()
process.akPu4PFCombinedSecondaryVertexV2BJetTags.tagInfos = cms.VInputTag(
    cms.InputTag("akPu4PFImpactParameterTagInfos"),
    cms.InputTag("akPu4PFSecondaryVertexTagInfos"))
process.akCs4PFCombinedSecondaryVertexV2BJetTags = process.pfCSVscikitJetTags.clone()
process.akCs4PFCombinedSecondaryVertexV2BJetTags.tagInfos = cms.VInputTag(
    cms.InputTag("akCs4PFImpactParameterTagInfos"),
    cms.InputTag("akCs4PFSecondaryVertexTagInfos"))
process.akPu4CaloCombinedSecondaryVertexV2BJetTags = process.pfCSVscikitJetTags.clone()
process.akPu4CaloCombinedSecondaryVertexV2BJetTags.tagInfos = cms.VInputTag(
    cms.InputTag("akPu4CaloImpactParameterTagInfos"),
    cms.InputTag("akPu4CaloSecondaryVertexTagInfos"))

# trained on CS jets
process.CSVscikitTags.weightFile = cms.FileInPath(
    'HeavyIonsAnalysis/JetAnalysis/data/TMVA_Btag_CsJets_PbPb_BDTG.weights.xml')

###############################################################################

#########################
# RecHits & pfTowers (HF, Castor & ZDC)
#########################
process.load('HeavyIonsAnalysis.JetAnalysis.rechitanalyzer_cfi')

###############################################################################

#########################
# Main analysis list
#########################

process.ana_step = cms.Path(
    process.HiForest +
    process.runAnalyzer +
    process.hltanalysis +
    process.centralityBin +
    process.hiEvtAnalyzer +
    process.HiGenParticleAna +
    process.genSignalSequence +
    process.jetSequence +
    process.hiFJRhoProducerFiner+
    process.hiFJGridEmptyAreaCalculatorFiner+
    process.ggHiNtuplizer +
    process.ggHiNtuplizerGED +
    process.hiFJRhoAnalyzer +
    process.pfcandAnalyzer +
    process.pfcandAnalyzerCS +
    process.trackSequencesPP +
    process.rechitanalyzerpp
    )

# # edm output for debugging purposes
# process.output = cms.OutputModule(
#     "PoolOutputModule",
#     fileName = cms.untracked.string('HiForestEDM.root'),
#     outputCommands = cms.untracked.vstring(
#         'keep *',
#         # drop aliased products
#         'drop *_akULPu3PFJets_*_*',
#         'drop *_akULPu4PFJets_*_*',
#         )
#     )

# process.output_path = cms.EndPath(process.output)

###############################################################################

#########################
# Event Selection
#########################

process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')
process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter)
process.pBeamScrapingFilter = cms.Path(process.beamScrapingFilter)
process.collisionEventSelectionAOD = cms.Path(process.collisionEventSelectionAOD)
process.collisionEventSelectionAODv2 = cms.Path(process.collisionEventSelectionAODv2)

process.load('HeavyIonsAnalysis.Configuration.hfCoincFilter_cff')
process.phfCoincFilter1Th3 = cms.Path(process.hfCoincFilterTh3)
process.phfCoincFilter2Th3 = cms.Path(process.hfCoincFilter2Th3)
process.phfCoincFilter3Th3 = cms.Path(process.hfCoincFilter3Th3)
process.phfCoincFilter4Th3 = cms.Path(process.hfCoincFilter4Th3)
process.phfCoincFilter5Th3 = cms.Path(process.hfCoincFilter5Th3)
process.phfCoincFilter1Th4 = cms.Path(process.hfCoincFilterTh4)
process.phfCoincFilter2Th4 = cms.Path(process.hfCoincFilter2Th4)
process.phfCoincFilter3Th4 = cms.Path(process.hfCoincFilter3Th4)
process.phfCoincFilter4Th4 = cms.Path(process.hfCoincFilter4Th4)
process.phfCoincFilter5Th4 = cms.Path(process.hfCoincFilter5Th4)
process.phfCoincFilter1Th5 = cms.Path(process.hfCoincFilterTh5)
process.phfCoincFilter4Th2 = cms.Path(process.hfCoincFilter4Th2)

process.load("HeavyIonsAnalysis.VertexAnalysis.PAPileUpVertexFilter_cff")
process.pVertexFilterCutG = cms.Path(process.pileupVertexFilterCutG)
process.pVertexFilterCutGloose = cms.Path(process.pileupVertexFilterCutGloose)
process.pVertexFilterCutGtight = cms.Path(process.pileupVertexFilterCutGtight)
process.pVertexFilterCutGplus = cms.Path(process.pileupVertexFilterCutGplus)
process.pVertexFilterCutE = cms.Path(process.pileupVertexFilterCutE)
process.pVertexFilterCutEandG = cms.Path(process.pileupVertexFilterCutEandG)

process.load('HeavyIonsAnalysis.JetAnalysis.EventSelection_cff')
process.pHBHENoiseFilterResultProducer = cms.Path(process.HBHENoiseFilterResultProducer)
process.HBHENoiseFilterResult = cms.Path(process.fHBHENoiseFilterResult)
process.HBHENoiseFilterResultRun1 = cms.Path(process.fHBHENoiseFilterResultRun1)
process.HBHENoiseFilterResultRun2Loose = cms.Path(process.fHBHENoiseFilterResultRun2Loose)
process.HBHENoiseFilterResultRun2Tight = cms.Path(process.fHBHENoiseFilterResultRun2Tight)
process.HBHEIsoNoiseFilterResult = cms.Path(process.fHBHEIsoNoiseFilterResult)

process.pAna = cms.EndPath(process.skimanalysis)

# Customization
###############################################################################
#process.Timing = cms.Service("Timing")
