# ######################################################################
#
# pixelLumi.py
#
# ----------------------------------------------------------------------
import os
import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')

options.register(
    'files',
    "List_mu.txt",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "list with input files"
)

options.register(
    'lumiMask',
    "False",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "enable lumiMask"
)

options.parseArguments()

process = cms.Process("Lumi")


# ----------------------------------------------------------------------
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.categories.append('HLTrigReport')
process.MessageLogger.categories.append('L1GtTrigReport')
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# -- Database configuration
process.load("CondCore.CondDB.CondDB_cfi")

# -- Conditions

process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff") #
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag

#process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_v14', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_dataRun2_Prompt_v6', '')


process.load("Configuration.StandardSequences.Reconstruction_cff") # 
# -- number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )

# -- skimming
process.zerobiasfilter = cms.EDFilter("HLTHighLevel",
   TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
   #HLTPaths = cms.vstring("HLT_ZeroBias_v*"),
   HLTPaths = cms.vstring("*ZeroBias*","*L1AlwaysTrue*"),
   eventSetupPathsKey = cms.string(""),
   andOr = cms.bool(True),
   throw = cms.bool(True)
    )

# the main Analyzer
process.lumi = cms.EDAnalyzer(
    "PCCNTupler",
    verbose                      = cms.untracked.int32(0),
    #rootFileName                 = cms.untracked.string(rootFileName),
    #type                         = cms.untracked.string(getDataset(process.source.fileNames[0])),
    globalTag                    = process.GlobalTag.globaltag,
    dumpAllEvents                = cms.untracked.int32(0),
    vertexCollLabel              = cms.untracked.InputTag('offlinePrimaryVertices'),
    pixelClusterLabel            = cms.untracked.InputTag('siPixelClusters'), # even in Phase2, for now.
    saveType                     = cms.untracked.string('Event'), # LumiSect, LumiNib, Event
    sampleType                   = cms.untracked.string('DATA'), # MC, DATA
    includeVertexInformation     = cms.untracked.bool(True),
    includePixels                = cms.untracked.bool(True),
    splitByBX                    = cms.untracked.bool(True),
    L1GTReadoutRecordLabel       = cms.untracked.InputTag('gtDigis'), 
    hltL1GtObjectMap             = cms.untracked.InputTag('hltL1GtObjectMap'), 
    HLTResultsLabel              = cms.untracked.InputTag('TriggerResults::HLT'),
    pixelPhase2Geometry          = cms.untracked.bool(True),
    )

# -- Path
process.p = cms.Path(
    process.zerobiasfilter*
    process.lumi
    )



#####################################################################################
# Input source
#####################################################################################
files = open(options.files, 'r')
fileList = cms.untracked.vstring()
fileList.extend( [line.strip() for line in files.read().splitlines()] )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring (fileList),
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    secondaryFileNames = cms.untracked.vstring()
)

#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string(options.outputFile))
