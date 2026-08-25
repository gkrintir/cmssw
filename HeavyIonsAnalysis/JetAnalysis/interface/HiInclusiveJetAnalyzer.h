#ifndef MNguyen_HiInclusiveJetAnalyzer_inclusiveJetAnalyzer_
#define MNguyen_HiInclusiveJetAnalyzer_inclusiveJetAnalyzer_

// system include files
#include <memory>
#include <string>
#include <iostream>

// ROOT headers
#include "TH2.h"
#include "TTree.h"

// user include files
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "fastjet/contrib/Njettiness.hh"
#include "DataFormats/JetMatching/interface/JetFlavourInfo.h"
#include "DataFormats/JetMatching/interface/JetFlavourInfoMatching.h"
//

/**\class HiInclusiveJetAnalyzer

   \author Matt Nguyen
   \date   November 2010
*/

class HiInclusiveJetAnalyzer : public edm::one::EDAnalyzer<edm::one::WatchRuns> {
public:
  explicit HiInclusiveJetAnalyzer(const edm::ParameterSet&);

  ~HiInclusiveJetAnalyzer() override;

  void analyze(const edm::Event&, const edm::EventSetup&) override;

  void beginRun(const edm::Run& run, const edm::EventSetup& es) override;
  void endRun(const edm::Run& run, const edm::EventSetup& es) override;

  void beginJob() override;

private:
  // for reWTA reclustering-----------------------
  bool doWTARecluster_ = false;
  fastjet::JetDefinition WTAjtDef =
      fastjet::JetDefinition(fastjet::JetAlgorithm::antikt_algorithm, 2, fastjet::WTA_pt_scheme);
  //--------------------------------------------

  //int getPFJetMuon(const pat::Jet& pfJet, const reco::PFCandidateCollection *pfCandidateColl);
  // int getPFJetMuon(const pat::Jet& pfJet, const edm::View<pat::PackedCandidate>* pfCandidateColl);

  //double getPtRel(const reco::PFCandidate& lep, const pat::Jet& jet );
  // double getPtRel(const pat::PackedCandidate& lep, const pat::Jet& jet);

  // void analyzeSubjets(const reco::Jet& jet);
  // int getGroomedGenJetIndex(const reco::GenJet& jet) const;
  // void analyzeRefSubjets(const reco::GenJet& jet);
  // void analyzeGenSubjets(const reco::GenJet& jet);

  void RandomConePtSum(float &cone_eta, float &cone_phi, float &cone_pt, edm::Handle<std::vector<reco::PFCandidate> > &pfCandidateColl);

  void IterativeDeclusteringRec(double groom_type, double groom_combine, const reco::Jet& jet);
  void IterativeDeclusteringGen(double groom_type, double groom_combine, const reco::GenJet& jet);
  float ReadJetAsymmMap(float eta, float phi, TH2F Asymm_map);
  std::vector<float> BinBoundsAsymmMap(float eta, float phi, TH2F Asymm_map);
  void RecoTruthSplitMatching(std::vector<fastjet::PseudoJet> &constituents_level1, fastjet::PseudoJet &hardest_level2, bool *bool_array, int *hardest_level1_split);
  void TruthRecoRecoTruthMatching();
  void matchPLJP(std::vector<float> &match_dR, std::vector<Int_t> &match_idx, std::vector<fastjet::PseudoJet> &level1, std::vector<fastjet::PseudoJet> &level2);
  int getPFJetMuon(const pat::Jet& pfJet, const reco::PFCandidateCollection *pfCandidateColl);
  void LookThroughJetSplits(fastjet::PseudoJet jj, int i);
  double getPtRel(const reco::PFCandidate& lep, const pat::Jet& jet );

    // --- NEW: B-Tagging Maps ---
    // Stores the configuration for which taggers to run
    std::map<std::string, std::map<std::string, edm::EDGetTokenT<reco::JetTagCollection>>> jetTaggers_;
    // Stores the actual discriminator values to be saved in the tree
    std::map<std::string, std::map<std::string, std::vector<float>>> jets_discr_;

