/*
  Based on the jet response analyzer
  Modified by Matt Nguyen, November 2010
*/

#include "HeavyIonsAnalysis/JetAnalysis/interface/HiInclusiveJetAnalyzer.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "fastjet/contrib/Njettiness.hh"
#include "fastjet/AreaDefinition.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/ClusterSequenceArea.hh"
#include "fastjet/contrib/SoftDrop.hh"
#include "fastjet/JetDefinition.hh"
#include "TLorentzVector.h"
#include <random>
#include "TRandom.h"
#include "TH1.h"
#include "TH2.h"
#include "TRandom3.h"
#include <math.h>

using namespace std;
using namespace edm;
using namespace reco;

HiInclusiveJetAnalyzer::HiInclusiveJetAnalyzer(const edm::ParameterSet& iConfig) {
  doMatch_ = iConfig.getUntrackedParameter<bool>("matchJets",false);
  jetTag_ = consumes<pat::JetCollection> (iConfig.getParameter<InputTag>("jetTag"));
  matchTag_ = consumes<pat::JetCollection> (iConfig.getUntrackedParameter<InputTag>("matchTag"));

  vtxTag_ = consumes<vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("vtxTag"));
  trackTag_ = consumes<reco::TrackCollection> (iConfig.getParameter<InputTag>("trackTag"));
  useQuality_ = iConfig.getUntrackedParameter<bool>("useQuality",1);
  trackQuality_ = iConfig.getUntrackedParameter<string>("trackQuality","highPurity");

  jetName_ = iConfig.getUntrackedParameter<string>("jetName");
  doGenSym_ = iConfig.getUntrackedParameter<bool>("doGenSym",0);
  doSubJets_ = iConfig.getUntrackedParameter<bool>("doSubJets",0);

  doBtagging_ = iConfig.getUntrackedParameter<bool>("doBtagging", false);
  doJetConstituents_ = iConfig.getUntrackedParameter<bool>("doJetConstituents", false);

  //reWTA reclustering
  doWTARecluster_ = iConfig.getUntrackedParameter<bool>("doWTARecluster", false);

  if (doGenSym_){
    tokenGenSym_ = consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("genSym"));
    tokenGenDroppedBranches_ = consumes<edm::ValueMap<int> >(iConfig.getParameter<edm::InputTag>("genDroppedBranches"));
  }

  isMC_ = iConfig.getUntrackedParameter<bool>("isMC",true);
  useHepMC_ = iConfig.getUntrackedParameter<bool> ("useHepMC",false);
  fillGenJets_ = iConfig.getUntrackedParameter<bool>("fillGenJets",false);

  doHiJetID_ = iConfig.getUntrackedParameter<bool>("doHiJetID",false);
  doStandardJetID_ = iConfig.getUntrackedParameter<bool>("doStandardJetID",false);

  rParam = iConfig.getParameter<double>("rParam");
  hardPtMin_ = iConfig.getUntrackedParameter<double>("hardPtMin",4);
  minConstituentPt_ = iConfig.getUntrackedParameter<double>("minConstituentPt", 0.);
  jetPtMin_ = iConfig.getParameter<double>("jetPtMin");
  mysdcut1 = iConfig.getParameter<double>("mysdcut1");
  mysdcut2 = iConfig.getParameter<double>("mysdcut2");
  mydynktcut = iConfig.getParameter<double>("mydynktcut");
  groom_type = iConfig.getParameter<double>("groom_type");
  groom_combine = iConfig.getParameter<double>("groom_combine");
  jetAbsEtaMax_ = iConfig.getUntrackedParameter<double>("jetAbsEtaMax", 2.5);

  if(isMC_){
    genjetTag_ = consumes<edm::View<reco::GenJet>>(iConfig.getParameter<InputTag>("genjetTag"));
    if(useHepMC_) eventInfoTag_ = consumes<HepMCProduct> (iConfig.getParameter<InputTag>("eventInfoTag"));
    eventGenInfoTag_ = consumes<GenEventInfoProduct> (iConfig.getParameter<InputTag>("eventInfoTag"));
  }
  verbose_ = iConfig.getUntrackedParameter<bool>("verbose",false);
  useVtx_ = iConfig.getUntrackedParameter<bool>("useVtx",false);
  useRawPt_ = iConfig.getUntrackedParameter<bool>("useRawPt",true);

  doLifeTimeTagging_ = iConfig.getUntrackedParameter<bool>("doLifeTimeTagging",false);
  doLifeTimeCandidateTagging_ = iConfig.getUntrackedParameter<bool>("doLifeTimeCandidateTagging",false);
  doLifeTimeTaggingExtras_ = iConfig.getUntrackedParameter<bool>("doLifeTimeTaggingExtras",true);
  saveBfragments_  = iConfig.getUntrackedParameter<bool>("saveBfragments",false);

  doTower = iConfig.getUntrackedParameter<bool>("doTower",false);
  if(doTower){
    TowerSrc_ = consumes<CaloTowerCollection>(iConfig.getParameter<edm::InputTag>("towersSrc"));
  }

  doExtraCTagging_ = iConfig.getUntrackedParameter<bool>("doExtraCTagging",false);

  pfCandidateToken_ = consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("pfCandSource"));

  if(isMC_){
    genParticleSrc_ = consumes<reco::GenParticleCollection>(iConfig.getUntrackedParameter<edm::InputTag>("genParticles"));
  }

  doChargedConstOnly_ = iConfig.getUntrackedParameter<bool>("doChargedConstOnly",0);
  TrackVariation_ = 1;
  pfChargedCandidateEnergyScale_ = 1;
  pfNeutralCandidateEnergyScale_ = 1;
  pfGammaCandidateEnergyScale_ = 1;
  pfNeutralSmear_ = false;
  doNaiveNeuPFScaling_ = false;
  doRatioNeuPFScaling_ = false;
  doPeripheralNeuPFScaling_ = false;
  doCompensatoryNeuPFScaling_ = false;

  doPrimaryLJPReco_ = iConfig.getUntrackedParameter<bool>("doPrimaryLJPReco", false);
  if(isMC_){
    doPrimaryLJPTruth_ = iConfig.getUntrackedParameter<bool>("doPrimaryLJPTruth", false);
    pfChargedCandidateEnergyScale_ = iConfig.getUntrackedParameter<double>("pfChargedEnergyScaleVar",1.);
    pfNeutralCandidateEnergyScale_ = iConfig.getUntrackedParameter<double>("pfNeutralEnergyScaleVar",1.);
    pfGammaCandidateEnergyScale_ = iConfig.getUntrackedParameter<double>("pfGammaEnergyScaleVar",1.);
    pfNeutralSmear_ = iConfig.getUntrackedParameter<bool>("pfNeutralSmear", false);
    doNaiveNeuPFScaling_ = iConfig.getUntrackedParameter<bool>("doNaiveNeuPFScaling", false);
    doRatioNeuPFScaling_ = iConfig.getUntrackedParameter<bool>("doRatioNeuPFScaling", false);
    doPeripheralNeuPFScaling_ = iConfig.getUntrackedParameter<bool>("doPeripheralNeuPFScaling", false);
    doCompensatoryNeuPFScaling_ = iConfig.getUntrackedParameter<bool>("doCompensatoryNeuPFScaling", false);
    TrackVariation_ = iConfig.getUntrackedParameter<double>("TrackVariation",0.);

    genPtMin_ = iConfig.getUntrackedParameter<double>("genPtMin",10);
    dopthatcut = iConfig.getUntrackedParameter<bool>("dopthatcut",0);
    doHardestSplitMatching_ = iConfig.getUntrackedParameter<bool>("doHardestSplitMatching",0);
    doFullPLJPmatching_ = iConfig.getUntrackedParameter<bool>("doFullPLJPmatching",0);
  }

  // ==== BTAGGING TOKENS ====
  if (doBtagging_) {
    for (const std::string label : {"pfJetProbabilityBJetTag", "pfDeepCSVJetTags", "pfDeepFlavourJetTags", "pfParticleTransformerAK4JetTags", "pfUnifiedParticleTransformerAK4JetTags"}) {
      const auto& tag = iConfig.getUntrackedParameter<string>(label, "");
      if (tag.empty())
        continue;
      else if (label == "pfJetProbabilityBJetTag")
        jetTaggers_["pfJP"].emplace("probb", consumes<JetTagCollection>(tag));
      else if (label == "pfDeepCSVJetTags")
        for (const auto& cat : {"probb", "probbb"})
          jetTaggers_["deepCSV"].emplace(cat, consumes<JetTagCollection>(tag+":"+cat));
      else if (label == "pfDeepFlavourJetTags")
        for (const auto& cat : {"probb", "probbb", "problepb"})
          jetTaggers_["deepFlavour"].emplace(cat, consumes<JetTagCollection>(tag+":"+cat));
      else if (label == "pfParticleTransformerAK4JetTags")
        for (const auto& cat : {"probb", "probbb", "problepb"})
          jetTaggers_["particleTransformer"].emplace(cat, consumes<JetTagCollection>(tag+":"+cat));
      else if (label == "pfUnifiedParticleTransformerAK4JetTags")
        for (const auto& cat : {"probb", "probbb", "problepb", "probc", "probg", "probu", "probd", "probs",
          "probtaup1h0p", "probtaup1h1p", "probtaup1h2p", "probtaup3h0p", "probtaup3h1p", "probtaum1h0p", "probtaum1h1p", "probtaum1h2p", "probtaum3h0p", "probtaum3h1p",
          "probele", "probmu", "ptcorr", "ptnu"})
          jetTaggers_["unifiedParticleTransformer"].emplace(cat, consumes<JetTagCollection>(tag+":"+cat));
    }
  }
}

