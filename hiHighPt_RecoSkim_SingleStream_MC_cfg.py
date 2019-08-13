import FWCore.ParameterSet.Config as cms
process = cms.Process("HIGHPTSKIM")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContentHeavyIons_cff')

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
        '/store/himc/HINPbPbAutumn18DR/WJetsToLNu_TuneCP5_HydjetDrumMB_5p02TeV-amcatnloFXFX-pythia8/AODSIM/mva98_103X_upgrade2018_realistic_HI_v11-v1/70001/FF00EC54-074B-B544-9AD5-E1FF5EF21AE5.root'
        #'/store/himc/HINPbPbAutumn18DR/TTJets_TuneCP5_HydjetDrumMB_5p02TeV-amcatnloFXFX-pythia8/AODSIM/mva98_103X_upgrade2018_realistic_HI_v11-v1/260000/FFDE7940-8BA3-4144-A8EB-DE5E0C642CA4.root'
)
)

# =============== Other Statements =====================
#process.MessageLogger = cms.Service("MessageLogger",
#                                              destinations   = cms.untracked.vstring('detailedInfo'),
#                                              categories      = cms.untracked.vstring('eventNumber'),
#                                              detailedInfo    = cms.untracked.PSet(
#                                                                        eventNumber = cms.untracked.PSet(
#                                                                        reportEvery = cms.untracked.int32(1000)
#                                                                                                )
#                                                                                                                                 ),
#)
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1000 )
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

#Trigger Selection (done in the loaded filters)

#Further Lepton Selection
process.load('Configuration.Skimming.PbPb_ZMMSkim_cff')
process.load('Configuration.Skimming.PbPb_ZEESkim_cff')
process.load('Configuration.Skimming.PbPb_EMuSkim_cff')

process.eventFilter_dimu = cms.Path(
    process.zMMSkimSequence
    )

process.eventFilter_diele = cms.Path(
    process.zEESkimSequence
    )

process.eventFilter_emu = cms.Path(
    process.emuSkimSequence
    )

process.output_dilep = cms.OutputModule("PoolOutputModule",
    outputCommands = process.RECOSIMEventContent.outputCommands,
    fileName = cms.untracked.string('dilep.root'),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('eventFilter_dimu','eventFilter_diele','eventFilter_emu')),
    dataset = cms.untracked.PSet(
    dataTier = cms.untracked.string('RECOSIM'),
    filterName = cms.untracked.string('hiHighPt'))
)

process.output_step_dilep = cms.EndPath(process.output_dilep)

process.schedule = cms.Schedule(
    process.eventFilter_dimu,
    process.eventFilter_diele,
    process.eventFilter_emu,
    process.output_step_dilep,
)
