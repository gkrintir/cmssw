import FWCore.ParameterSet.Config as cms
process = cms.Process("HIGHPTSKIM")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContentHeavyIons_cff')

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
        'file:/eos/cms/store/hidata/HIRun2018A/HISingleMuon/AOD/04Apr2019-v1/260004/F8E73537-8701-AE42-8F7F-9EAC04AD406C.root',
        'file:/eos/cms/store/hidata/HIRun2018A/HISingleMuon/AOD/04Apr2019-v1/260004/31703978-0174-BF4E-B115-B5E75CFD1DB5.root',
        'file:/eos/cms/store/hidata/HIRun2018A/HISingleMuon/AOD/04Apr2019-v1/260004/E7D9C887-04A1-9345-8949-AE72F833DD9B.root',
        'file:/eos/cms/store/hidata/HIRun2018A/HISingleMuon/AOD/04Apr2019-v1/260004/43BAF598-34F9-764C-BA65-95EE3C723DA0.root',
        'file:/eos/cms/store/hidata/HIRun2018A/HISingleMuon/AOD/04Apr2019-v1/260004/79511DAE-BD74-5B4B-9570-0B1961375107.root',
        'file:/eos/cms/store/hidata/HIRun2018A/HISingleMuon/AOD/04Apr2019-v1/260004/702CF304-1597-6741-8A76-C5F96691FD96.root',
        'file:/eos/cms/store/hidata/HIRun2018A/HISingleMuon/AOD/04Apr2019-v1/260004/CFD13D34-B2A9-2149-B815-6ADCB5BC3DAA.root',
        'file:/eos/cms/store/hidata/HIRun2018A/HISingleMuon/AOD/04Apr2019-v1/260004/3B995A4A-F95F-714F-89CB-FD9F6AFAD843.root',
)
)

# =============== Other Statements =====================
process.MessageLogger = cms.Service("MessageLogger",
                                              destinations   = cms.untracked.vstring('detailedInfo'),
                                              categories      = cms.untracked.vstring('eventNumber'),
                                              detailedInfo    = cms.untracked.PSet(
                                                                        eventNumber = cms.untracked.PSet(
                                                                        reportEvery = cms.untracked.int32(1000)
                                                                                                )
                                                                                                                                 ),
)
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

process.output_dimu = cms.OutputModule("PoolOutputModule",
    outputCommands = process.RECOEventContent.outputCommands,
    fileName = cms.untracked.string('dimu.root'),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('eventFilter_dimu')),
    dataset = cms.untracked.PSet(
      dataTier = cms.untracked.string('RECO'),
      filterName = cms.untracked.string('hiHighPt'))
)

process.output_diele = cms.OutputModule("PoolOutputModule",
    outputCommands = process.RECOEventContent.outputCommands,
    fileName = cms.untracked.string('diele.root'),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('eventFilter_diele')),
    dataset = cms.untracked.PSet(
      dataTier = cms.untracked.string('RECO'),
      filterName = cms.untracked.string('hiHighPt'))
)

process.output_emu = cms.OutputModule("PoolOutputModule",
    outputCommands = process.RECOEventContent.outputCommands,
    fileName = cms.untracked.string('emu.root'),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('eventFilter_emu')),
    dataset = cms.untracked.PSet(
      dataTier = cms.untracked.string('RECO'),
      filterName = cms.untracked.string('hiHighPt'))
)

process.output_step_dimu = cms.EndPath(process.output_dimu)

process.output_step_diele = cms.EndPath(process.output_diele)

process.output_step_emu = cms.EndPath(process.output_emu)

process.schedule = cms.Schedule(
    process.eventFilter_dimu,
    process.eventFilter_diele,
    process.eventFilter_emu,
    process.output_step_dimu,
    process.output_step_diele,
    process.output_step_emu,
)