    // --- NEW: Helper Functions ---
    std::pair<float, float> calculateWTAAxis(const reco::Jet& jet);
    float getBTagValue(const edm::Handle<reco::JetTagCollection> &bTags, const pat::Jet &jet);
    void fillBtagging(const pat::Jet& jet, int jIndex, const std::map<std::string, std::map<std::string, edm::Handle<reco::JetTagCollection>>>& jetTaggers);
  
  void saveDaughters( const reco::GenParticle & gen);
  void saveDaughters( const reco::Candidate & gen);
  int  getGroomedGenJetIndex(const reco::GenJet& jet) const;
  void analyzeRefSubjets(const reco::GenJet& jet);
  void analyzeGenSubjets(const reco::GenJet& jet);
  void incrementJetID(const reco::Candidate& it);

  int TaggedJet(pat::Jet patjet, edm::Handle<reco::JetTagCollection > jetTags );

  edm::InputTag   jetTagLabel_;
  edm::EDGetTokenT<std::vector<reco::Vertex> >       vtxTag_;
  edm::EDGetTokenT<pat::JetCollection>               jetTag_;
  edm::EDGetTokenT<pat::JetCollection>               matchTag_;
  edm::EDGetTokenT<pat::PackedCandidateCollection> pfCandidateToken_;
  // edm::EDGetTokenT<reco::PFCandidateCollection>      pfCandidateLabel_;
  edm::EDGetTokenT<reco::TrackCollection>            trackTag_;
  edm::EDGetTokenT<reco::GenParticleCollection>      genParticleSrc_;
  edm::EDGetTokenT<edm::View<reco::GenJet>>          genjetTag_;
  edm::EDGetTokenT<edm::HepMCProduct>                eventInfoTag_;
  edm::EDGetTokenT<GenEventInfoProduct>              eventGenInfoTag_;
  
  std::string                              jetName_; //used as prefix for jet structures
  edm::Handle<reco::JetView>               gensubjets_;

  edm::EDGetTokenT< edm::ValueMap<float> > tokenGenSym_;
  edm::Handle<edm::ValueMap<float> >       genSymVM_;
  edm::EDGetTokenT< edm::ValueMap<int> >   tokenGenDroppedBranches_;
  edm::Handle<edm::ValueMap<int> >         genDroppedBranchesVM_;
  
  // towers
  edm::EDGetTokenT<CaloTowerCollection> TowerSrc_;

  std::vector<float> usedStringPts;

  TH2F *Asymm_map_;

  /// verbose ?
  bool verbose_;
  bool doMatch_;
  bool useVtx_;
  bool useRawPt_;
  bool doTower;
  bool isMC_;
  bool useHepMC_;
  bool fillGenJets_;
  bool useQuality_;
  std::string trackQuality_;
  bool doBtagging_;

  bool doPrimaryLJPReco_;
  bool doPrimaryLJPTruth_;

  double minConstituentPt_;
  bool doChargedConstOnly_;
  bool doHardestSplitMatching_;
  bool dopthatcut;
  double genPtMin_;
  bool doLifeTimeTagging_;
  bool doLifeTimeCandidateTagging_;
  bool doLifeTimeTaggingExtras_;
  bool saveBfragments_;
  bool doExtraCTagging_;

  bool doHiJetID_;
  bool doStandardJetID_;

  double rParam;
  double hardPtMin_;
  double jetPtMin_;
  double mysdcut1;
  double mysdcut2;
  double mydynktcut;
  double groom_type;
  double groom_combine;
  double jetAbsEtaMax_;
  bool doGenTaus_;
  bool doGenSym_;
  bool doSubJets_;
  bool doJetConstituents_;


  //Systematics variables
  bool doNaiveNeuPFScaling_;
  bool doRatioNeuPFScaling_;
  bool doPeripheralNeuPFScaling_;
  bool doCompensatoryNeuPFScaling_;
  double pfChargedCandidateEnergyScale_;
  double pfGammaCandidateEnergyScale_;
  double pfNeutralCandidateEnergyScale_;
  double TrackVariation_;
  bool pfNeutralSmear_;
  bool doFullPLJPmatching_;


