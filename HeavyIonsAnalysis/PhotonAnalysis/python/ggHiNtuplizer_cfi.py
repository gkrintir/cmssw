import FWCore.ParameterSet.Config as cms

from HeavyIonsAnalysis.PhotonAnalysis.ElectronVID_cff import *

ggHiNtuplizer = cms.EDAnalyzer(
    "ggHiNtuplizer",
    doGenParticles     = cms.bool(True),
    runOnParticleGun   = cms.bool(False),
    useValMapIso       = cms.bool(True),
    doElectronVID      = cms.bool(False),
    pileupCollection   = cms.InputTag("slimmedAddPileupInfo"),
    genParticleSrc     = cms.InputTag("prunedGenParticles"),
    gsfElectronLabel   = cms.InputTag("slimmedElectrons"),
    recoPhotonSrc      = cms.InputTag("slimmedPhotons"),
    electronVetoID     = electronVetoID25nsV1,
    electronLooseID    = electronLooseID25nsV1,
    electronMediumID   = electronMediumID25nsV1,
    electronTightID    = electronTightID25nsV1,
    recoPhotonHiIsolationMap = cms.InputTag("photonIsolationHIProducer"),
    recoMuonSrc        = cms.InputTag("slimmedMuons"),
    VtxLabel           = cms.InputTag("offlineSlimmedPrimaryVertices"),
    rho                = cms.InputTag("fixedGridRhoFastjetAll"),
    beamSpot           = cms.InputTag('offlineBeamSpot'),
    conversions        = cms.InputTag('reducedEgamma',"reducedConversions"),
    effAreasConfigFile = effAreasConfigFile25ns,
    doPfIso            = cms.bool(True),
    doVsIso            = cms.bool(True),
    particleFlowCollection = cms.InputTag("packedPFCandidates"),
    voronoiBackgroundCalo = cms.InputTag("voronoiBackgroundCalo"),
    voronoiBackgroundPF = cms.InputTag("voronoiBackgroundPF"),
    pfMETLabel = cms.InputTag("slimmedMETs"),
    pfMETNoHFLabel = cms.InputTag("slimmedMETsNoHF")
)
