import FWCore.ParameterSet.Config as cms

myPartons = cms.EDProducer("PartonSelector",
    withLeptons = cms.bool(False),
    src = cms.InputTag("prunedGenParticles")
)

makePartons = cms.Sequence(myPartons)