  TTree *t;
  edm::Service<TFileService> fs1;

  std::string bTagJetName_;
  std::string ipTagInfos_;
  std::string svTagInfos_;
  std::string trackCHEBJetTags_;
  std::string trackCHPBJetTags_;
  std::string jetPBJetTags_;
  std::string jetBPBJetTags_;
  std::string simpleSVHighEffBJetTags_;
  std::string simpleSVHighPurBJetTags_;
  std::string combinedSVV1BJetTags_;
  std::string combinedSVV2BJetTags_;
  std::string deepCSVBJetTags_;
  
  static const int MAXJETS = 1000;
  static const int MAXTRACKS = 5000;
  static const int MAXBFRAG = 500;

  struct JRA{

    int nref;
    int run;
    int evt;
    int lumi;
    float vx, vy, vz;

    float jtMapPt[MAXJETS] = {0};
    float rawpt[MAXJETS] = {0};
    float jtrawE[MAXJETS] = {0};
    float jtpt[MAXJETS] = {0};
    float jteta[MAXJETS] = {0};
    float jtphi[MAXJETS] = {0};

    float WTAeta[MAXJETS] = {0};
    float WTAphi[MAXJETS] = {0};
    float refWTAeta[MAXJETS] = {0};
    float refWTAphi[MAXJETS] = {0};
    
    float jtdyn_var[MAXJETS] = {0};
    int jtdyn_split[MAXJETS] = {0};
    float jtdyn_deltaR[MAXJETS] = {0};
    float jtdyn_kt[MAXJETS] = {0};
    float jtdyn_eta[MAXJETS] = {0};
    float jtdyn_phi[MAXJETS] = {0};
    float jtdyn_z[MAXJETS] = {0};
    int jt_intjet_multi[MAXJETS] = {0};
    float jt_girth[MAXJETS] = {0};
    float jt_girth_new[MAXJETS] = {0};
    float jt_thrust[MAXJETS] = {0};
    float jt_LHA[MAXJETS] = {0};
    float jt_pTD[MAXJETS] = {0};
    std::vector<std::vector<float>> jt_PLJPkT = {};
    std::vector<std::vector<float>> jt_PLJPdR = {};
    std::vector<std::vector<float>> jt_PLJPeta = {};
    std::vector<std::vector<float>> jt_PLJPphi = {};

    std::vector<std::vector<float>> PLJP_TtoRmatch_dR = {}, PLJP_RtoTmatch_dR = {};
    std::vector<std::vector<Int_t>> PLJP_TtoRmatch_idx = {}, PLJP_RtoTmatch_idx = {};

    std::vector<fastjet::PseudoJet> jtJetConstituent = {};
    std::vector<fastjet::PseudoJet> refJetConstituent = {};

    bool jtdyn_isClosestToTruth[MAXJETS] = {0};
    bool refdyn_isClosestToReco[MAXJETS] = {0};
    float jtdyn_refdyn_dR[MAXJETS] = {0};

    float trackMax[MAXJETS] = {0};
    float trackSum[MAXJETS] = {0};
    int trackN[MAXJETS] = {0};

    float chargedMax[MAXJETS] = {0};
    float chargedSum[MAXJETS] = {0};
    int chargedN[MAXJETS] = {0};

    float h_HFMax[MAXJETS] = {0};
    float h_HFSum[MAXJETS] = {0};
    int h_HFN[MAXJETS] = {0};

    float eg_HFMax[MAXJETS] = {0};
    float eg_HFSum[MAXJETS] = {0};
    int eg_HFN[MAXJETS] = {0};

    float photonMax[MAXJETS] = {0};
    float photonSum[MAXJETS] = {0};
    int photonN[MAXJETS] = {0};

    float trackHardSum[MAXJETS] = {0};
    float chargedHardSum[MAXJETS] = {0};
    float photonHardSum[MAXJETS] = {0};

    int trackHardN[MAXJETS] = {0};
    int chargedHardN[MAXJETS] = {0};
    int photonHardN[MAXJETS] = {0};

