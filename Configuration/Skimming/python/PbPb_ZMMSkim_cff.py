import FWCore.ParameterSet.Config as cms

# HLT dimuon trigger
import HLTrigger.HLTfilters.hltHighLevel_cfi
hltZMMPbPb = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
hltZMMPbPb.HLTPaths = ["HLT_HIL3Mu12_v*","HLT_HIL3Mu15_v*","HLT_HIL3_L1DoubleMu10_v*"]
hltZMMPbPb.throw = True
hltZMMPbPb.andOr = True

# selection of valid vertex --> will run it at hin tree level
#primaryVertexFilterForZMM = cms.EDFilter("VertexSelector",
#    src = cms.InputTag("offlinePrimaryVertices"),
#    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2"), 
#    filter = cms.bool(True),   # otherwise it won't filter the events
#    )

# selection of dimuons with mass in Z range
muonSelectorForZMM = cms.EDFilter("MuonSelector",
    src = cms.InputTag("muons"),
    cut = cms.string("(isTrackerMuon && isGlobalMuon) && pt > 20. && abs(eta)<2.4"),
    filter = cms.bool(True)
    )

muonFilterForZMM = cms.EDFilter("MuonCountFilter",
    src = cms.InputTag("muonSelectorForZMM"),
    minNumber = cms.uint32(2)
    )

dimuonMassCutForZMM = cms.EDProducer("CandViewShallowCloneCombiner",
    checkCharge = cms.bool(True),
    cut = cms.string(' mass > 20'),
    decay = cms.string("muonSelectorForZMM@+ muonSelectorForZMM@-")
    )

dimuonMassCutFilterForZMM = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("dimuonMassCutForZMM"),
    minNumber = cms.uint32(1)
    )

# Z->mumu skim sequence
zMMSkimSequence = cms.Sequence(
    hltZMMPbPb *
    #primaryVertexFilterForZMM *
    muonSelectorForZMM *
    muonFilterForZMM *
    dimuonMassCutForZMM *
    dimuonMassCutFilterForZMM
    )
