import FWCore.ParameterSet.Config as cms

from JetMETCorrections.Configuration.JetCorrectionServicesAllAlgos_cff import *
from JetMETCorrections.Configuration.JetCorrectors_cff import *


#
# SINGLE LEVEL CORRECTORS
#

# L1 (offset) Correctors
ak7CaloL1OffsetCorrector = ak4CaloL1OffsetCorrector.clone()
kt4CaloL1OffsetCorrector = ak4CaloL1OffsetCorrector.clone()
kt6CaloL1OffsetCorrector = ak4CaloL1OffsetCorrector.clone()
ic5CaloL1OffsetCorrector = ak4CaloL1OffsetCorrector.clone()

ak1PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()
ak1PFCHSL1OffsetCorrector   = ak4PFCHSL1OffsetCorrector.clone()
ak2PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()
ak2PFCHSL1OffsetCorrector   = ak4PFCHSL1OffsetCorrector.clone()
ak3PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()
ak3PFCHSL1OffsetCorrector   = ak4PFCHSL1OffsetCorrector.clone()
ak5PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()
ak5PFCHSL1OffsetCorrector   = ak4PFCHSL1OffsetCorrector.clone()
ak6PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()
ak6PFCHSL1OffsetCorrector   = ak4PFCHSL1OffsetCorrector.clone()
ak7PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()
ak7PFCHSL1OffsetCorrector   = ak4PFCHSL1OffsetCorrector.clone()
ak8PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()
ak8PFCHSL1OffsetCorrector   = ak4PFCHSL1OffsetCorrector.clone()
ak9PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()
ak9PFCHSL1OffsetCorrector   = ak4PFCHSL1OffsetCorrector.clone()
ak10PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()
ak10PFCHSL1OffsetCorrector   = ak4PFCHSL1OffsetCorrector.clone()



kt4PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()
kt6PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()
ic5PFL1OffsetCorrector   = ak4PFL1OffsetCorrector.clone()

ak7JPTL1OffsetCorrector  = ak4CaloL1OffsetCorrector.clone()

# L1 (fastjet) Correctors
ak7CaloL1FastjetCorrector = ak4CaloL1FastjetCorrector.clone()
kt4CaloL1FastjetCorrector = ak4CaloL1FastjetCorrector.clone()
kt6CaloL1FastjetCorrector = ak4CaloL1FastjetCorrector.clone()
ic5CaloL1FastjetCorrector = ak4CaloL1FastjetCorrector.clone()

ak1PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()
ak1PFCHSL1FastjetCorrector   = ak4PFCHSL1FastjetCorrector.clone()
ak2PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()
ak2PFCHSL1FastjetCorrector   = ak4PFCHSL1FastjetCorrector.clone()
ak3PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()
ak3PFCHSL1FastjetCorrector   = ak4PFCHSL1FastjetCorrector.clone()
ak5PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()
ak5PFCHSL1FastjetCorrector   = ak4PFCHSL1FastjetCorrector.clone()
ak6PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()
ak6PFCHSL1FastjetCorrector   = ak4PFCHSL1FastjetCorrector.clone()
ak7PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()
ak7PFCHSL1FastjetCorrector   = ak4PFCHSL1FastjetCorrector.clone()
ak8PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()
ak8PFCHSL1FastjetCorrector   = ak4PFCHSL1FastjetCorrector.clone()
ak9PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()
ak9PFCHSL1FastjetCorrector   = ak4PFCHSL1FastjetCorrector.clone()
ak10PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()
ak10PFCHSL1FastjetCorrector   = ak4PFCHSL1FastjetCorrector.clone()
kt4PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()
kt6PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()
ic5PFL1FastjetCorrector   = ak4PFL1FastjetCorrector.clone()

ak7JPTL1FastjetCorrector  = ak4JPTL1FastjetCorrector.clone()

# SPECIAL L1JPTOffset
ak7L1JPTOffsetCorrector = ak4L1JPTOffsetCorrector.clone()

# L2 (relative eta-conformity) Correctors
ak7CaloL2RelativeCorrector = ak4CaloL2RelativeCorrector.clone( algorithm = 'AK7Calo' )
kt4CaloL2RelativeCorrector = ak4CaloL2RelativeCorrector.clone( algorithm = 'KT4Calo' )
kt6CaloL2RelativeCorrector = ak4CaloL2RelativeCorrector.clone( algorithm = 'KT6Calo' )
ic5CaloL2RelativeCorrector = ak4CaloL2RelativeCorrector.clone( algorithm = 'IC5Calo' )


