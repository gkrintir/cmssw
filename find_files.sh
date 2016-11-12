for dir in $(find ~/tempeos/cms/store/data/Run2015E/SingleMuHighPt/AOD/PromptReco-v1/ ! -name ".*" -type f ) 
do
    echo $dir >> logfile.txt
done