HiInclusiveJetAnalyzer::~HiInclusiveJetAnalyzer() {}

void HiInclusiveJetAnalyzer::beginRun(const edm::Run& run, const edm::EventSetup& es) {}
void HiInclusiveJetAnalyzer::endRun(const edm::Run& run, const edm::EventSetup& es) {}

void HiInclusiveJetAnalyzer::beginJob() {
  std::cout << "Running job with systematics" << std::endl;
  std::cout << "Reco cut on jet constituents for reclustering: " << minConstituentPt_ << std::endl;
  std::cout << "Doing Charged only: " << doChargedConstOnly_ << std::endl;
  std::cout << "Track efficiency var: " << TrackVariation_ << std::endl;
  std::cout << "Charged pfCand 4-mom var: " << pfChargedCandidateEnergyScale_ << std::endl;
  std::cout << "Neutral pfCand 4-mom var: " << pfNeutralCandidateEnergyScale_ << std::endl;
  std::cout << "Photon pfCand 4-mom var: " << pfGammaCandidateEnergyScale_ << std::endl;
  std::cout << "Neutral phi and rapidity smearing: " << pfNeutralSmear_ << std::endl;
  string jetTagTitle = jetTagLabel_.label()+" Jet Analysis Tree";
  t = fs1->make<TTree>("t",jetTagTitle.c_str());
  t->Branch("run",&jets_.run,"run/I");
  t->Branch("evt",&jets_.evt,"evt/I");
  t->Branch("lumi",&jets_.lumi,"lumi/I");
  if (useVtx_) {
    t->Branch("vx",&jets_.vx,"vx/F");
    t->Branch("vy",&jets_.vy,"vy/F");
    t->Branch("vz",&jets_.vz,"vz/F");
  }

  t->Branch("nref",&jets_.nref,"nref/I");
  t->Branch("jtptUncorrected",jets_.rawpt,"jtptUncorrected[nref]/F");
  t->Branch("jtEUncorrected",jets_.jtrawE,"jtEUncorrected[nref]/F");
  if(doCompensatoryNeuPFScaling_ or doNaiveNeuPFScaling_ or doRatioNeuPFScaling_)
    t->Branch("jtptMap", jets_.jtMapPt, "jtptMap[nref]/F");
  t->Branch("jtpt",jets_.jtpt,"jtpt[nref]/F");
  t->Branch("jteta",jets_.jteta,"jteta[nref]/F");
  t->Branch("jtphi",jets_.jtphi,"jtphi[nref]/F");

  // WTA Branches
  if (doWTARecluster_) {
    t->Branch("WTAeta", jets_.WTAeta, "WTAeta[nref]/F");
    t->Branch("WTAphi", jets_.WTAphi, "WTAphi[nref]/F");
  }

  // ==== BTAGGING BRANCHES WITH MEMORY FIX ====
  if (doBtagging_) {
    for (const auto& tg : jetTaggers_) {
      auto& discr = jets_discr_[tg.first];
      discr["b"].resize(10000, 0.0); // RESIZE FIX
      t->Branch(("discr_"+tg.first).c_str(), discr["b"].data(), ("discr_"+tg.first+"[nref]/F").c_str());
      if (tg.first == "unifiedParticleTransformer") {
        discr["probtau"].resize(10000, 0.0); // RESIZE FIX
        t->Branch(("discr_"+tg.first+"_probtau").c_str(), discr["probtau"].data(), ("discr_"+tg.first+"_probtau[nref]/F").c_str());
        for (const auto& c : tg.second) {
          if (c.first.rfind("probtau",0)!=0) {
            discr[c.first].resize(10000, 0.0); // RESIZE FIX
            t->Branch(("discr_"+tg.first+"_"+c.first).c_str(), discr[c.first].data(), ("discr_"+tg.first+"_"+c.first+"[nref]/F").c_str());
          }
        }
      }
    }
  }

  if (doHiJetID_) {
    /*
    t->Branch("trackMax", jets_.trackMax, "trackMax[nref]/F");
    t->Branch("trackSum", jets_.trackSum, "trackSum[nref]/F");
    t->Branch("trackN", jets_.trackN, "trackN[nref]/I");
    t->Branch("trackHardSum", jets_.trackHardSum, "trackHardSum[nref]/F");
    t->Branch("trackHardN", jets_.trackHardN, "trackHardN[nref]/I");
    */
    t->Branch("chargedMax", jets_.chargedMax, "chargedMax[nref]/F");
    t->Branch("chargedSum", jets_.chargedSum, "chargedSum[nref]/F");
    t->Branch("chargedN", jets_.chargedN, "chargedN[nref]/I");
    t->Branch("chargedHardSum", jets_.chargedHardSum, "chargedHardSum[nref]/F");
    t->Branch("chargedHardN", jets_.chargedHardN, "chargedHardN[nref]/I");
    /*
    t->Branch("photonMax", jets_.photonMax, "photonMax[nref]/F");
    t->Branch("photonSum", jets_.photonSum, "photonSum[nref]/F");
    t->Branch("photonN", jets_.photonN, "photonN[nref]/I");
    t->Branch("photonHardSum", jets_.photonHardSum, "photonHardSum[nref]/F");
    t->Branch("photonHardN", jets_.photonHardN, "photonHardN[nref]/I");

    t->Branch("neutralMax", jets_.neutralMax, "neutralMax[nref]/F");
    t->Branch("neutralSum", jets_.neutralSum, "neutralSum[nref]/F");
    t->Branch("neutralN", jets_.neutralN, "neutralN[nref]/I");

    t->Branch("eMax", jets_.eMax, "eMax[nref]/F");
    t->Branch("eSum", jets_.eSum, "eSum[nref]/F");
    t->Branch("eN", jets_.eN, "eN[nref]/I");

    t->Branch("eg_HFMax", jets_.eg_HFMax, "eg_HFMax[nref]/F");
    t->Branch("eg_HFSum", jets_.eg_HFSum, "eg_HFSum[nref]/F");
    t->Branch("eg_HFN", jets_.eg_HFN, "eg_HFN[nref]/I");

    t->Branch("h_HFMax", jets_.h_HFMax, "h_HFMax[nref]/F");
    t->Branch("h_HFSum", jets_.h_HFSum, "h_HFSum[nref]/F");
    t->Branch("h_HFN", jets_.h_HFN, "h_HFN[nref]/I");

    t->Branch("muMax", jets_.muMax, "muMax[nref]/F");
    t->Branch("muSum", jets_.muSum, "muSum[nref]/F");
    t->Branch("muN", jets_.muN, "muN[nref]/I");
    */
  }

  if (doStandardJetID_) {
    t->Branch("fHPD", jets_.fHPD, "fHPD[nref]/F");
    t->Branch("fRBX", jets_.fRBX, "fRBX[nref]/F");
    t->Branch("n90", jets_.n90, "n90[nref]/I");
    t->Branch("fSubDet1", jets_.fSubDet1, "fSubDet1[nref]/F");
    t->Branch("fSubDet2", jets_.fSubDet2, "fSubDet2[nref]/F");
    t->Branch("fSubDet3", jets_.fSubDet3, "fSubDet3[nref]/F");
    t->Branch("fSubDet4", jets_.fSubDet4, "fSubDet4[nref]/F");
    t->Branch("restrictedEMF", jets_.restrictedEMF, "restrictedEMF[nref]/F");
    t->Branch("nHCAL", jets_.nHCAL, "nHCAL[nref]/I");
    t->Branch("nECAL", jets_.nECAL, "nECAL[nref]/I");
    t->Branch("apprHPD", jets_.apprHPD, "apprHPD[nref]/F");
    t->Branch("apprRBX", jets_.apprRBX, "apprRBX[nref]/F");
    t->Branch("n2RPC", jets_.n2RPC, "n2RPC[nref]/I");
    t->Branch("n3RPC", jets_.n3RPC, "n3RPC[nref]/I");
    t->Branch("nRPC", jets_.nRPC, "nRPC[nref]/I");

    t->Branch("fEB", jets_.fEB, "fEB[nref]/F");
    t->Branch("fEE", jets_.fEE, "fEE[nref]/F");
    t->Branch("fHB", jets_.fHB, "fHB[nref]/F");
    t->Branch("fHE", jets_.fHE, "fHE[nref]/F");
    t->Branch("fHO", jets_.fHO, "fHO[nref]/F");
    t->Branch("fLong", jets_.fLong, "fLong[nref]/F");
    t->Branch("fShort", jets_.fShort, "fShort[nref]/F");
    t->Branch("fLS", jets_.fLS, "fLS[nref]/F");
    t->Branch("fHFOOT", jets_.fHFOOT, "fHFOOT[nref]/F");
  }

  t->Branch("jtdyn_split",jets_.jtdyn_split,"jtdyn_split[nref]/I");
  t->Branch("jtdyn_eta",jets_.jtdyn_eta,"jtdyn_eta[nref]/F");
  t->Branch("jtdyn_phi",jets_.jtdyn_phi,"jtdyn_phi[nref]/F");
  t->Branch("jtdyn_deltaR",jets_.jtdyn_deltaR,"jtdyn_deltaR[nref]/F");
  t->Branch("jtdyn_kt",jets_.jtdyn_kt,"jtdyn_kt[nref]/F");
  t->Branch("jtdyn_z",jets_.jtdyn_z,"jtdyn_z[nref]/F");

  t->Branch("jt_intjet_multi", jets_.jt_intjet_multi,"jt_intjet_multi[nref]/I");
  t->Branch("jt_girth", jets_.jt_girth, "jt_girth[nref]/F");
  t->Branch("jt_girth_new", jets_.jt_girth_new, "jt_girth_new[nref]/F");
  t->Branch("jt_thrust", jets_.jt_thrust,"jt_thrust[nref]/I");
  t->Branch("jt_LHA", jets_.jt_LHA,"jt_LHA[nref]/I");
  t->Branch("jt_pTD", jets_.jt_pTD,"jt_pTD[nref]/I");
  
  if(doPrimaryLJPReco_){
    t->Branch("jt_PLJPkT",&jets_.jt_PLJPkT);
    t->Branch("jt_PLJPdR",&jets_.jt_PLJPdR);
    t->Branch("jt_PLJPeta",&jets_.jt_PLJPeta);
    t->Branch("jt_PLJPphi",&jets_.jt_PLJPphi);
  }

  if(isMC_){
    if (useHepMC_) {
      t->Branch("beamId1",&jets_.beamId1,"beamId1/I");
      t->Branch("beamId2",&jets_.beamId2,"beamId2/I");
    }
    // Only matched gen jets
    t->Branch("refpt",jets_.refpt,"refpt[nref]/F");
    t->Branch("refeta",jets_.refeta,"refeta[nref]/F");
    t->Branch("refphi",jets_.refphi,"refphi[nref]/F");
    
    // Gen WTA Branches
    if (doWTARecluster_) {
      t->Branch("refWTAeta", jets_.refWTAeta, "refWTAeta[nref]/F");
      t->Branch("refWTAphi", jets_.refWTAphi, "refWTAphi[nref]/F");
    }

    t->Branch("refdyn_split",jets_.refdyn_split,"refdyn_split[nref]/I");
    t->Branch("refdyn_eta",jets_.refdyn_eta,"refdyn_eta[nref]/F");
    t->Branch("refdyn_phi",jets_.refdyn_phi,"refdyn_phi[nref]/F");
    t->Branch("refdyn_deltaR",jets_.refdyn_deltaR,"refdyn_deltaR[nref]/F");
    t->Branch("refdyn_kt",jets_.refdyn_kt,"refdyn_kt[nref]/F");
    t->Branch("refdyn_z",jets_.refdyn_z,"refdyn_z[nref]/F");
    
    t->Branch("jtdyn_isClosestToTruth", jets_.jtdyn_isClosestToTruth,"jtdyn_isClosestToTruth[nref]/O");
    t->Branch("refdyn_isClosestToReco", jets_.refdyn_isClosestToReco,"refdyn_isClosestToReco[nref]/O");
    t->Branch("jtdyn_refdyn_dR", jets_.jtdyn_refdyn_dR,"jtdyn_refdyn_dR[nref]/F");

    t->Branch("ref_intjet_multi", jets_.ref_intjet_multi,"ref_intjet_multi[nref]/I");
    t->Branch("ref_girth", jets_.ref_girth, "ref_girth[nref]/F");
    t->Branch("ref_girth_new", jets_.ref_girth_new, "ref_girth_new[nref]/F");
    t->Branch("ref_thrust", jets_.ref_thrust,"ref_thrust[nref]/I");
    t->Branch("ref_LHA", jets_.ref_LHA,"ref_LHA[nref]/I");
    t->Branch("ref_pTD", jets_.ref_pTD,"ref_pTD[nref]/I");
    
    if(doFullPLJPmatching_){
      t->Branch("jt_PLJP_RtoTmatch_idx",&jets_.PLJP_RtoTmatch_idx);
      t->Branch("jt_PLJP_TtoRmatch_idx",&jets_.PLJP_TtoRmatch_idx);
      t->Branch("jt_PLJP_RtoTmatch_dR",&jets_.PLJP_RtoTmatch_dR);
      t->Branch("jt_PLJP_TtoRmatch_dR",&jets_.PLJP_TtoRmatch_dR);
    }

    if(doPrimaryLJPTruth_){
      t->Branch("ref_PLJPkT",&jets_.ref_PLJPkT);
      t->Branch("ref_PLJPdR",&jets_.ref_PLJPdR);
      t->Branch("ref_PLJPeta",&jets_.ref_PLJPeta);
      t->Branch("ref_PLJPphi",&jets_.ref_PLJPphi);
    }
    
    t->Branch("refparton_pt",jets_.refparton_pt,"refparton_pt[nref]/F");
    t->Branch("refparton_flavor",jets_.refparton_flavor,"refparton_flavor[nref]/I");
  }    

  float x[83] = {-5.191, -4.889, -4.716, -4.538, -4.363, -4.191, -4.013, -3.839, -3.664, -3.489, -3.314, -3.139, -2.964, -2.853, -2.65, -2.5, -2.322, -2.172, -2.043, -1.93, -1.83, -1.74, -1.653, -1.566, -1.479, -1.392, -1.305, -1.218, -1.131, -1.044, -0.957, -0.879, -0.783, -0.696, -0.609, -0.522, -0.435, -0.348, -0.261, -0.174, -0.087, 0, 0.087, 0.174, 0.261, 0.348, 0.435, 0.522, 0.609, 0.696, 0.783, 0.879, 0.957, 1.044, 1.131, 1.218, 1.305, 1.392, 1.479, 1.566, 1.653, 1.74, 1.83, 1.93, 2.043, 2.172, 2.322, 2.5, 2.65, 2.853, 2.964, 3.139, 3.314, 3.489, 3.664, 3.839, 4.013, 4.191, 4.363, 4.538, 4.716, 4.889, 5.191};
  float y[73] = {-3.14159, -3.05433, -2.96706, -2.87979, -2.79253, -2.70526, -2.61799, -2.53073, -2.44346, -2.35619, -2.26893, -2.18166, -2.0944, -2.00713, -1.91986, -1.8326, -1.74533, -1.65806, -1.5708, -1.48353, -1.39626, -1.309, -1.22173, -1.13446, -1.0472, -0.959931, -0.872665, -0.785398, -0.698132, -0.610865, -0.523599, -0.436332, -0.349066, -0.261799, -0.174533, -0.0872665, 0, 0.0872665, 0.174533, 0.261799, 0.349066, 0.436332, 0.523599, 0.610865, 0.698132, 0.785398, 0.872665, 0.959931, 1.0472, 1.13446, 1.22173, 1.309, 1.39626, 1.48353, 1.5708, 1.65806, 1.74533, 1.8326, 1.91986, 2.00713, 2.0944, 2.18166, 2.26893, 2.35619, 2.44346, 2.53073, 2.61799, 2.70526, 2.79253, 2.87979, 2.96706, 3.05433, 3.14159};
  Asymm_map_ = new TH2F("Asymm_map","Asymm_map", 82, x, 72, y);

  if (doBtagging_) {
    for (auto& t : jets_discr_)
      for (auto& c : t.second)
        std::fill(c.second.begin(), c.second.end(), 0.0);
  }
}

