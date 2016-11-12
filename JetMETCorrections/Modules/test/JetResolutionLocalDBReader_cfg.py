import FWCore.ParameterSet.Config as cms

process = cms.Process("JERDBLocalReader")

process.load('Configuration.StandardSequences.Services_cff')
process.load("JetMETCorrections.Modules.JetResolutionESProducer_cfi")

from CondCore.DBCommon.CondDBSetup_cfi import *

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.source = cms.Source("EmptySource")

process.PoolDBESSource = cms.ESSource("PoolDBESSource",
        CondDBSetup,
        toGet = cms.VPSet(
            # Resolution
            cms.PSet(
                record = cms.string('JetResolutionRcd'),
                tag    = cms.string('JR_Fall15_25nsV2_MC_PtResolution_AK4PFch'),
                label  = cms.untracked.string('AK4PFchs_pt')
                ),

            # Scale factors
            cms.PSet(
                record = cms.string('JetResolutionScaleFactorRcd'),
                tag    = cms.string('JR_Fall15_25nsV2_MC_SF_AK4PFchs'),
                label  = cms.untracked.string('AK4PFchs')
                ),
            ),
        connect = cms.string('sqlite:PhysicsTools/PatUtils/data/Fall15_25nsV2_MC.db')
        )


process.demo1 = cms.EDAnalyzer('JetResolutionDBReader', 
        era = cms.untracked.string('Fall15_25nsV2_MC_PtResolution'),
        label = cms.untracked.string('AK4PFchs_pt'),
        dump = cms.untracked.bool(True),
        saveFile = cms.untracked.bool(True)
        )

process.demo2 = cms.EDAnalyzer('JetResolutionScaleFactorDBReader', 
        era = cms.untracked.string('Fall15_25nsV2_MC_SF'),
        label = cms.untracked.string('AK4PFchs'),
        dump = cms.untracked.bool(True),
        saveFile = cms.untracked.bool(True)
        )

process.p = cms.Path(process.demo1 * process.demo2)
