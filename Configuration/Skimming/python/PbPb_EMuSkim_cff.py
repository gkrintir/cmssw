import FWCore.ParameterSet.Config as cms

# HLT dimuon trigger
import HLTrigger.HLTfilters.hltHighLevel_cfi
hltEMuHI = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
hltEMuHI.HLTPaths = ["HLT_HIL3Mu12_v*","HLT_HIL3Mu15_v*"]
hltEMuHI.throw = True
hltEMuHI.andOr = True

# selection of valid vertex --> will run it at hin tree level 
#primaryVertexFilterForEMu = cms.EDFilter("VertexSelector",
#    src = cms.InputTag("offlinePrimaryVertices"),
#    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2"), 
#    filter = cms.bool(True),   # otherwise it won't filter the events
#    )

# single lepton selector                                                                                                                                               
electronSelectorForEMu = cms.EDFilter("GsfElectronRefSelector",
                                   src = cms.InputTag("gedGsfElectrons"),
                                   cut = cms.string("pt > 20 && abs(eta)<2.1")
                                   )

muonSelectorForEMu = cms.EDFilter("MuonSelector",
                                  src = cms.InputTag("muons"),
                                  cut = cms.string("(isTrackerMuon && isGlobalMuon) && pt > 20. && abs(eta)<2.4"),
                                  filter = cms.bool(True)
    )

## dilepton selectors                                                                                                                                                                                       
diLeptonsForZEM = cms.EDProducer("CandViewShallowCloneCombiner",
                                   decay       = cms.string("electronSelectorForEMu muonSelectorForEMu"),
                                   checkCharge = cms.bool(False),
                                   cut         = cms.string("mass > 20")
                                   )
# dilepton counter                                                                                                                                                                                          
diLeptonsFilterForZEM = cms.EDFilter("CandViewCountFilter",
                                       src = cms.InputTag("diLeptonsForZEM"),
                                       minNumber = cms.uint32(1)
                                       
)
# EMu skim sequence
emuSkimSequence = cms.Sequence(
    hltEMuHI *
    #primaryVertexFilterForEMu *
    electronSelectorForEMu * 
    muonSelectorForEMu *
    diLeptonsForZEM *
    diLeptonsFilterForZEM
)
