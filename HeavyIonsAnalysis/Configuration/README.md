# Run 3 HiForest configurations and CRAB submission

These changes target the `OO_CMSSW_15_0_11` branch of
[gkrintir/cmssw](https://github.com/gkrintir/cmssw), using CMSSW 15.0.11.
The local branch is named `gkrintir/OO_CMSSW_15_0_11`.

## Changes included

### Jet analyzer

The header, source, and Python configuration were updated together using
the [CmsHI forest_CMSSW_15_1_X analyzer](https://github.com/CmsHI/cmssw/tree/forest_CMSSW_15_1_X/HeavyIonsAnalysis/JetAnalysis)
as a reference:

- `../JetAnalysis/interface/HiInclusiveJetAnalyzer.h`
- `../JetAnalysis/src/HiInclusiveJetAnalyzer.cc`
- `../JetAnalysis/python/inclusiveJetAnalyzer_cff.py`

The update replaces the earlier custom LJP/declustering and PF systematic
controls with the newer analyzer implementation. It aligns header buffers
and function signatures with the source, adds the required `caloJetTag`
and untracked `pfCandidateLabel` parameters, and supports configurable
JP, DeepCSV, DeepFlavour, ParticleTransformer, and unified
ParticleTransformer (UParT) discriminator maps. The current OO jobs select
JP and UParT. The `BuildFile.xml` dependencies are unchanged.

| Base analyzer parameter | Previous default | Current default |
| --- | --- | --- |
| `jetPtMin` | 20 | 5 |
| `rParam` | 0.2 | 0.4 |
| `useRawPt` | True | False |
| `doHiJetID` | True | False |
| `doBtagging` | False | True |

The OO forest configurations override the threshold to 15 GeV, enable HI
jet ID, WTA and b tagging, and select R=0.4 and R=0.8.

A variable must be declared, filled, and attached to a ROOT branch to be
saved; changing the header alone is insufficient. Current limitations:

- `refparton_pt` and `refparton_flavor` remain `-999`.
- `genChargedSum`, `genHardSum`, `signalChargedSum`, and
  `signalHardSum` remain zero because their filling code is commented.
- Constituent, subjet, and generator tau output remains disabled in the
  current OO configuration.
- UParT tau probabilities are summed into `probtau`; individual tau decay
  probabilities are not written separately.
- `jty`, `refy`, and `geny` currently store `eta()`, rather than rapidity.

### Forest configurations

| File | Changes or purpose |
| --- | --- |
| `forest_miniAOD_run3_DATA.py` | Enable `hltanalysis`; replace the R=0.2/0.4/0.6/0.8 jet selection with R=0.4/0.8. |
| `forest_miniAOD_run3_MC.py` | Enable `hltanalysis` and `HiGenParticleAna`; select R=0.4/0.8 jets; replace the R=0.2 random cone analyzer with R=0.8 alongside R=0.4; change the local OO Pythia input; reduce the local event limit from 2000 to 500. |
| `forest_miniAOD_run3_ppref_DATA.py` | Include the existing local pp reference DATA configuration: `Run3_2024_ppRef` era, `141X_dataRun3_Prompt_v3` GlobalTag, local event limit -1. |
| `forest_miniAOD_run3_ppref_MC.py` | Include the existing local pp reference MC configuration: `Run3_2024_ppRef` era, `141X_mcRun3_2024_realistic_ppRef5TeV_v7` GlobalTag, local event limit 1000. |

The existing pp reference calibration/GlobalTag TODOs remain unresolved.
The OO MC file for local testing is from the v7 production; the default
CRAB OO MC dataset is CustomTrack v9. CRAB uses its configured dataset,
rather than the local test filename in the forest configuration.

### Submission names and behavior

Python `crab_*.py` files configure a single dataset. Bash
`submit_multidataset_*.sh` files submit one DATA task per dataset.

| Previous name | New name |
| --- | --- |
| `submit_multidataset_OO_DATA.py` | `crab_OO_DATA.py` |
| `submit_OO_MC.py` | `crab_OO_MC.py` |
| `submit_multidataset_pp2024_DATA.py` | `crab_ppref_DATA.py` |
| `submit_pp_MC_2024.py` | `crab_ppref_MC.py` |
| `submit_all_OO_DATA.sh` | `submit_multidataset_OO_DATA.sh` |
| `submit_ppref_multidataset.sh` | `submit_multidataset_ppref_DATA.sh` |
| `OO_datasets.txt` | `datasets_OO_DATA.txt` |
| `ppRef_datasets.txt` | `datasets_ppref_DATA.txt` |

The refactor also:

- Aligns `General.requestName` and `Data.outputDatasetTag` across templates
  and batch submissions.
- Uses the same `General.workArea` for submission and existing-task checks;
  previously the wrappers checked a different directory from CRAB.
- Replaces user-specific AFS mask/list paths with local paths, and makes
  wrappers resolve their own configuration directory.
- Standardizes output directories, correcting the missing slash in the
  former pp reference DATA output path.
- Adds `--dry-run`, `--help`, an optional dataset list, duplicate detection,
  and submission summaries. Invalid entries and failed submissions are
  counted without stopping the remaining datasets; any failure returns a
  nonzero final status.
- Ignores local CRAB project directories, submission logs, and Python
  caches through `.gitignore`. ROOT files are already ignored globally.

Existing CRAB tasks retain their old names and directories. The new
work areas do not detect tasks stored under legacy paths; check existing
tasks before launching the newly named campaign. Historical files under
`test/` are unchanged.

## Configurations and inputs

Run individual submission commands from `HeavyIonsAnalysis/Configuration`.

| Sample | CRAB configuration | CMSSW configuration | Events/job target |
| --- | --- | --- | --- |
| OO DATA | `crab_OO_DATA.py` | `forest_miniAOD_run3_DATA.py` | 50000 |
| OO MC | `crab_OO_MC.py` | `forest_miniAOD_run3_MC.py` | 30000 |
| pp reference DATA | `crab_ppref_DATA.py` | `forest_miniAOD_run3_ppref_DATA.py` | 50000 |
| pp reference MC | `crab_ppref_MC.py` | `forest_miniAOD_run3_ppref_MC.py` | 100000 |

All use `EventAwareLumiBased` splitting, `totalUnits = -1`, no publication,
and storage site `T2_US_Vanderbilt`. Output paths currently use username
`jvelazqu`; customize the username and site for another account.
DATA memory limits are 2500 MB (OO) and 3000 MB (pp reference); MC uses
2500 MB.

| DATA campaign | Dataset list | Luminosity mask |
| --- | --- | --- |
| OO 2025 | `datasets_OO_DATA.txt`: IonPhysics0 through IonPhysics59 (60 streams), `/OORun2025-PromptReco-v1/MINIAOD` | `Cert_Collisions2025OO_394153_394217_golden.json` |
| pp reference 2024 | `datasets_ppref_DATA.txt`: PPRefHardProbes0 through PPRefHardProbes4 (five streams), `/Run2024J-PromptReco-v1/MINIAOD` | `Cert_Collisions2024_ppref_387474_387721_golden.json` |

Each DATA template defaults to stream 0. The pp reference luminosity mask
is included alongside the existing OO mask; both paths are relative to
this directory. Custom batch lists must use the same campaign patterns
shown above; input lists contain dataset names, not individual ROOT files.

Default OO MC dataset:

```text
/QCD-dijet_pThat15-event-weighted_TuneCP5_5p36TeV_pythia8/HINOOSpring25MiniAOD-CustomTrack_150X_mcRun3_2025_forOO_realistic_v9-v2/MINIAODSIM
```

Default pp reference MC dataset:

```text
/QCD_pThat-15to1200_TuneCP5_5p36TeV_pythia8/RunIIIpp5p36Winter24MiniAOD-141X_mcRun3_2024_realistic_ppRef5TeV_v7-v2/MINIAODSIM
```

## Task names and output locations

DATA request names and output tags are
`HiForest_OO2025_DATA_IonPhysics<N>_v1` and
`HiForest_ppref2024_DATA_PPRefHardProbes<N>_v1`.
MC names are `HiForest_OO2025_MC_Pythia8_CustomTrack_v1` and
`HiForest_ppref2024_MC_Pythia8_v1`.

| Sample | Work area | Output base |
| --- | --- | --- |
| OO DATA | `crab_projects/OO2025_DATA` | `/store/user/jvelazqu/HiForest/OO2025/DATA` |
| OO MC | `crab_projects/OO2025_MC` | `/store/user/jvelazqu/HiForest/OO2025/MC` |
| pp reference DATA | `crab_projects/ppref2024_DATA` | `/store/user/jvelazqu/HiForest/ppref2024/DATA` |
| pp reference MC | `crab_projects/ppref2024_MC` | `/store/user/jvelazqu/HiForest/ppref2024/MC` |

A local task resides at `<workArea>/crab_<requestName>`.
For a new production version, change the Python template's default
`General.requestName` and the corresponding wrapper's `REQUEST_VERSION`
together. MC sample changes also require a distinct sample/request name.

## Build and check

The C++ header/source update requires rebuilding:

```bash
cd /eos/user/j/jvelazqu/Foresting/CMSSW_15_0_11/src
cmsenv
scram b -j 4
cmsRun HeavyIonsAnalysis/Configuration/forest_miniAOD_run3_MC.py
```

The MC configuration currently processes 500 events locally. Inspect its
ROOT output for branch presence and populated values. Syntax checks and
offline batch tests do not establish CMSSW 15.0.11 compatibility, dataset
access, calibration correctness, or CRAB submission success; this
combination still needs build and event processing validation.
Python-only edits do not require recompiling C++.

Validation performed for this refactor: syntax checks passed for nine
Python files and both Bash wrappers. Mocked imports checked all four CRAB
configurations, their paths, luminosity-mask JSON, task names and tags.
454 offline assertions covered the 60 OO and five pp reference datasets,
caller-relative paths with spaces, CRLF and unterminated final lines,
invalid/duplicate entries, missing inputs/CRAB, existing-task skips, and
continuation after a simulated submission failure. All submission
execution in these tests used a fake CRAB executable. No CMSSW build,
event processing, real CRAB submission, commit, or push was performed.

From this directory, syntax checks can be repeated with:

```bash
python3 -m py_compile crab_*.py forest_miniAOD_run3*.py
bash -n submit_multidataset_OO_DATA.sh
bash -n submit_multidataset_ppref_DATA.sh
```

## Submit one dataset

Initialize the CMSSW/CRAB environment and a valid CMS proxy. Review the
dataset, mask, request version, site, and output directory. Each command
below is an independent example; choose the desired configuration.

```bash
crab submit -c crab_OO_DATA.py
crab submit -c crab_OO_MC.py
crab submit -c crab_ppref_DATA.py
crab submit -c crab_ppref_MC.py
```

## Submit multiple DATA datasets

Preview the generated commands without invoking CRAB:

```bash
bash submit_multidataset_OO_DATA.sh --dry-run
bash submit_multidataset_ppref_DATA.sh --dry-run
```

Submit the complete lists:

```bash
bash submit_multidataset_OO_DATA.sh
bash submit_multidataset_ppref_DATA.sh
```

Optionally supply a list and use `--help` for usage:

```bash
bash submit_multidataset_OO_DATA.sh --dry-run /path/to/selected_OO_DATA.txt
bash submit_multidataset_ppref_DATA.sh --dry-run /path/to/selected_ppref_DATA.txt
```

Custom relative list paths are resolved from the caller's directory.
Wrappers then run from their own directory, keeping pset, mask, and work
area paths consistent. Blank/comment lines and CRLF line endings are
accepted. Existing local task directories are skipped, including during
dry runs; this check does not assess remote task status.
Summaries report planned, submitted, skipped, and failed datasets.

## Prepare the commit

From the CMSSW `src` directory:

```bash
git status --short
git diff --check
git diff --stat
```

Stage only the intended changes. Include the deleted tracked filename so
its removal is staged alongside the new configuration:

```bash
git add -A -- \
  HeavyIonsAnalysis/Configuration/.gitignore \
  HeavyIonsAnalysis/Configuration/README.md \
  HeavyIonsAnalysis/Configuration/crab_OO_DATA.py \
  HeavyIonsAnalysis/Configuration/crab_OO_MC.py \
  HeavyIonsAnalysis/Configuration/crab_ppref_DATA.py \
  HeavyIonsAnalysis/Configuration/crab_ppref_MC.py \
  HeavyIonsAnalysis/Configuration/submit_multidataset_OO_DATA.py \
  HeavyIonsAnalysis/Configuration/submit_multidataset_OO_DATA.sh \
  HeavyIonsAnalysis/Configuration/submit_multidataset_ppref_DATA.sh \
  HeavyIonsAnalysis/Configuration/datasets_OO_DATA.txt \
  HeavyIonsAnalysis/Configuration/datasets_ppref_DATA.txt \
  HeavyIonsAnalysis/Configuration/Cert_Collisions2024_ppref_387474_387721_golden.json \
  HeavyIonsAnalysis/Configuration/forest_miniAOD_run3_DATA.py \
  HeavyIonsAnalysis/Configuration/forest_miniAOD_run3_MC.py \
  HeavyIonsAnalysis/Configuration/forest_miniAOD_run3_ppref_DATA.py \
  HeavyIonsAnalysis/Configuration/forest_miniAOD_run3_ppref_MC.py \
  HeavyIonsAnalysis/JetAnalysis/interface/HiInclusiveJetAnalyzer.h \
  HeavyIonsAnalysis/JetAnalysis/src/HiInclusiveJetAnalyzer.cc \
  HeavyIonsAnalysis/JetAnalysis/python/inclusiveJetAnalyzer_cff.py

git diff --cached --check
git diff --cached --stat
git diff --cached
```

Review any changes already staged before these commands. Generated ROOT
files, logs, task directories, caches, and historical `test/` artifacts
are excluded from the explicit staging list.

After validating and reviewing the staged changes:

```bash
git commit -m "Update jet analyzer and standardize OO and ppref CRAB production"
```

Preparing these files does not submit jobs, create a commit, or push.