ak1PFL2RelativeCorrector   = ak4PFL2RelativeCorrector.clone(algorithm='AK1PF')
ak1PFCHSL2RelativeCorrector   = ak4PFCHSL2RelativeCorrector.clone(algorithm='AK1PFchs')
ak2PFL2RelativeCorrector   = ak4PFL2RelativeCorrector.clone(algorithm='AK2PF')
ak2PFCHSL2RelativeCorrector   = ak4PFCHSL2RelativeCorrector.clone(algorithm='AK2PFchs')
ak3PFL2RelativeCorrector   = ak4PFL2RelativeCorrector.clone(algorithm='AK3PF')
ak3PFCHSL2RelativeCorrector   = ak4PFCHSL2RelativeCorrector.clone(algorithm='AK3PFchs')
ak5PFL2RelativeCorrector   = ak4PFL2RelativeCorrector.clone(algorithm='AK5PF')
ak5PFCHSL2RelativeCorrector   = ak4PFCHSL2RelativeCorrector.clone(algorithm='AK5PFchs')
ak6PFL2RelativeCorrector   = ak4PFL2RelativeCorrector.clone(algorithm='AK6PF')
ak6PFCHSL2RelativeCorrector   = ak4PFCHSL2RelativeCorrector.clone(algorithm='AK6PFchs')
ak7PFL2RelativeCorrector   = ak4PFL2RelativeCorrector.clone(algorithm='AK7PF')
ak7PFCHSL2RelativeCorrector   = ak4PFCHSL2RelativeCorrector.clone(algorithm='AK7PFchs')
ak8PFL2RelativeCorrector   = ak4PFL2RelativeCorrector.clone(algorithm='AK8PF')
ak8PFCHSL2RelativeCorrector   = ak4PFCHSL2RelativeCorrector.clone(algorithm='AK8PFchs')
ak9PFL2RelativeCorrector   = ak4PFL2RelativeCorrector.clone(algorithm='AK9PF')
ak9PFCHSL2RelativeCorrector   = ak4PFCHSL2RelativeCorrector.clone(algorithm='AK9PFchs')
ak10PFL2RelativeCorrector   = ak4PFL2RelativeCorrector.clone(algorithm='AK10PF')
ak10PFCHSL2RelativeCorrector   = ak4PFCHSL2RelativeCorrector.clone(algorithm='AK10PFchs')
kt4PFL2RelativeCorrector   = ak4PFL2Relative.clone  ( algorithm = 'KT4PF' )
kt6PFL2RelativeCorrector   = ak4PFL2Relative.clone  ( algorithm = 'KT6PF' )
ic5PFL2RelativeCorrector   = ak4PFL2Relative.clone  ( algorithm = 'IC5PF' )

# L3 (absolute) Correctors
ak7CaloL3AbsoluteCorrector = ak4CaloL3AbsoluteCorrector.clone( algorithm = 'AK7Calo' )
kt4CaloL3AbsoluteCorrector = ak4CaloL3AbsoluteCorrector.clone( algorithm = 'KT4Calo' )
kt6CaloL3AbsoluteCorrector = ak4CaloL3AbsoluteCorrector.clone( algorithm = 'KT6Calo' )
ic5CaloL3AbsoluteCorrector = ak4CaloL3AbsoluteCorrector.clone( algorithm = 'IC5Calo' )

