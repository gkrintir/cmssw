for dir in $(find /afs/cern.ch/work/g/gkrintir/private/HI/MET/CMSSW_8_0_23/src/ ! -name ".*" -type d ) 
do
    echo 'giving read persmision for directory:' $dir
    fs setacl $dir mverweij read
done