void HiInclusiveJetAnalyzer::analyze(const Event& iEvent, const EventSetup& iSetup) {
  int event = iEvent.id().event();
  int run = iEvent.id().run();
  int lumi = iEvent.id().luminosityBlock();

  jets_.run = run;
  jets_.evt = event;
  jets_.lumi = lumi;

  LogDebug("HiInclusiveJetAnalyzer")<<"START event: "<<event<<" in run "<<run<<endl;

  reco::Vertex::Point vtx(0,0,0);
  if (useVtx_) {
    edm::Handle<vector<reco::Vertex> >vertex;
    iEvent.getByToken(vtxTag_, vertex);
    if(vertex->size()>0) {
      jets_.vx = vertex->begin()->x();
      jets_.vy = vertex->begin()->y();
      jets_.vz = vertex->begin()->z();
      vtx = vertex->begin()->position();
    }
  }

  edm::Handle<pat::JetCollection> jets;
  iEvent.getByToken(jetTag_, jets);

  edm::Handle<pat::JetCollection> matchedjets;
  iEvent.getByToken(matchTag_, matchedjets);

  auto const& pfCandidates = iEvent.get(pfCandidateToken_);

  edm::Handle<reco::TrackCollection> tracks;
  iEvent.getByToken(trackTag_,tracks);
    
  edm::Handle<CaloTowerCollection> towers;
  if(doTower){
    iEvent.getByToken(TowerSrc_,towers);
  }

  double pthat = 0;
  if(isMC_){
    edm::Handle<GenEventInfoProduct> hEventInfo;
    iEvent.getByToken(eventGenInfoTag_,hEventInfo);
    pthat = hEventInfo->qScale();
  }

  // ==== BTAGGING HANDLES ====
  std::map<std::string, std::map<std::string, edm::Handle<reco::JetTagCollection>>> jetTaggers;
  if (doBtagging_) {
    for (const auto& t : jetTaggers_) {
      for (const auto& c : t.second) {
        jetTaggers[t.first].emplace(c.first, iEvent.getHandle(c.second));
      }
    }
  }

  // ==== INLINE BTAGGING LAMBDA ====
  auto getTag = [](const edm::Handle<reco::JetTagCollection> &bTags,const pat::Jet &jet) {
    if(!bTags.isValid()) return -999.0f; // PREVENT SEGFAULT IF TAGGER MISSING
    float tagValue(-999), maxDR2(9.8690); // = 3.1415^2
    for (const auto &t : *bTags) {
      auto const dR2 = reco::deltaR2(jet, *(t.first));
      if (dR2 > maxDR2) continue;
      maxDR2=dR2;
      tagValue=t.second;
    }
    if(maxDR2 > 0.16) tagValue=-999; // 0.16 = 0.4^2
    return tagValue;
  };

  // ==== DEFINE WTA RECLUSTERING SCHEME ====
  fastjet::JetDefinition WTAjtDef(fastjet::antikt_algorithm, rParam, fastjet::WTA_pt_scheme);

  jets_.nref = 0;

  for(unsigned int j = 0; j < jets->size(); ++j){
    const pat::Jet& jet = (*jets)[j];
    auto pt = useRawPt_ ? jet.correctedJet("Uncorrected").pt() : jet.pt();
    
    if(pt < jetPtMin_) continue;

    jets_.rawpt[jets_.nref] = jet.correctedJet("Uncorrected").pt();
    jets_.jtrawE[jets_.nref] = jet.correctedJet("Uncorrected").energy();
    jets_.jtMapPt[jets_.nref] = jets_.rawpt[jets_.nref]*(1+ReadJetAsymmMap(jet.eta(), jet.phi(), *Asymm_map_));
    jets_.jtpt[jets_.nref] = jet.pt();
    jets_.jteta[jets_.nref] = jet.eta();
    jets_.jtphi[jets_.nref] = jet.phi();

    // -------------------------------------------------------------
    // Extract b-tagging using reference logic
    // -------------------------------------------------------------
    if (doBtagging_) {
      for (const auto& t : jetTaggers) {
        auto& discr = jets_discr_.at(t.first);
        if (t.first == "pfJP")
          discr["b"][jets_.nref] = getTag(t.second.at("probb"),jet);
        else if (t.first == "deepCSV")
          discr["b"][jets_.nref]  = getTag(t.second.at("probb"),jet)+getTag(t.second.at("probbb"),jet);
        else if (t.first == "deepFlavour" || t.first == "particleTransformer" || t.first == "unifiedParticleTransformer")
          discr["b"][jets_.nref] = getTag(t.second.at("probb"),jet)+getTag(t.second.at("probbb"),jet)+getTag(t.second.at("problepb"),jet);
        
        if (t.first == "unifiedParticleTransformer") {
          float tag(0.0);
          for (const auto& n : {"probtaup1h0p", "probtaup1h1p", "probtaup1h2p", "probtaup3h0p", "probtaup3h1p", "probtaum1h0p", "probtaum1h1p", "probtaum1h2p", "probtaum3h0p", "probtaum3h1p"})
            tag += getTag(t.second.at(n), jet);
          discr["probtau"][jets_.nref] = tag;
          for (const auto& c : t.second)
            if (c.first.rfind("probtau",0)!=0)
              discr[c.first][jets_.nref] = getTag(c.second,jet);
        }
      }
    }

    // -------------------------------------------------------------
    // Calculate Winner-Takes-All Axis for Reco Jet
    // -------------------------------------------------------------
    if (doWTARecluster_) {
      std::vector<fastjet::PseudoJet> candidates;
      auto daughters = jet.getJetConstituents();
      for (auto it = daughters.begin(); it != daughters.end(); ++it) {
        candidates.push_back(fastjet::PseudoJet((**it).px(), (**it).py(), (**it).pz(), (**it).energy()));
      }
      auto cs = new fastjet::ClusterSequence(candidates, WTAjtDef);
      std::vector<fastjet::PseudoJet> wtajt = fastjet::sorted_by_pt(cs->inclusive_jets(0));

      jets_.WTAeta[jets_.nref] = (!wtajt.empty()) ? wtajt[0].eta() : -999;
      jets_.WTAphi[jets_.nref] = (!wtajt.empty()) ? wtajt[0].phi_std() : -999;
      delete cs;
    }

    jets_.jtdyn_split[jets_.nref] = 0;
    jets_.jtdyn_kt[jets_.nref] = 0;
    jets_.jtdyn_z[jets_.nref] = 0;

    if(doFullPLJPmatching_ or doHardestSplitMatching_){
      jets_.jtJetConstituent = {};
      jets_.refJetConstituent = {};
    }
    
    IterativeDeclusteringRec(groom_type, groom_combine, jet);

    jets_.refpt[jets_.nref] = 0;
    jets_.refeta[jets_.nref] = 0;
    jets_.refphi[jets_.nref] = 0;
    jets_.refsym[jets_.nref] = 0.;

    jets_.refdyn_split[jets_.nref] = 0;
    jets_.refdyn_kt[jets_.nref] = 0;
    jets_.refdyn_z[jets_.nref] = 0;
    jets_.jtdyn_isClosestToTruth[jets_.nref] = 0;
    jets_.refdyn_isClosestToReco[jets_.nref] = 0;
    jets_.jtdyn_refdyn_dR[jets_.nref] = 0;

    if(isMC_){
      const reco::GenJet * genjet = jet.genJet();
      
      if(!genjet or (genjet and dopthatcut and pthat<0.35*genjet->pt())){
        jets_.refdyn_split[jets_.nref] = std::numeric_limits<int>::min();
        jets_.refdyn_eta[jets_.nref] = -std::numeric_limits<double>::max();
        jets_.refdyn_phi[jets_.nref] = -std::numeric_limits<double>::max();
        jets_.refdyn_deltaR[jets_.nref] = - std::numeric_limits<double>::max();
        jets_.refdyn_kt[jets_.nref] = - std::numeric_limits<double>::max();
        jets_.refdyn_z[jets_.nref] = - std::numeric_limits<double>::max();
        jets_.ref_intjet_multi[jets_.nref] = std::numeric_limits<int>::min();
        jets_.ref_girth[jets_.nref] = - std::numeric_limits<double>::max();
        jets_.ref_girth_new[jets_.nref] = - std::numeric_limits<double>::max();
        jets_.ref_thrust[jets_.nref] = - std::numeric_limits<double>::max();
        jets_.ref_LHA[jets_.nref] = - std::numeric_limits<double>::max();
        jets_.ref_pTD[jets_.nref] = - std::numeric_limits<double>::max();
        jets_.ref_PLJPkT.push_back({});
        jets_.ref_PLJPdR.push_back({});
        jets_.ref_PLJPeta.push_back({});
        jets_.ref_PLJPphi.push_back({});
        jets_.refpt[jets_.nref] = - std::numeric_limits<double>::max();
        jets_.refeta[jets_.nref] = - std::numeric_limits<double>::max();
        jets_.refphi[jets_.nref] = - std::numeric_limits<double>::max();
        jets_.PLJP_TtoRmatch_dR.push_back({});
        jets_.PLJP_TtoRmatch_idx.push_back({});
        jets_.PLJP_RtoTmatch_dR.push_back({});
        jets_.PLJP_RtoTmatch_idx.push_back({});
        jets_.refdyn_isClosestToReco[jets_.nref] = false;
        jets_.jtdyn_isClosestToTruth[jets_.nref] = false;
        jets_.jtdyn_refdyn_dR[jets_.nref] = std::numeric_limits<float>::max();

        if (doWTARecluster_) {
          jets_.refWTAeta[jets_.nref] = -std::numeric_limits<double>::max();
          jets_.refWTAphi[jets_.nref] = -std::numeric_limits<double>::max();
        }
      }
      else{
        if(jet.genParton()){
          const reco::GenParticle & parton = *jet.genParton();
          jets_.refparton_pt[jets_.nref] = parton.pt();
          jets_.refparton_flavor[jets_.nref] = parton.pdgId();
        }
        else {
          jets_.refparton_pt[jets_.nref] = -999;
          jets_.refparton_flavor[jets_.nref] = -999;
        }
        
        jets_.refpt[jets_.nref] = genjet->pt();
        jets_.refeta[jets_.nref] = genjet->eta();
        jets_.refphi[jets_.nref] = genjet->phi();
        
        // -------------------------------------------------------------
        // Calculate Winner-Takes-All Axis for Gen Jet
        // -------------------------------------------------------------
        if (doWTARecluster_) {
          std::vector<fastjet::PseudoJet> candidates;
          auto daughters = genjet->getJetConstituents();
          for (auto it = daughters.begin(); it != daughters.end(); ++it) {
            candidates.push_back(fastjet::PseudoJet((**it).px(), (**it).py(), (**it).pz(), (**it).energy()));
          }
          auto cs = new fastjet::ClusterSequence(candidates, WTAjtDef);
          std::vector<fastjet::PseudoJet> wtajt = fastjet::sorted_by_pt(cs->inclusive_jets(0));

          jets_.refWTAeta[jets_.nref] = (!wtajt.empty()) ? wtajt[0].eta() : -999;
          jets_.refWTAphi[jets_.nref] = (!wtajt.empty()) ? wtajt[0].phi_std() : -999;
          delete cs;
        }

        IterativeDeclusteringGen(groom_type, groom_combine, *genjet);
      
        if(doHardestSplitMatching_){
          TruthRecoRecoTruthMatching();
        }
        if(doFullPLJPmatching_){
          std::vector<float> TtoR_dist = {};
          std::vector<float> RtoT_dist = {};
          std::vector<Int_t> TtoR_idx = {};
          std::vector<Int_t> RtoT_idx = {};
          matchPLJP(TtoR_dist, TtoR_idx, jets_.refJetConstituent, jets_.jtJetConstituent);
          matchPLJP(RtoT_dist, RtoT_idx, jets_.jtJetConstituent, jets_.refJetConstituent);
          jets_.PLJP_TtoRmatch_dR.push_back(TtoR_dist);
          jets_.PLJP_TtoRmatch_idx.push_back(TtoR_idx);
          jets_.PLJP_RtoTmatch_dR.push_back(RtoT_dist);
          jets_.PLJP_RtoTmatch_idx.push_back(RtoT_idx);
        }

        if(doFullPLJPmatching_ or doHardestSplitMatching_){
          jets_.jtJetConstituent = {};
          jets_.refJetConstituent = {};
        }
      }
    }   
    jets_.nref++;
  }
  
  t->Fill();
  
  // Safe zero-initialization to avoid memset vector corruption warnings
  jets_ = JRA();
}

