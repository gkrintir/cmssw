#!/usr/bin/env python
import os, re
import commands
import math, time
import sys

print 
print 'START'
print 
########   YOU ONLY NEED TO FILL THE AREA BELOW   #########
########   customization  area #########
NumberOfJobs= 15 # number of jobs to be submitted #42
interval = 10 # 4number files to be processed in a single job, take care to split your file so that you run on all files. The last job might be with smaller number of files (the ones that remain).
OutputFileNames = "pcc_Data_PixVtx_Event_92X_300019" # base of the output file name, they will be saved in res directory
ScriptName = "/afs/cern.ch/work/g/gkrintir/private/PCCTools/CMSSW_9_2_6/src/RecoLuminosity/LumiProducer/test/analysis/test/Run_PixVertex_Event_OnBatch.py" # script to be used with cmsRun
FileList = "run_300019.txt" # list with all the file directories
LumiMask = "True" # apply lumimask
queue = "cmscaf1nd" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
########   customization end   #########

path = os.getcwd()
print
print 'do not worry about folder creation:'
os.system("rm -r tmp2")
os.system("mkdir tmp2")
os.system("mkdir res2")
print

##### loop for creating and sending jobs #####
for x in range(1, int(NumberOfJobs)+1):
   ##### creates directory and file list for job #######
   os.system("mkdir -p tmp2/"+str(x))
   os.chdir("tmp2/"+str(x))
   os.system("sed '"+str(1+interval*(x-1))+","+str(interval*x)+"!d' ../../"+FileList+" > list.txt ")
   
   ##### creates jobs #######
   with open('job.sh', 'w') as fout:
      fout.write("#!/bin/sh\n")
      fout.write("echo\n")
      fout.write("echo\n")
      fout.write("echo 'START---------------'\n")
      fout.write("echo 'WORKDIR ' ${PWD}\n")
      fout.write("source /afs/cern.ch/cms/cmsset_default.sh\n")
      fout.write("cd "+str(path)+"\n")
      fout.write("cmsenv\n")
      fout.write("cmsRun "+ScriptName+" outputFile='res2/"+OutputFileNames+"_"+str(x)+".root' files='tmp2/"+str(x)+"/list.txt' lumiMask="+LumiMask+"\n")
      fout.write("mv /afs/cern.ch/work/g/gkrintir/private/PCCTools/CMSSW_9_2_6/src/RecoLuminosity/LumiProducer/test/analysis/test/res2/"+OutputFileNames+"_"+str(x)+".root /eos/cms/store/group/comm_luminosity/PCC/ForLumiComputation/2017/VdMFills/6016/ZeroBias_Or_AlwaysTrue_splitPerBXTrue/\n")
      #fout.write("rm /afs/cern.ch/work/g/gkrintir/private/HI/ttbar_sig_new/CMSSW_8_0_26_patch2/src/core*\n")
      fout.write("echo 'STOP---------------'\n")
      fout.write("echo\n")
      fout.write("echo\n")
   os.system("chmod 755 job.sh")
   #os.chdir("../..")
 
   ###### sends bjobs ######
   os.system("bsub -q "+queue+" -o logs job.sh")
   print "job nr " + str(x) + " submitted"
   
   os.chdir("../..")
   
print
print "your jobs:"
os.system("bjobs")
print
print 'END'
print