ak1PFL3AbsoluteCorrector   = ak4PFL3AbsoluteCorrector.clone(algorithm='AK1PF')
ak1PFCHSL3AbsoluteCorrector   = ak4PFCHSL3AbsoluteCorrector.clone(algorithm='AK1PFchs')
ak2PFL3AbsoluteCorrector   = ak4PFL3AbsoluteCorrector.clone(algorithm='AK2PF')
ak2PFCHSL3AbsoluteCorrector   = ak4PFCHSL3AbsoluteCorrector.clone(algorithm='AK2PFchs')
ak3PFL3AbsoluteCorrector   = ak4PFL3AbsoluteCorrector.clone(algorithm='AK3PF')
ak3PFCHSL3AbsoluteCorrector   = ak4PFCHSL3AbsoluteCorrector.clone(algorithm='AK3PFchs')
ak5PFL3AbsoluteCorrector   = ak4PFL3AbsoluteCorrector.clone(algorithm='AK5PF')
ak5PFCHSL3AbsoluteCorrector   = ak4PFCHSL3AbsoluteCorrector.clone(algorithm='AK5PFchs')
ak6PFL3AbsoluteCorrector   = ak4PFL3AbsoluteCorrector.clone(algorithm='AK6PF')
ak6PFCHSL3AbsoluteCorrector   = ak4PFCHSL3AbsoluteCorrector.clone(algorithm='AK6PFchs')
ak7PFL3AbsoluteCorrector   = ak4PFL3AbsoluteCorrector.clone(algorithm='AK7PF')
ak7PFCHSL3AbsoluteCorrector   = ak4PFCHSL3AbsoluteCorrector.clone(algorithm='AK7PFchs')
ak8PFL3AbsoluteCorrector   = ak4PFL3AbsoluteCorrector.clone(algorithm='AK8PF')
ak8PFCHSL3AbsoluteCorrector   = ak4PFCHSL3AbsoluteCorrector.clone(algorithm='AK8PFchs')
ak9PFL3AbsoluteCorrector   = ak4PFL3AbsoluteCorrector.clone(algorithm='AK9PF')
ak9PFCHSL3AbsoluteCorrector   = ak4PFCHSL3AbsoluteCorrector.clone(algorithm='AK9PFchs')
ak10PFL3AbsoluteCorrector   = ak4PFL3AbsoluteCorrector.clone(algorithm='AK10PF')
ak10PFCHSL3AbsoluteCorrector   = ak4PFCHSL3AbsoluteCorrector.clone(algorithm='AK10PFchs')
kt4PFL3AbsoluteCorrector   = ak4PFL3Absolute.clone  ( algorithm = 'KT4PF' )
kt6PFL3AbsoluteCorrector   = ak4PFL3Absolute.clone  ( algorithm = 'KT6PF' )
ic5PFL3AbsoluteCorrector   = ak4PFL3Absolute.clone  ( algorithm = 'IC5PF' )

# Residual Correctors
ak7CaloResidualCorrector   = ak4CaloResidualCorrector.clone()
kt4CaloResidualCorrector   = ak4CaloResidualCorrector.clone()
kt6CaloResidualCorrector   = ak4CaloResidualCorrector.clone()
ic5CaloResidualCorrector   = ak4CaloResidualCorrector.clone()

ak1PFResidualCorrector   = ak4PFResidualCorrector.clone()
ak1PFCHSResidualCorrector   = ak4PFCHSResidualCorrector.clone()
ak2PFResidualCorrector   = ak4PFResidualCorrector.clone()
ak2PFCHSResidualCorrector   = ak4PFCHSResidualCorrector.clone()
ak3PFResidualCorrector   = ak4PFResidualCorrector.clone()
ak3PFCHSResidualCorrector   = ak4PFCHSResidualCorrector.clone()
ak5PFResidualCorrector   = ak4PFResidualCorrector.clone()
ak5PFCHSResidualCorrector   = ak4PFCHSResidualCorrector.clone()
ak6PFResidualCorrector   = ak4PFResidualCorrector.clone()
ak6PFCHSResidualCorrector   = ak4PFCHSResidualCorrector.clone()
ak7PFResidualCorrector   = ak4PFResidualCorrector.clone()
ak7PFCHSResidualCorrector   = ak4PFCHSResidualCorrector.clone()
ak8PFResidualCorrector   = ak4PFResidualCorrector.clone()
ak8PFCHSResidualCorrector   = ak4PFCHSResidualCorrector.clone()
ak9PFResidualCorrector   = ak4PFResidualCorrector.clone()
ak9PFCHSResidualCorrector   = ak4PFCHSResidualCorrector.clone()
ak10PFResidualCorrector   = ak4PFResidualCorrector.clone()
ak10PFCHSResidualCorrector   = ak4PFCHSResidualCorrector.clone()
kt4PFResidualCorrector   = ak4PFResidualCorrector.clone()
kt6PFResidualCorrector   = ak4PFResidualCorrector.clone()
ic5PFResidualCorrector   = ak4PFResidualCorrector.clone()

# L6 (semileptonically decaying b-jet) Correctors
ak7CaloL6SLBCorrector = ak4CaloL6SLBCorrector.clone(
    srcBTagInfoElectron = cms.InputTag('ak7CaloJetsSoftElectronTagInfos'),
    srcBTagInfoMuon     = cms.InputTag('ak7CaloJetsSoftMuonTagInfos')
    )
kt4CaloL6SLBCorrector = ak4CaloL6SLBCorrector.clone(
    srcBTagInfoElectron = cms.InputTag('kt4CaloJetsSoftElectronTagInfos'),
    srcBTagInfoMuon     = cms.InputTag('kt4CaloJetsSoftMuonTagInfos')
    )
