import FWCore.ParameterSet.Config as cms

process = cms.Process("BSworkflow")

from filelist_NoMinBias5 import file_list
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      file_list
    ),
    skipBadFiles = cms.untracked.bool(True),
lumisToProcess = cms.untracked.VLuminosityBlockRange('thelumirange')
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport  = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(10000),
)
process.MessageLogger.debugModules = ['BeamSpotAnalyzer']

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.Geometry.GeometryRecoDB_cff')


## BeamSpot fit
process.load("RecoVertex.BeamSpotProducer.d0_phi_analyzer_cff")

process.d0_phi_analyzer.BeamFitter.WriteAscii                = True
process.d0_phi_analyzer.BeamFitter.AsciiFileName             = 'BeamFit_LumiBased_alcareco_template.txt'
process.d0_phi_analyzer.BeamFitter.AppendRunToFileName       = True
process.d0_phi_analyzer.BeamFitter.InputBeamWidth            = -1
process.d0_phi_analyzer.BeamFitter.MaximumImpactParameter    = 1.0
process.d0_phi_analyzer.BeamFitter.MaximumNormChi2           = 10
process.d0_phi_analyzer.BeamFitter.MinimumInputTracks        = 50
process.d0_phi_analyzer.BeamFitter.MinimumPixelLayers        = -1
process.d0_phi_analyzer.BeamFitter.MinimumPt                 = 1.0
process.d0_phi_analyzer.BeamFitter.MinimumTotalLayers        = 6
process.d0_phi_analyzer.BeamFitter.OutputFileName            = 'BeamFit_LumiBased_Workflow_alcareco.root'
process.d0_phi_analyzer.BeamFitter.TrackAlgorithm            = cms.untracked.vstring()
process.d0_phi_analyzer.BeamFitter.TrackCollection           = 'hiGeneralTracks'
process.d0_phi_analyzer.BeamFitter.SaveFitResults            = False
process.d0_phi_analyzer.BeamFitter.SaveNtuple                = False
process.d0_phi_analyzer.BeamFitter.SavePVVertices            = False
#process.d0_phi_analyzer.BeamFitter.timerange                 = cms.untracked.vdouble(1464336285,1464336313)
process.d0_phi_analyzer.BeamFitter.selectBx                  = cms.untracked.vint32([12, 16, 25, 29, 38, 42, 51, 55, 64, 68, 104, 108, 117, 121, 130, 134, 143, 147, 156, 160, 169, 173, 182, 186, 195, 199, 208, 212, 221, 225, 234, 238, 247, 251, 287, 291, 300, 304, 313, 317, 326, 330, 339, 343, 352, 356, 365, 369, 378, 382, 391, 395, 404, 408, 446, 450, 459, 463, 472, 476, 485, 489, 498, 502, 511, 515, 524, 528, 537, 541, 550, 554, 563, 567, 576, 580, 589, 593, 629, 633, 642, 646, 655, 659, 668, 672, 681, 685, 694, 698, 707, 711, 720, 724, 733, 737, 746, 750, 759, 763, 772, 776, 812, 816, 825, 829, 838, 842, 851, 855, 864, 868, 877, 881, 890, 894, 903, 907, 916, 920, 929, 933, 942, 946, 955, 959, 995, 999, 1008, 1012, 1021, 1025, 1034, 1038, 1047, 1051, 1060, 1064, 1073, 1077, 1086, 1090, 1099, 1103, 1112, 1116, 1125, 1129, 1138, 1142, 1178, 1182, 1191, 1195, 1204, 1208, 1217, 1221, 1230, 1234, 1243, 1247, 1256, 1260, 1269, 1273, 1282, 1286, 1520, 1524, 1533, 1537, 1546, 1550, 1559, 1563, 1572, 1576, 1585, 1589, 1598, 1602, 1611, 1615, 1624, 1628, 1637, 1641, 1650, 1654, 1663, 1667, 1703, 1707, 1716, 1720, 1729, 1733, 1742, 1746, 1755, 1759, 1768, 1772, 1781, 1785, 1794, 1798, 1807, 1811, 1820, 1824, 1833, 1837, 1846, 1850, 1886, 1890, 1899, 1903, 1912, 1916, 1925,1929, 1938, 1942, 1951, 1955, 1964, 1968, 1977, 1981, 1990, 1994, 2003, 2007, 2016, 2020, 2029, 2033, 2069, 2073, 2082, 2086, 2095, 2099, 2108, 2112, 2121, 2125, 2134, 2138, 2147, 2151, 2160, 2164, 2173, 2177, 2186, 2190, 2228, 2232, 2241, 2245, 2254, 2258, 2267, 2271, 2280, 2284, 2293, 2297, 2306, 2310, 2319, 2323, 2332, 2336, 2345, 2349, 2358, 2362, 2371, 2375, 2411, 2415, 2424, 2428, 2437, 2441, 2450, 2454, 2463, 2467, 2476, 2480, 2489, 2493, 2502, 2506, 2515, 2519, 2528, 2532, 2541, 2545, 2554, 2558, 2594, 2598, 2607, 2611, 2620, 2624, 2633, 2637, 2646, 2650, 2659, 2663, 2672, 2676, 2685, 2689, 2698, 2702, 2711, 2715, 2724, 2728, 2737, 2741, 2777, 2781, 2790, 2794, 2803, 2807, 2816, 2820, 2829, 2833, 2842, 2846, 2855, 2859, 2868, 2872, 2881, 2885, 2894, 2898, 2907, 2911, 2920, 2924, 2960, 2964, 2973, 2977, 2986, 2990, 2999, 3003, 3012, 3016, 3025, 3029, 3038, 3042, 3051, 3055, 3064, 3068, 3077, 3081, 3119, 3123, 3132, 3136, 3145, 3149, 3158, 3162, 3171, 3175, 3184, 3188, 3197, 3201, 3210, 3214, 3223, 3227, 3236, 3240, 3249, 3253, 3262, 3266])
'''
{{ <row>L1_ZeroBias_copy,  265, 1</row>}}
{{ <row>L1_ZeroBias_copy,  865, 1</row>}}
{{ <row>L1_ZeroBias_copy, 1780, 1</row>}}
{{ <row>L1_ZeroBias_copy, 2192, 1</row>}}
{{ <row>L1_ZeroBias_copy, 3380, 1</row>}}
'''

process.d0_phi_analyzer.PVFitter.maxNrStoredVertices         = 200000

process.d0_phi_analyzer.PVFitter.Apply3DFit                  = True
process.d0_phi_analyzer.PVFitter.minNrVerticesForFit         = 10
process.d0_phi_analyzer.PVFitter.nSigmaCut                   = 50.0
process.d0_phi_analyzer.PVFitter.VertexCollection            = 'hiSelectedVertex'

process.d0_phi_analyzer.PVFitter.errorScale                  = 0.9
# process.d0_phi_analyzer.PVFitter.useOnlyFirstPV              = cms.untracked.bool(True)
# process.d0_phi_analyzer.PVFitter.minSumPt                    = cms.untracked.double(50.)
# process.d0_phi_analyzer.PVFitter.minVertexNTracks            = cms.untracked.uint32(30)

process.d0_phi_analyzer.BSAnalyzerParameters.fitEveryNLumi   = -1#-1
process.d0_phi_analyzer.BSAnalyzerParameters.resetEveryNLumi = -1#-1


process.p = cms.Path(process.d0_phi_analyzer)