    float neutralMax[MAXJETS] = {0};
    float neutralSum[MAXJETS] = {0};
    int neutralN[MAXJETS] = {0};

    float eMax[MAXJETS] = {0};
    float eSum[MAXJETS] = {0};
    int eN[MAXJETS] = {0};

    float muMax[MAXJETS] = {0};
    float muSum[MAXJETS] = {0};
    int muN[MAXJETS] = {0};

    float genChargedSum[MAXJETS] = {0};
    float genHardSum[MAXJETS] = {0};
    float signalChargedSum[MAXJETS] = {0};
    float signalHardSum[MAXJETS] = {0};
    // Update by Raghav, modified to take it from the towers
    float hcalSum[MAXJETS] = {0};
    float ecalSum[MAXJETS] = {0};

    float fHPD[MAXJETS] = {0};
    float fRBX[MAXJETS] = {0};
    int n90[MAXJETS] = {0};
    float fSubDet1[MAXJETS] = {0};
    float fSubDet2[MAXJETS] = {0};
    float fSubDet3[MAXJETS] = {0};
    float fSubDet4[MAXJETS] = {0};
    float restrictedEMF[MAXJETS] = {0};
    int nHCAL[MAXJETS] = {0};
    int nECAL[MAXJETS] = {0};
    float apprHPD[MAXJETS] = {0};
    float apprRBX[MAXJETS] = {0};

    //    int n90[MAXJETS] = {0};
    int n2RPC[MAXJETS] = {0};
    int n3RPC[MAXJETS] = {0};
    int nRPC[MAXJETS] = {0};

    float fEB[MAXJETS] = {0};
    float fEE[MAXJETS] = {0};
    float fHB[MAXJETS] = {0};
    float fHE[MAXJETS] = {0};
    float fHO[MAXJETS] = {0};
    float fLong[MAXJETS] = {0};
    float fShort[MAXJETS] = {0};
    float fLS[MAXJETS] = {0};
    float fHFOOT[MAXJETS] = {0};

    float refpt[MAXJETS] = {0};
    float refeta[MAXJETS] = {0};
    float refphi[MAXJETS] = {0};
    float refm[MAXJETS] = {0};
    float refarea[MAXJETS] = {0};
    float refy[MAXJETS] = {0};
    float reftau1[MAXJETS] = {0};
    float reftau2[MAXJETS] = {0};
    float reftau3[MAXJETS] = {0};
    float refsym[MAXJETS] = {0};
    // float refrg[MAXJETS] = {0};
    // float refdyn_pt1[MAXJETS] = {0};
    // float refangu[MAXJETS] = {0};
    
    float refdyn_var[MAXJETS] = {0};
    int refdyn_split[MAXJETS] = {0};
    // float refdyn_theta[MAXJETS] = {0};
    float refdyn_deltaR[MAXJETS] = {0};
    float refdyn_kt[MAXJETS] = {0};
    float refdyn_eta[MAXJETS] = {0};
    float refdyn_phi[MAXJETS] = {0};
    float refdyn_z[MAXJETS] = {0};
    int ref_intjet_multi[MAXJETS] = {0};
    float ref_girth[MAXJETS] = {0};
    float ref_girth_new[MAXJETS] = {0};
    float ref_thrust[MAXJETS] = {0};
    float ref_LHA[MAXJETS] = {0};
    float ref_pTD[MAXJETS] = {0};
    std::vector<std::vector<float>> ref_PLJPkT = {};
    std::vector<std::vector<float>> ref_PLJPdR = {};
    std::vector<std::vector<float>> ref_PLJPeta = {};
    std::vector<std::vector<float>> ref_PLJPphi = {};

    float refparton_pt[MAXJETS] = {0};
    int refparton_flavor[MAXJETS] = {0};
    int refparton_flavorForB[MAXJETS] = {0};

    float pthat;
    int beamId1, beamId2;

    float gensym[MAXJETS] = {0};
    int   gendroppedBranches[MAXJETS] = {0};

  };

  JRA jets_;

};

#endif