kt6CaloL6SLBCorrector = ak4CaloL6SLBCorrector.clone(
    srcBTagInfoElectron = cms.InputTag('kt6CaloJetsSoftElectronTagInfos'),
    srcBTagInfoMuon     = cms.InputTag('kt6CaloJetsSoftMuonTagInfos')
    )
ic5CaloL6SLBCorrector = ak4CaloL6SLBCorrector.clone(
    srcBTagInfoElectron = cms.InputTag('ic5CaloJetsSoftElectronTagInfos'),
    srcBTagInfoMuon     = cms.InputTag('ic5CaloJetsSoftMuonTagInfos')
    )

ak7PFL6SLBCorrector = ak4PFL6SLBCorrector.clone(
    srcBTagInfoElectron = cms.InputTag('ak7PFJetsSoftElectronTagInfos'),
    srcBTagInfoMuon     = cms.InputTag('ak7PFJetsSoftMuonTagInfos')
    )
kt4PFL6SLBCorrector = ak4PFL6SLBCorrector.clone(
    srcBTagInfoElectron = cms.InputTag('kt4PFJetsSoftElectronTagInfos'),
    srcBTagInfoMuon     = cms.InputTag('kt4PFJetsSoftMuonTagInfos')
    )
kt6PFL6SLBCorrector = ak4PFL6SLBCorrector.clone(
    srcBTagInfoElectron = cms.InputTag('kt6PFJetsSoftElectronTagInfos'),
    srcBTagInfoMuon     = cms.InputTag('kt6PFJetsSoftMuonTagInfos')
    )
ic5PFL6SLBCorrector = ak4PFL6SLBCorrector.clone(
    srcBTagInfoElectron = cms.InputTag('ic5PFJetsSoftElectronTagInfos'),
    srcBTagInfoMuon     = cms.InputTag('ic5PFJetsSoftMuonTagInfos')
    )


#
# MULTIPLE LEVEL CORRECTORS
#

# L2L3 CORRECTORS
ak7CaloL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7CaloL2Relative','ak7CaloL3Absolute')
    )
kt4CaloL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt4CaloL2Relative','kt4CaloL3Absolute')
    )
kt6CaloL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt6CaloL2Relative','kt6CaloL3Absolute')
    )
ic5CaloL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ic5CaloL2Relative','ic5CaloL3Absolute')
    )


ak1PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak1PFL2Relative','ak1PFL3Absolute')
    )

ak1PFCHSL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak1PFCHSL2Relative','ak1PFCHSL3Absolute')
    )

ak2PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak2PFL2Relative','ak2PFL3Absolute')
    )

ak2PFCHSL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak2PFCHSL2Relative','ak2PFCHSL3Absolute')
    )

ak3PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak3PFL2Relative','ak3PFL3Absolute')
    )

ak3PFCHSL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak3PFCHSL2Relative','ak3PFCHSL3Absolute')
    )

ak5PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak5PFL2Relative','ak5PFL3Absolute')
    )

ak5PFCHSL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak5PFCHSL2Relative','ak5PFCHSL3Absolute')
    )

ak6PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak6PFL2Relative','ak6PFL3Absolute')
    )

ak6PFCHSL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak6PFCHSL2Relative','ak6PFCHSL3Absolute')
    )

ak7PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7PFL2Relative','ak7PFL3Absolute')
    )

ak7PFCHSL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7PFCHSL2Relative','ak7PFCHSL3Absolute')
    )

ak8PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak8PFL2Relative','ak8PFL3Absolute')
    )

ak8PFCHSL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak8PFCHSL2Relative','ak8PFCHSL3Absolute')
    )

ak9PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak9PFL2Relative','ak9PFL3Absolute')
    )

ak9PFCHSL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak9PFCHSL2Relative','ak9PFCHSL3Absolute')
    )

ak10PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak10PFL2Relative','ak10PFL3Absolute')
    )

ak10PFCHSL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak10PFCHSL2Relative','ak10PFCHSL3Absolute')
    )

kt4PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt4PFL2Relative','kt4PFL3Absolute')
    )
kt6PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt6PFL2Relative','kt6PFL3Absolute')
    )
ic5PFL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ic5PFL2Relative','ic5PFL3Absolute')
    )

#--- JPT needs the L1JPTOffset to account for the ZSP changes.
#--- L1JPTOffset is NOT the same as L1Offset !!!!!
ak7JPTL2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7L1JPTOffset','ak7JPTL2Relative','ak7JPTL3Absolute')
    )

