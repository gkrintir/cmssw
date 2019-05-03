import FWCore.ParameterSet.Config as cms

# import kt jets for rho estimators
from HeavyIonsAnalysis.JetAnalysis.ktPFJets_cfi import PFTowers, kt4PFJets, kt4PFJetsForRho

from RecoHI.HiJetAlgos.hiFJRhoProducers import hiFJRhoProducer, hiFJRhoProducerFinerBins
from RecoHI.HiJetAlgos.hiFJGridEmptyAreaCalculators_cff import hiFJGridEmptyAreaCalculator, hiFJGridEmptyAreaCalculatorFinerBins

rhoSequence = cms.Sequence(
    PFTowers +
    kt4PFJets +
    kt4PFJetsForRho +
    hiFJRhoProducer +
    hiFJRhoProducerFinerBins +
    hiFJGridEmptyAreaCalculator +
    hiFJGridEmptyAreaCalculatorFinerBins
)