void HiInclusiveJetAnalyzer::IterativeDeclusteringRec(double groom_type, double groom_combine, const reco::Jet& jet)
{
  Double_t map_Corrected_jtpt = jets_.rawpt[jets_.nref];
  Double_t assymDelta_jetpt = 0;
  std::vector <float> jetBoundsInMap = {};
  if(doPeripheralNeuPFScaling_ || doCompensatoryNeuPFScaling_){
    jetBoundsInMap = BinBoundsAsymmMap(jet.eta(), jet.phi(), *Asymm_map_);
    map_Corrected_jtpt = jets_.rawpt[jets_.nref]*(1+ReadJetAsymmMap(jet.eta(), jet.phi(), *Asymm_map_));
    assymDelta_jetpt = map_Corrected_jtpt - jets_.rawpt[jets_.nref];
  }

  TRandom *rand_track_sel = new TRandom3(0);
  TRandom *rand_charge_smear = new TRandom3(0);
  TRandom *rand_hcal_y_smear = new TRandom3(0);
  TRandom *rand_hcal_phi_smear = new TRandom3(0);
  std::vector<Int_t> posDonor = {};
  std::vector<Int_t> posAcceptor = {};

  Int_t intjet_multi = 0;
  float jet_girth = 0;
  float jet_girth_new = 0;
  float jet_thrust = 0;
  float jet_LHA = 0;
  float jet_pTD = 0;
  std::vector<float> jet_PLJPkT = {};
  std::vector<float> jet_PLJPdR = {};
  std::vector<float> jet_PLJPeta = {};
  std::vector<float> jet_PLJPphi = {};
  
  Int_t nsplit = 0;
  double dyn_kt = std::numeric_limits<double>::min();
  Int_t dyn_split = 0;
  double z = 0;
  double dyn_eta = 0;
  double dyn_phi = 0;
  double dyn_deltaR = 0;
  double dyn_z = 0;
  double jet_radius_ca = 1.0;
  
  fastjet::JetDefinition jet_def(fastjet::genkt_algorithm,jet_radius_ca,0,static_cast<fastjet::RecombinationScheme>(0), fastjet::Best);
  fastjet::PseudoJet myjet;
  fastjet::PseudoJet mypart;
  myjet.reset(jet.p4().px(),jet.p4().py(),jet.p4().pz(),jet.p4().e());

  try{
    std::vector<fastjet::PseudoJet> particles = {};
    auto daughters = jet.getJetConstituents();
    Int_t count_it = 0;
    double JetNeutralEnergy = 0.;

    float assymDelta_corePtChange = 0;
    float assymSum_peripheralChange = 0;
    float assymSum_allNeuChange = 0;
    if(isMC_ && (doPeripheralNeuPFScaling_ or doCompensatoryNeuPFScaling_)){
      fastjet::PseudoJet coreSum;
      fastjet::PseudoJet coreSum_modified;
      fastjet::PseudoJet peripheralSum;
      fastjet::PseudoJet peripheralSum_modified;
      fastjet::PseudoJet totalSum;
      fastjet::PseudoJet totalSum_modified;

      coreSum.reset(0,0,0,0);
      coreSum_modified.reset(0,0,0,0);
      for(auto it = daughters.begin(); it!=daughters.end(); ++it){
        Int_t abspdgId = abs((**it).pdgId());
        if(abspdgId!=130) continue;
        fastjet::PseudoJet pseudoNeutral;
        fastjet::PseudoJet pseudoNeutral_modified;
        float neutralMapValue = ReadJetAsymmMap((**it).eta(), (**it).phi(), *Asymm_map_);
        pseudoNeutral.reset((**it).px(), (**it).py(), (**it).pz(), (**it).energy());
        pseudoNeutral_modified.reset((**it).px()*(1.+neutralMapValue), (**it).py()*(1.+neutralMapValue), (**it).pz()*(1.+neutralMapValue), (**it).energy()*(1.+neutralMapValue));
        totalSum = totalSum + pseudoNeutral;
        totalSum_modified = totalSum_modified + pseudoNeutral_modified;
        if((**it).eta() > jetBoundsInMap.at(0) && (**it).eta() > jetBoundsInMap.at(0) && (**it).eta() < jetBoundsInMap.at(1) && (**it).phi() > jetBoundsInMap.at(2) && (**it).phi() < jetBoundsInMap.at(3)){
          coreSum = coreSum + pseudoNeutral;
          coreSum_modified = coreSum_modified + pseudoNeutral_modified;
        }
        else{ 
          peripheralSum = peripheralSum + pseudoNeutral;
          peripheralSum_modified = peripheralSum_modified + pseudoNeutral_modified;
        }
      }
      assymDelta_corePtChange = coreSum_modified.pt() - coreSum.pt();
      assymSum_peripheralChange = peripheralSum_modified.pt() - peripheralSum.pt();
      assymSum_allNeuChange = (totalSum_modified - totalSum).pt();
      if((totalSum_modified - totalSum).e() < 0) assymSum_allNeuChange = - assymSum_allNeuChange;
    }
    
    float peripheralNeutralChange = assymDelta_jetpt - assymDelta_corePtChange; 
    double JetNeutralEnergyFraction = JetNeutralEnergy/jets_.jtrawE[jets_.nref];
    
    for(auto it = daughters.begin(); it!=daughters.end(); ++it){
      if(doHiJetID_){
        incrementJetID(**it);
      }
      if(doChargedConstOnly_ && (**it).charge()==0) continue;
      
      double PFE_scale = 1.;
      double charge_track_smear = 1.;
      double Hcal_y_smear = 1.;
      double Hcal_phi_smear = 1.;
      if(isMC_){
        if((**it).charge()!=0)
          PFE_scale = pfChargedCandidateEnergyScale_;
        else if((**it).pdgId()==22){
          PFE_scale = pfGammaCandidateEnergyScale_;
        }
        else if((**it).pdgId()==130){
          PFE_scale = pfNeutralCandidateEnergyScale_;
          if(doCompensatoryNeuPFScaling_){
            double map_value = ReadJetAsymmMap((**it).eta(), (**it).phi(), *Asymm_map_);
            map_value = map_value*assymDelta_jetpt/assymSum_allNeuChange;
            PFE_scale = 1 + map_value;
          }
          if(doPeripheralNeuPFScaling_){
            double map_value = ReadJetAsymmMap((**it).eta(), (**it).phi(), *Asymm_map_);
            map_value = 10*map_value*peripheralNeutralChange/assymSum_peripheralChange;
            PFE_scale = 1 + map_value;
          }
          if(doRatioNeuPFScaling_){
            double map_value = ReadJetAsymmMap((**it).eta(), (**it).phi(), *Asymm_map_);
            map_value = map_value*10;
            PFE_scale = 1 + map_value/JetNeutralEnergyFraction;
          }
          else if(doNaiveNeuPFScaling_){
            double map_value = ReadJetAsymmMap((**it).eta(), (**it).phi(), *Asymm_map_);
            map_value = map_value*10;
            PFE_scale = 1 + map_value;
          }
          if(pfNeutralSmear_){
            while(abs(Hcal_y_smear) > 0.087){
              Hcal_y_smear = rand_hcal_y_smear->Gaus(0, 0.087/2);
            }
            while(abs(Hcal_phi_smear) > 0.087){
              Hcal_phi_smear = rand_hcal_phi_smear->Gaus(0, 0.087/2);
            }
          }
        }
      }
      
      if(isMC_ && TrackVariation_ != 0. && doChargedConstOnly_){
        if(rand_track_sel->Uniform(0,1) < TrackVariation_) continue;
      }
      else if(isMC_ && TrackVariation_ != 0. && !doChargedConstOnly_ && (**it).charge()!=0 && rand_track_sel->Uniform(0,1) < TrackVariation_ ){
        double closest_to_particle = 0.087;
        fastjet::PseudoJet temp_part;
        temp_part.reset((**it).px(), (**it).py(), (**it).pz(), (**it).energy());
        Int_t  count_it2 = 0;
        Int_t selectedAcceptor = 0;
        for(auto it2 = daughters.begin(); it2!=daughters.end(); ++it2){
          fastjet::PseudoJet temp_part_acceptor;
          temp_part_acceptor.reset((**it2).px(), (**it2).py(), (**it2).pz(), (**it2).energy());
          Double_t dR_DonorAcceptor = temp_part_acceptor.delta_R(temp_part);
          if( dR_DonorAcceptor < closest_to_particle && count_it2!=count_it && (**it2).pdgId()!=22 ){
            selectedAcceptor = count_it2;
            closest_to_particle = dR_DonorAcceptor;
          }
          count_it2++;
        }
        if(closest_to_particle < 0.087){
          posDonor.push_back(count_it);
          posAcceptor.push_back(selectedAcceptor);
        }
        double charge_track_shift = rand_charge_smear->Gaus(0, (**it).energy()*0.1);
        charge_track_smear = ((**it).energy()-charge_track_shift)/(**it).energy();
      }
      
      mypart.reset((**it).px(), (**it).py(), (**it).pz(), (**it).energy());
      if(PFE_scale < 0.){
        PFE_scale = 0.01;
      }
      if( isMC_ ) mypart.reset((**it).px()*PFE_scale*charge_track_smear, (**it).py()*PFE_scale*charge_track_smear, (**it).pz()*PFE_scale*charge_track_smear, (**it).energy()*PFE_scale*charge_track_smear);
      if( isMC_ && pfNeutralSmear_ && (**it).pdgId()==130 ){
        mypart.reset_PtYPhiM(mypart.perp(), mypart.rap()+Hcal_y_smear, mypart.phi()+Hcal_phi_smear, mypart.m());
      }
      if(mypart.perp() < minConstituentPt_){
        continue;
      }

      particles.push_back(mypart);
      double frac_dR = mypart.delta_R(myjet)/rParam;
      double frac_pt = mypart.perp()/myjet.perp();
      intjet_multi++;
      jet_girth     += mypart.perp()*mypart.delta_R(myjet)/myjet.perp();
      jet_girth_new += frac_pt*frac_dR;
      jet_thrust    += frac_pt*frac_dR*frac_dR;
      jet_LHA       += frac_pt*sqrt(frac_dR);
      jet_pTD       += frac_pt*frac_pt;
      count_it++;
    }
    
    if(isMC_ && TrackVariation_ != 0. && !doChargedConstOnly_){
      for(size_t pos{0}; pos < posDonor.size(); ++pos){
        particles.at(posAcceptor.at(pos)) = particles.at(posAcceptor.at(pos)) + particles.at(posDonor.at(pos));
        particles.at(posDonor.at(pos)).reset(0., 0., 0., 0.);
      }
    }
    
    if(isMC_ and TrackVariation_){
      for(auto itp = particles.begin(); itp!=particles.end(); ++itp){
        if(itp->perp()==0 and itp!=particles.end()){
          particles.erase(itp);
          itp--;
        }
      }
    }
    
    if(particles.empty()){
      jets_.jtdyn_split[jets_.nref] = std::numeric_limits<int>::min();
      jets_.jtdyn_eta[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jtdyn_phi[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jtdyn_deltaR[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jtdyn_kt[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jtdyn_z[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_intjet_multi[jets_.nref] = std::numeric_limits<int>::min();
      jets_.jt_girth[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_girth_new[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_thrust[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_LHA[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_pTD[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_PLJPkT.push_back(jet_PLJPkT);
      jets_.jt_PLJPdR.push_back(jet_PLJPdR);
      jets_.jt_PLJPeta.push_back(jet_PLJPeta);
      jets_.jt_PLJPphi.push_back(jet_PLJPphi);
      throw(123);
    }

    fastjet::ClusterSequence csiter(particles, jet_def);
    std::vector<fastjet::PseudoJet> output_jets = csiter.inclusive_jets(0);
    output_jets = sorted_by_pt(output_jets);
    fastjet::PseudoJet jj = output_jets[0];
    fastjet::PseudoJet j1;
    fastjet::PseudoJet j2;
    fastjet::PseudoJet highest_splitting;
    
    if(!jj.has_parents(j1,j2)){
      jets_.jtdyn_split[jets_.nref] = std::numeric_limits<int>::min();
      jets_.jtdyn_eta[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jtdyn_phi[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jtdyn_deltaR[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jtdyn_kt[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jtdyn_z[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_intjet_multi[jets_.nref] = std::numeric_limits<int>::min();
      jets_.jt_girth[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_girth_new[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_thrust[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_LHA[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_pTD[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.jt_PLJPkT.push_back(jet_PLJPkT);
      jets_.jt_PLJPdR.push_back(jet_PLJPdR);
      jets_.jt_PLJPeta.push_back(jet_PLJPeta);
      jets_.jt_PLJPphi.push_back(jet_PLJPphi);
      throw(124);
    }
    
    while(jj.has_parents(j1,j2)){
      if(j1.perp() < j2.perp()) std::swap(j1,j2);
      double delta_R = j1.delta_R(j2);
      double k_t = j2.perp()*delta_R;
      if((doHardestSplitMatching_ && isMC_) or (doFullPLJPmatching_ && isMC_)){
        jets_.jtJetConstituent.push_back(j2);
      }
      
      z = j2.perp()/(j1.perp()+j2.perp());
      if(doPrimaryLJPReco_){
        jet_PLJPkT.push_back(k_t);
        jet_PLJPdR.push_back(delta_R);
        jet_PLJPeta.push_back(j2.eta());
        jet_PLJPphi.push_back(j2.phi());
      }
      if(k_t > dyn_kt){
        highest_splitting = j2;
        dyn_kt = k_t;
        dyn_split = nsplit;
        dyn_deltaR = delta_R;
        dyn_z = z;
        dyn_eta = j2.eta();
        dyn_phi = j2.phi();
      }
      jj = j1;
      nsplit = nsplit+1;
    }
    
    jets_.jtdyn_split[jets_.nref] = dyn_split;
    jets_.jtdyn_eta[jets_.nref] = dyn_eta;
    jets_.jtdyn_phi[jets_.nref] = dyn_phi;
    jets_.jtdyn_deltaR[jets_.nref] = dyn_deltaR;
    jets_.jtdyn_kt[jets_.nref] = dyn_kt;
    jets_.jtdyn_z[jets_.nref] = dyn_z;
    jets_.jt_intjet_multi[jets_.nref] = intjet_multi;
    jets_.jt_girth[jets_.nref] = jet_girth;
    jets_.jt_girth_new[jets_.nref] = jet_girth_new;
    jets_.jt_thrust[jets_.nref] = jet_thrust;
    jets_.jt_LHA[jets_.nref] = jet_LHA;
    jets_.jt_pTD[jets_.nref] = jet_pTD;
    jets_.jt_PLJPkT.push_back(jet_PLJPkT);
    jets_.jt_PLJPdR.push_back(jet_PLJPdR);
    jets_.jt_PLJPeta.push_back(jet_PLJPeta);
    jets_.jt_PLJPphi.push_back(jet_PLJPphi);
  } 
  catch (fastjet::Error) { /*return -1;*/ }
  catch (Int_t MyNum){
    if(MyNum == 123)
      std::cout << "Whoops, seems the number of charged jet constituents is 0! Setting all reco jet split variables to numeric min." << std::endl;
  }
}

void HiInclusiveJetAnalyzer::IterativeDeclusteringGen(double groom_type, double groom_combine, const reco::GenJet& jet)
{
  Int_t intjet_multi = 0;
  float jet_girth = 0;
  float jet_girth_new = 0;
  float jet_thrust = 0;
  float jet_LHA = 0;
  float jet_pTD = 0;
  std::vector<float> jet_PLJPkT = {};
  std::vector<float> jet_PLJPdR = {};
  std::vector<float> jet_PLJPeta = {};
  std::vector<float> jet_PLJPphi = {};
  double nsplit = 0;
  double dyn_kt = std::numeric_limits<double>::min();
  double dyn_eta = 0;
  double dyn_phi = 0;

  Int_t dyn_split = 0;
  double dyn_deltaR = 0;
  double z = 0;
  double dyn_z = 0;
  double jet_radius_ca = 1.0;
  fastjet::JetDefinition jet_def(fastjet::genkt_algorithm,jet_radius_ca,0,static_cast<fastjet::RecombinationScheme>(0), fastjet::Best);
  fastjet::PseudoJet myjet;
  fastjet::PseudoJet mypart;
  myjet.reset(jet.p4().px(),jet.p4().py(),jet.p4().pz(),jet.p4().e());  
  
  try{
    std::vector<fastjet::PseudoJet> particles = {};                         
    auto daughters = jet.getJetConstituents();
    for(auto it = daughters.begin(); it != daughters.end(); ++it){
      if( doChargedConstOnly_ && (**it).charge() == 0 ) continue;
      if((**it).pt() < minConstituentPt_){
        continue;
      }
      particles.push_back(fastjet::PseudoJet((**it).px(), (**it).py(), (**it).pz(), (**it).energy()));
      mypart.reset((**it).px(), (**it).py(), (**it).pz(), (**it).energy());
      double frac_dR = mypart.delta_R(myjet)/rParam;
      double frac_pt = mypart.perp()/myjet.perp();
      intjet_multi++;
      jet_girth     += mypart.perp()*mypart.delta_R(myjet)/myjet.perp();
      jet_girth_new += frac_pt*frac_dR;
      jet_thrust    += frac_pt*frac_dR*frac_dR;
      jet_LHA       += frac_pt*sqrt(frac_dR);
      jet_pTD       += frac_pt*frac_pt;
    }
    
    if(particles.empty()){
      jets_.refdyn_split[jets_.nref] = std::numeric_limits<int>::min();
      jets_.refdyn_eta[jets_.nref] = -std::numeric_limits<double>::max();
      jets_.refdyn_phi[jets_.nref] = -std::numeric_limits<double>::max();
      jets_.refdyn_deltaR[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.refdyn_kt[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.refdyn_z[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_intjet_multi[jets_.nref] = std::numeric_limits<int>::min();
      jets_.ref_girth[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_girth_new[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_thrust[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_LHA[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_pTD[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_PLJPkT.push_back(jet_PLJPkT);
      jets_.ref_PLJPdR.push_back(jet_PLJPdR);
      jets_.ref_PLJPeta.push_back(jet_PLJPeta);
      jets_.ref_PLJPphi.push_back(jet_PLJPphi);
      throw(123);
    }
    
    fastjet::ClusterSequence csiter(particles, jet_def);
    std::vector<fastjet::PseudoJet> output_jets = csiter.inclusive_jets(0);
    output_jets = sorted_by_pt(output_jets);

    fastjet::PseudoJet jj = output_jets[0];
    fastjet::PseudoJet j1;
    fastjet::PseudoJet j2;
    fastjet::PseudoJet highest_splitting;
    
    if(!jj.has_parents(j1,j2)){
      jets_.refdyn_split[jets_.nref] = std::numeric_limits<int>::min();
      jets_.refdyn_eta[jets_.nref] = -std::numeric_limits<double>::max();
      jets_.refdyn_phi[jets_.nref] = -std::numeric_limits<double>::max();
      jets_.refdyn_deltaR[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.refdyn_kt[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.refdyn_z[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_intjet_multi[jets_.nref] = std::numeric_limits<int>::min();
      jets_.ref_girth[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_girth_new[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_thrust[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_LHA[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_pTD[jets_.nref] = - std::numeric_limits<double>::max();
      jets_.ref_PLJPkT.push_back(jet_PLJPkT);
      jets_.ref_PLJPdR.push_back(jet_PLJPdR);
      jets_.ref_PLJPeta.push_back(jet_PLJPeta);
      jets_.ref_PLJPphi.push_back(jet_PLJPphi);
      throw(124);
    }
    
    while(jj.has_parents(j1,j2)){
      if(j1.perp() < j2.perp()) std::swap(j1,j2);
      double delta_R = j1.delta_R(j2);
      if((doHardestSplitMatching_ && isMC_) or (doFullPLJPmatching_ && isMC_)) jets_.refJetConstituent.push_back(j2);
      double k_t = j2.perp()*delta_R;
      z = j2.perp()/(j1.perp()+j2.perp());
      if(doPrimaryLJPTruth_){
        jet_PLJPkT.push_back(k_t);
        jet_PLJPdR.push_back(delta_R);
        jet_PLJPeta.push_back(j2.eta());
        jet_PLJPphi.push_back(j2.phi());
      }
      
      if(k_t > dyn_kt){
        highest_splitting = j2;
        dyn_kt = k_t;
        dyn_split = nsplit;
        dyn_deltaR = delta_R;
        dyn_z = z;
        dyn_eta = j2.eta();
        dyn_phi = j2.phi();
      }
      jj = j1;
      nsplit = nsplit+1;
    }
    
    jets_.refdyn_split[jets_.nref] = dyn_split;
    jets_.refdyn_eta[jets_.nref] = dyn_eta;
    jets_.refdyn_phi[jets_.nref] = dyn_phi;
    jets_.refdyn_deltaR[jets_.nref] = dyn_deltaR;
    jets_.refdyn_kt[jets_.nref] = dyn_kt;
    jets_.refdyn_z[jets_.nref] = dyn_z;
    jets_.ref_intjet_multi[jets_.nref] = intjet_multi;
    jets_.ref_girth[jets_.nref] = jet_girth;
    jets_.ref_girth_new[jets_.nref] = jet_girth_new;
    if(isinf(jet_girth_new)) std::cout << "Infinite girth!" << std::endl;
    jets_.ref_thrust[jets_.nref] = jet_thrust;
    jets_.ref_LHA[jets_.nref] = jet_LHA;
    jets_.ref_pTD[jets_.nref] = jet_pTD;
    jets_.ref_PLJPkT.push_back(jet_PLJPkT);
    jets_.ref_PLJPdR.push_back(jet_PLJPdR);
    jets_.ref_PLJPeta.push_back(jet_PLJPeta);
    jets_.ref_PLJPphi.push_back(jet_PLJPphi);
  } 
  catch (fastjet::Error) { /*return -1;*/ }
  catch (Int_t MyNum){
    if(MyNum == 123)
      std::cout << "Whoops, seems the number of charged jet constituents is 0! Setting all gen jet split variables to numeric min." << std::endl;
    if(MyNum == 124)
      std::cout << "Jet does not have any parents, out of the loop!" << std::endl;
  }
}

void HiInclusiveJetAnalyzer::RecoTruthSplitMatching(std::vector<fastjet::PseudoJet> &constituents_level1, fastjet::PseudoJet &hardest_level2, bool *bool_array, int *hardest_level1_split){
  float min_dR = std::numeric_limits<float>::max();
  size_t closest_level1 = 0;
  for(size_t i{0};i<constituents_level1.size();++i){
    float dR = constituents_level1.at(i).delta_R(hardest_level2);
    if(min_dR > dR){
      closest_level1 = i;
      min_dR = dR;
    }
  }
  if(static_cast<int>(closest_level1) == hardest_level1_split[jets_.nref] ){
    bool_array[jets_.nref] = true;
  }
  else{
    bool_array[jets_.nref] = false;
  }
}

void HiInclusiveJetAnalyzer::TruthRecoRecoTruthMatching(){
  if( jets_.jtdyn_split[jets_.nref] == std::numeric_limits<int>::min() || jets_.refdyn_split[jets_.nref] == std::numeric_limits<int>::min() || jets_.jtJetConstituent.size() == 0 || jets_.refJetConstituent.size() == 0 ){
    jets_.refdyn_isClosestToReco[jets_.nref] = false;
    jets_.jtdyn_isClosestToTruth[jets_.nref] = false;
    jets_.jtdyn_refdyn_dR[jets_.nref] = std::numeric_limits<float>::max();
    return;
  }
  fastjet::PseudoJet hardest_R_split = jets_.jtJetConstituent.at(jets_.jtdyn_split[jets_.nref]);
  fastjet::PseudoJet hardest_T_split = jets_.refJetConstituent.at(jets_.refdyn_split[jets_.nref]);
  jets_.jtdyn_refdyn_dR[jets_.nref] = hardest_R_split.delta_R(hardest_T_split);
  RecoTruthSplitMatching(jets_.refJetConstituent, hardest_R_split, jets_.refdyn_isClosestToReco, jets_.refdyn_split);
  RecoTruthSplitMatching(jets_.jtJetConstituent,  hardest_T_split, jets_.jtdyn_isClosestToTruth, jets_.jtdyn_split);
}

void HiInclusiveJetAnalyzer::matchPLJP(std::vector<float> &match_dR, std::vector<Int_t> &match_idx, std::vector<fastjet::PseudoJet> &level1, std::vector<fastjet::PseudoJet> &level2){
  for( Int_t i{0}; i < (Int_t)level1.size(); ++i ){
    Double_t min_distance = std::numeric_limits<double>::max();
    Int_t paired_em = -5;
    for( Int_t j{0}; j < (Int_t)level2.size(); ++j ){
      Double_t dist = level1.at(i).delta_R(level2.at(j));
      if( dist < min_distance ){
        min_distance = dist;
        paired_em = j;
      }
    }
  match_idx.push_back(paired_em);
  match_dR.push_back(min_distance);
  }
}

float HiInclusiveJetAnalyzer::ReadJetAsymmMap(float eta, float phi, TH2F Asymm_map){
  float result =  Asymm_map.GetBinContent(Asymm_map.GetXaxis()->FindBin(eta),Asymm_map.GetYaxis()->FindBin(phi));
  float high_bound = 0.15;
  float low_bound = -0.15;
  if( result < low_bound ){
    result = low_bound;
  }
  if( result > high_bound ){
    result = high_bound;
  }
  return result;
}

std::vector<float> HiInclusiveJetAnalyzer::BinBoundsAsymmMap(float eta, float phi, TH2F Asymm_map){
  std::vector<float> result;
  float eta_low =  Asymm_map.GetXaxis()->GetBinLowEdge(Asymm_map.GetXaxis()->FindBin(eta));
  float eta_high =  Asymm_map.GetXaxis()->GetBinLowEdge(Asymm_map.GetXaxis()->FindBin(eta)+1);
  float phi_low = Asymm_map.GetYaxis()->GetBinLowEdge(Asymm_map.GetYaxis()->FindBin(phi));
  float phi_high = Asymm_map.GetYaxis()->GetBinLowEdge(Asymm_map.GetYaxis()->FindBin(phi)+1);
  return result = {eta_low, eta_high, phi_low, phi_high};
}

int HiInclusiveJetAnalyzer::getPFJetMuon(const pat::Jet& pfJet, const reco::PFCandidateCollection *pfCandidateColl)
{
  int pfMuonIndex = -1;
  float ptMax = 0.;
  for(unsigned icand=0;icand<pfCandidateColl->size(); icand++) {
    const reco::PFCandidate& pfCandidate = pfCandidateColl->at(icand);
    int id = pfCandidate.particleId();
    if(abs(id) != 3) continue;
    if(reco::deltaR(pfJet,pfCandidate)>0.5) continue;
    double pt =  pfCandidate.pt();
    if(pt>ptMax){
      ptMax = pt;
      pfMuonIndex = (int) icand;
    }
  }
  return pfMuonIndex;
}

void HiInclusiveJetAnalyzer::LookThroughJetSplits(fastjet::PseudoJet jj, int i=1){
  fastjet::PseudoJet j1;
  fastjet::PseudoJet j2;
  if(jj.has_parents(j1,j2)){
    LookThroughJetSplits(j2, 2);
    LookThroughJetSplits(j1, 1);
  }
}

double HiInclusiveJetAnalyzer::getPtRel(const reco::PFCandidate& lep, const pat::Jet& jet )
{
  float lj_x = jet.p4().px();
  float lj_y = jet.p4().py();
  float lj_z = jet.p4().pz();
  float lj2  = lj_x*lj_x+lj_y*lj_y+lj_z*lj_z;
  float lep2 = lep.px()*lep.px()+lep.py()*lep.py()+lep.pz()*lep.pz();
  float lepXlj = lep.px()*lj_x+lep.py()*lj_y+lep.pz()*lj_z;
  float pLrel2 = lepXlj*lepXlj/lj2;
  float pTrel2 = lep2-pLrel2;
  return (pTrel2 > 0) ? std::sqrt(pTrel2) : 0.0;
}

int HiInclusiveJetAnalyzer::getGroomedGenJetIndex(const reco::GenJet& jet) const {
  double drMin = 100;
  int imatch = -1;
  for(unsigned int i = 0 ; i < gensubjets_->size(); ++i) {
    const reco::Jet& mjet = (*gensubjets_)[i];
    double dr = deltaR(jet,mjet);
    if(dr < drMin){
      imatch = i;
      drMin = dr;
    }
  }
  return imatch;
}

void HiInclusiveJetAnalyzer::analyzeRefSubjets(const reco::GenJet& jet){
  int imatch = getGroomedGenJetIndex(jet);
}

void HiInclusiveJetAnalyzer::analyzeGenSubjets(const reco::GenJet& jet){
  int imatch = getGroomedGenJetIndex(jet);
  double dr = 999.;
}

void HiInclusiveJetAnalyzer::incrementJetID(const reco::Candidate& it){
  if(it.charge()!=0){
    TrackRef trk = it.get<TrackRef>();
    if(trk.isNonnull()){
      double ptcand = trk->pt();
      jets_.trackSum[jets_.nref] += ptcand;
      jets_.trackN[jets_.nref] += 1;
      if (ptcand > hardPtMin_) {
        jets_.trackHardSum[jets_.nref] += ptcand;
        jets_.trackHardN[jets_.nref] += 1;
      }
      if (ptcand > jets_.trackMax[jets_.nref])
        jets_.trackMax[jets_.nref] = ptcand;
    }
  }
  Double_t ecand = it.energy();
  Int_t abspdgId = abs(it.pdgId());
  
  if( abspdgId == 22 ){
    jets_.photonSum[jets_.nref] += ecand;
    jets_.photonN[jets_.nref] += 1;
    if (ecand > hardPtMin_) {
      jets_.photonHardSum[jets_.nref] += ecand;
      jets_.photonHardN[jets_.nref] += 1;
    }
    if (ecand > jets_.photonMax[jets_.nref])
      jets_.photonMax[jets_.nref] = ecand;
  }
  else if( abspdgId == 130 ){
    jets_.neutralSum[jets_.nref] += ecand;
    jets_.neutralN[jets_.nref] += 1;
    if (ecand > jets_.neutralMax[jets_.nref])
      jets_.neutralMax[jets_.nref] = ecand;
  }
  else if( abspdgId == 211 ){
    jets_.chargedSum[jets_.nref] += ecand;
    jets_.chargedN[jets_.nref] += 1;
    if (ecand > hardPtMin_) {
      jets_.chargedHardSum[jets_.nref] += ecand;
      jets_.chargedHardN[jets_.nref] += 1;
    }
    if (ecand > jets_.chargedMax[jets_.nref])
      jets_.chargedMax[jets_.nref] = ecand;
  }
  else if( abspdgId == 11 ){
    jets_.eSum[jets_.nref] += ecand;
    jets_.eN[jets_.nref] += 1;
    if (ecand > jets_.eMax[jets_.nref])
      jets_.eMax[jets_.nref] = ecand;
  }
  else if( abspdgId == 13 ){
    jets_.muSum[jets_.nref] += ecand;
    jets_.muN[jets_.nref] += 1;
    if (ecand > jets_.muMax[jets_.nref])
      jets_.muMax[jets_.nref] = ecand;
  }
  else if( abspdgId == 1 ){
    jets_.h_HFSum[jets_.nref] += ecand;
    jets_.h_HFN[jets_.nref] += 1;
    if (ecand > jets_.h_HFMax[jets_.nref])
      jets_.h_HFMax[jets_.nref] = ecand;
  }
  else if( abspdgId == 2 ){
    jets_.eg_HFSum[jets_.nref] += ecand;
    jets_.eg_HFN[jets_.nref] += 1;
    if (ecand > jets_.eg_HFMax[jets_.nref])
      jets_.eg_HFMax[jets_.nref] = ecand;
  }
  else{
    std::cout << " Unknown particle! something else??? ID: " << abspdgId << std::endl;
  }
}

DEFINE_FWK_MODULE(HiInclusiveJetAnalyzer);