# L1L2L3 CORRECTORS
ak7CaloL1L2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7CaloL1Offset','ak7CaloL2Relative','ak7CaloL3Absolute')
    )
kt4CaloL1L2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt4CaloL1Offset','kt4CaloL2Relative','kt4CaloL3Absolute')
    )
kt6CaloL1L2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt6CaloL1Offset','kt6CaloL2Relative','kt6CaloL3Absolute')
    )
ic5CaloL1L2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ic5CaloL1Offset','ic5CaloL2Relative','ic5CaloL3Absolute')
    )

ak7PFL1L2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7PFL1Offset','ak7PFL2Relative','ak7PFL3Absolute')
    )
kt4PFL1L2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt4PFL1Offset','kt4PFL2Relative','kt4PFL3Absolute')
    )
kt6PFL1L2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt6PFL1Offset','kt6PFL2Relative','kt6PFL3Absolute')
    )
ic5PFL1L2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ic5PFL1Offset','ic5PFL2Relative','ic5PFL3Absolute')
    )
#--- JPT needs the L1JPTOffset to account for the ZSP changes.
#--- L1JPTOffset is NOT the same as L1Offset !!!!!
ak7JPTL1L2L3Corrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7JPTL1Offset','ak7L1JPTOffset','ak7JPTL2Relative','ak7JPTL3Absolute')
    )

# L2L3Residual CORRECTORS
ak7CaloL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7CaloL2Relative','ak7CaloL3Absolute','ak7CaloResidual')
    )
kt4CaloL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt4CaloL2Relative','kt4CaloL3Absolute','kt4CaloResidual')
    )
kt6CaloL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt6CaloL2Relative','kt6CaloL3Absolute','kt6CaloResidual')
    )
ic5CaloL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ic5CaloL2Relative','ic5CaloL3Absolute','ic5CaloResidual')
    )





ak1PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak1PFL2Relative','ak1PFL3Absolute','ak1PFResidual')
    )
ak1PFCHSL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak1PFCHSL2Relative','ak1PFCHSL3Absolute','ak1PFCHSResidual')
    )
ak2PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak2PFL2Relative','ak2PFL3Absolute','ak2PFResidual')
    )
ak2PFCHSL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak2PFCHSL2Relative','ak2PFCHSL3Absolute','ak2PFCHSResidual')
    )
ak3PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak3PFL2Relative','ak3PFL3Absolute','ak3PFResidual')
    )
ak3PFCHSL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak3PFCHSL2Relative','ak3PFCHSL3Absolute','ak3PFCHSResidual')
    )
ak5PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak5PFL2Relative','ak5PFL3Absolute','ak5PFResidual')
    )
ak5PFCHSL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak5PFCHSL2Relative','ak5PFCHSL3Absolute','ak5PFCHSResidual')
    )
ak6PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak6PFL2Relative','ak6PFL3Absolute','ak6PFResidual')
    )
ak6PFCHSL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak6PFCHSL2Relative','ak6PFCHSL3Absolute','ak6PFCHSResidual')
    )
ak7PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7PFL2Relative','ak7PFL3Absolute','ak7PFResidual')
    )
ak7PFCHSL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7PFCHSL2Relative','ak7PFCHSL3Absolute','ak7PFCHSResidual')
    )
ak8PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak8PFL2Relative','ak8PFL3Absolute','ak8PFResidual')
    )
ak8PFCHSL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak8PFCHSL2Relative','ak8PFCHSL3Absolute','ak8PFCHSResidual')
    )
ak9PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak9PFL2Relative','ak9PFL3Absolute','ak9PFResidual')
    )
ak9PFCHSL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak9PFCHSL2Relative','ak9PFCHSL3Absolute','ak9PFCHSResidual')
    )
ak10PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak10PFL2Relative','ak10PFL3Absolute','ak10PFResidual')
    )
ak10PFCHSL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak10PFCHSL2Relative','ak10PFCHSL3Absolute','ak10PFCHSResidual')
    )

kt4PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt4PFL2Relative','kt4PFL3Absolute','kt4PFResidual')
    )
kt6PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt6PFL2Relative','kt6PFL3Absolute','kt6PFResidual')
    )
ic5PFL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ic5PFL2Relative','ic5PFL3Absolute','ic5PFResidual')
    )

# L1L2L3Residual CORRECTORS
ak7CaloL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7CaloL1Offset','ak7CaloL2Relative','ak7CaloL3Absolute','ak7CaloResidual')
    )
kt4CaloL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt4CaloL1Offset','kt4CaloL2Relative','kt4CaloL3Absolute','kt4CaloResidual')
    )
kt6CaloL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt6CaloL1Offset','kt6CaloL2Relative','kt6CaloL3Absolute','kt6CaloResidual')
    )
ic5CaloL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ic5CaloL1Offset','ic5CaloL2Relative','ic5CaloL3Absolute','ic5CaloResidual')
    )

ak1PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak1PFL1Offset','ak1PFL2Relative','ak1PFL3Absolute','ak1PFResidual')
    )
ak1PFCHSL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak1PFCHSL1Offset','ak1PFCHSL2Relative','ak1PFCHSL3Absolute','ak1PFCHSResidual')
    )
ak2PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak2PFL1Offset','ak2PFL2Relative','ak2PFL3Absolute','ak2PFResidual')
    )
ak2PFCHSL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak2PFCHSL1Offset','ak2PFCHSL2Relative','ak2PFCHSL3Absolute','ak2PFCHSResidual')
    )
ak3PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak3PFL1Offset','ak3PFL2Relative','ak3PFL3Absolute','ak3PFResidual')
    )
ak3PFCHSL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak3PFCHSL1Offset','ak3PFCHSL2Relative','ak3PFCHSL3Absolute','ak3PFCHSResidual')
    )
ak5PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak5PFL1Offset','ak5PFL2Relative','ak5PFL3Absolute','ak5PFResidual')
    )
ak5PFCHSL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak5PFCHSL1Offset','ak5PFCHSL2Relative','ak5PFCHSL3Absolute','ak5PFCHSResidual')
    )
ak6PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak6PFL1Offset','ak6PFL2Relative','ak6PFL3Absolute','ak6PFResidual')
    )
ak6PFCHSL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak6PFCHSL1Offset','ak6PFCHSL2Relative','ak6PFCHSL3Absolute','ak6PFCHSResidual')
    )
ak7PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7PFL1Offset','ak7PFL2Relative','ak7PFL3Absolute','ak7PFResidual')
    )
ak7PFCHSL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7PFCHSL1Offset','ak7PFCHSL2Relative','ak7PFCHSL3Absolute','ak7PFCHSResidual')
    )
ak8PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak8PFL1Offset','ak8PFL2Relative','ak8PFL3Absolute','ak8PFResidual')
    )
ak8PFCHSL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak8PFCHSL1Offset','ak8PFCHSL2Relative','ak8PFCHSL3Absolute','ak8PFCHSResidual')
    )
ak9PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak9PFL1Offset','ak9PFL2Relative','ak9PFL3Absolute','ak9PFResidual')
    )
ak9PFCHSL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak9PFCHSL1Offset','ak9PFCHSL2Relative','ak9PFCHSL3Absolute','ak9PFCHSResidual')
    )
ak10PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak10PFL1Offset','ak10PFL2Relative','ak10PFL3Absolute','ak10PFResidual')
    )
ak10PFCHSL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak10PFCHSL1Offset','ak10PFCHSL2Relative','ak10PFCHSL3Absolute','ak10PFCHSResidual')
    )

kt4PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt4PFL1Offset','kt4PFL2Relative','kt4PFL3Absolute','kt4PFResidual')
    )
kt6PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt6PFL1Offset','kt6PFL2Relative','kt6PFL3Absolute','kt6PFResidual')
    )
ic5PFL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ic5PFL1Offset','ic5PFL2Relative','ic5PFL3Absolute','ic5PFResidual')
    )
#--- JPT needs the L1JPTOffset to account for the ZSP changes.
#--- L1JPTOffset is NOT the same as L1Offset !!!!!
ak7JPTL1L2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7JPTL1Offset','ak7L1JPTOffset','ak7JPTL2Relative','ak7JPTL3Absolute','ak7JPTResidual')
    )

# L1FastL2L3 CORRECTORS
ak7CaloL1FastL2L3Corrector = ak7CaloL2L3Corrector.clone()
ak7CaloL1FastL2L3Corrector.correctors.insert(0,'ak4CaloL1Fastjet')
kt4CaloL1FastL2L3Corrector = kt4CaloL2L3Corrector.clone()
kt4CaloL1FastL2L3Corrector.correctors.insert(0,'ak4CaloL1Fastjet')
kt6CaloL1FastL2L3Corrector = kt6CaloL2L3Corrector.clone()
kt6CaloL1FastL2L3Corrector.correctors.insert(0,'ak4CaloL1Fastjet')
ic5CaloL1FastL2L3Corrector = ic5CaloL2L3Corrector.clone()
ic5CaloL1FastL2L3Corrector.correctors.insert(0,'ak4CaloL1Fastjet')

ak7PFL1FastL2L3Corrector = ak7PFL2L3Corrector.clone()
ak7PFL1FastL2L3Corrector.correctors.insert(0,'ak4PFL1Fastjet')
ak7PFCHSL1FastL2L3Corrector = ak7PFCHSL2L3Corrector.clone()
ak7PFCHSL1FastL2L3Corrector.correctors.insert(0,'ak4PFCHSL1Fastjet')
kt4PFL1FastL2L3Corrector = kt4PFL2L3Corrector.clone()
kt4PFL1FastL2L3Corrector.correctors.insert(0,'ak4PFL1Fastjet')
kt6PFL1FastL2L3Corrector = kt6PFL2L3Corrector.clone()
kt6PFL1FastL2L3Corrector.correctors.insert(0,'ak4PFL1Fastjet')
ic5PFL1FastL2L3Corrector = ic5PFL2L3Corrector.clone()
ic5PFL1FastL2L3Corrector.correctors.insert(0,'ak4PFL1Fastjet')

ak4TrackL1FastL2L3Corrector = ak4TrackL2L3Corrector.clone()
ak4TrackL1FastL2L3Corrector.correctors.insert(0,'ak4CaloL1Fastjet')

# L1FastL2L3Residual CORRECTORS
ak7CaloL1FastL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7CaloL1Fastjet','ak7CaloL2Relative','ak7CaloL3Absolute','ak7CaloResidual')
    )
kt4CaloL1FastL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt4CaloL1Fastjet','kt4CaloL2Relative','kt4CaloL3Absolute','kt4CaloResidual')
    )
kt6CaloL1FastL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt6CaloL1Fastjet','kt6CaloL2Relative','kt6CaloL3Absolute','kt6CaloResidual')
    )
ic5CaloL1FastL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ic5CaloL1Fastjet','ic5CaloL2Relative','ic5CaloL3Absolute','ic5CaloResidual')
    )



ak1PFL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak1PFL1Fastjet','ak1PFL2Relative','ak1PFL3Absolute','ak1PFResidual')
    )
ak1PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak1PFCHSL1Fastjet','ak1PFCHSL2Relative','ak1PFCHSL3Absolute','ak1PFCHSResidual')
    )
ak2PFL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak2PFL1Fastjet','ak2PFL2Relative','ak2PFL3Absolute','ak2PFResidual')
    )
ak2PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak2PFCHSL1Fastjet','ak2PFCHSL2Relative','ak2PFCHSL3Absolute','ak2PFCHSResidual')
    )
ak3PFL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak3PFL1Fastjet','ak3PFL2Relative','ak3PFL3Absolute','ak3PFResidual')
    )
ak3PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak3PFCHSL1Fastjet','ak3PFCHSL2Relative','ak3PFCHSL3Absolute','ak3PFCHSResidual')
    )
ak5PFL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak5PFL1Fastjet','ak5PFL2Relative','ak5PFL3Absolute','ak5PFResidual')
    )
ak5PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak5PFCHSL1Fastjet','ak5PFCHSL2Relative','ak5PFCHSL3Absolute','ak5PFCHSResidual')
    )
ak6PFL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak6PFL1Fastjet','ak6PFL2Relative','ak6PFL3Absolute','ak6PFResidual')
    )
ak6PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak6PFCHSL1Fastjet','ak6PFCHSL2Relative','ak6PFCHSL3Absolute','ak6PFCHSResidual')
    )
ak7PFL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7PFL1Fastjet','ak7PFL2Relative','ak7PFL3Absolute','ak7PFResidual')
    )
ak7PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7PFCHSL1Fastjet','ak7PFCHSL2Relative','ak7PFCHSL3Absolute','ak7PFCHSResidual')
    )
ak8PFL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak8PFL1Fastjet','ak8PFL2Relative','ak8PFL3Absolute','ak8PFResidual')
    )
ak8PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak8PFCHSL1Fastjet','ak8PFCHSL2Relative','ak8PFCHSL3Absolute','ak8PFCHSResidual')
    )
ak9PFL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak9PFL1Fastjet','ak9PFL2Relative','ak9PFL3Absolute','ak9PFResidual')
    )
ak9PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak9PFCHSL1Fastjet','ak9PFCHSL2Relative','ak9PFCHSL3Absolute','ak9PFCHSResidual')
    )
ak10PFL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak10PFL1Fastjet','ak10PFL2Relative','ak10PFL3Absolute','ak10PFResidual')
    )
ak10PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak10PFCHSL1Fastjet','ak10PFCHSL2Relative','ak10PFCHSL3Absolute','ak10PFCHSResidual')
    )

kt4PFL1FastL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt4PFL1Fastjet','kt4PFL2Relative','kt4PFL3Absolute','kt4PFResidual')
    )
kt6PFL1FastL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('kt6PFL1Fastjet','kt6PFL2Relative','kt6PFL3Absolute','kt6PFResidual')
    )
ic5PFL1FastL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ic5PFL1Fastjet','ic5PFL2Relative','ic5PFL3Absolute','ic5PFResidual')
    )
#--- JPT needs the L1JPTOffset to account for the ZSP changes.
#--- L1JPTOffset is NOT the same as L1Offset !!!!!
ak7JPTL1FastL2L3ResidualCorrector = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.vstring('ak7JPTL1Fastjet','ak7L1JPTOffset','ak7JPTL2Relative','ak7JPTL3Absolute','ak7JPTResidual')
    )

# L2L3L6 CORRECTORS
ak7CaloL2L3L6Corrector = ak7CaloL2L3Corrector.clone()
ak7CaloL2L3L6Corrector.correctors.append('ak7CaloL6SLB')
kt4CaloL2L3L6Corrector = kt4CaloL2L3Corrector.clone()
kt4CaloL2L3L6Corrector.correctors.append('kt4CaloL6SLB')
kt6CaloL2L3L6Corrector = kt6CaloL2L3Corrector.clone()
kt6CaloL2L3L6Corrector.correctors.append('kt6CaloL6SLB')
ic5CaloL2L3L6Corrector = ic5CaloL2L3Corrector.clone()
ic5CaloL2L3L6Corrector.correctors.append('ic5CaloL6SLB')

ak7PFL2L3L6Corrector = ak7PFL2L3Corrector.clone()
ak7PFL2L3L6Corrector.correctors.append('ak7PFL6SLB')
kt4PFL2L3L6Corrector = kt4PFL2L3Corrector.clone()
kt4PFL2L3L6Corrector.correctors.append('kt4PFL6SLB')
kt6PFL2L3L6Corrector = kt6PFL2L3Corrector.clone()
kt6PFL2L3L6Corrector.correctors.append('kt6PFL6SLB')
ic5PFL2L3L6Corrector = ic5PFL2L3Corrector.clone()
ic5PFL2L3L6Corrector.correctors.append('ic5PFL6SLB')


# L1L2L3L6 CORRECTORS
ak7CaloL1FastL2L3L6Corrector = ak7CaloL1L2L3Corrector.clone()
ak7CaloL1FastL2L3L6Corrector.correctors.append('ak7CaloL6SLB')
kt4CaloL1FastL2L3L6Corrector = kt4CaloL1L2L3Corrector.clone()
kt4CaloL1FastL2L3L6Corrector.correctors.append('kt4CaloL6SLB')
kt6CaloL1FastL2L3L6Corrector = kt6CaloL1L2L3Corrector.clone()
kt6CaloL1FastL2L3L6Corrector.correctors.append('kt6CaloL6SLB')
ic5CaloL1FastL2L3L6Corrector = ic5CaloL1L2L3Corrector.clone()
ic5CaloL1FastL2L3L6Corrector.correctors.append('ic5CaloL6SLB')

ak7PFL1FastL2L3L6Corrector = ak7PFL1FastL2L3Corrector.clone()
ak7PFL1FastL2L3L6Corrector.correctors.append('ak7PFL6SLB')
kt4PFL1FastL2L3L6Corrector = kt4PFL1FastL2L3Corrector.clone()
kt4PFL1FastL2L3L6Corrector.correctors.append('kt4PFL6SLB')
kt6PFL1FastL2L3L6Corrector = kt6PFL1FastL2L3Corrector.clone()
kt6PFL1FastL2L3L6Corrector.correctors.append('kt6PFL6SLB')
ic5PFL1FastL2L3L6Corrector = ic5PFL1FastL2L3Corrector.clone()
ic5PFL1FastL2L3L6Corrector.correctors.append('ic5PFL6SLB')
