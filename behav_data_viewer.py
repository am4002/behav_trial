# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:18:33 2016

@author: a
"""

import csv
from numpy import mean
from os import path, listdir
from time import time
from datetime import datetime



pData = [fi for fi in listdir('.') if path.isfile(fi) and fi.endswith('.csv')] #for each .csv file in the current directiory, add that file to this list
t = str(time()) #generate a timestamp to mark the data output so each run is unique and dated
output = open('stats_at_%s.txt'%t,'wb') #create file to save results
pAnz = [] #holds data for each participant, as a tuple
groupAnz = [] #holds the aglomerated data for all participants


def quickPercent(right, total): #compares the number correct vs the total possible correct    
    r = len(right)
    t = len(total)
    return str((t/r)*100)+'% correct'



def participantReader(pLis,anz):  #reads participant files and generates % correct for each condition in each subject
    for pF in pLis:
        subj = path.splitext(str(pF))
        subj = subj[0]
        
        #placeholders for the various tests
        visCorr = 0
        audCorr = 0
        withvICorr = 0
        withaICorr = 0
        betvICorr = 0
        betaICorr = 0
        pairCorr = 0
        unpairCorr = 0
        vDisCorr = 0
        aDisCorr = 0
        numTri = len(pLis)/8 #the number of trials in each condition
        
        #because interleaved trials are broken up into corrects for visual/auditory trials, more palceholders
        numWithV = 0
        numWithA = 0
        numBetV = 0
        numBetA = 0
        
        with open (pF, 'rb') as par:
            pRead = csv.reader(par)
            for entry in pRead:
                tryType = entry[0]
                print entry
                print tryType
                print tryType[1]
                print entry[2]
                print entry[3]
                if entry[2] == entry[3]:                
                    if tryType == 'visual': visCorr += 1
                    elif tryType == 'auditory': audCorr += 1
                    elif tryType == 'withinInterleaved visual': withvICorr +=1
                    elif tryType == 'withinInterleaved auditory': withaICorr +=1
                    elif tryType == 'betweenInterleaved visual':  betvICorr +=1     
                    elif tryType == 'betweenInterleaved auditory': betaICorr +=1
                    elif tryType == 'paired': pairCorr += 1
                    elif tryType == 'unpaired': unpairCorr += 1
                    elif tryType == 'vDistractor': vDisCorr += 1
                    elif tryType == 'aDistractor':aDisCorr += 1
                if tryType == 'withinInterleaved visual': numWithV +=1
                elif tryType == 'withinInterleaved auditory': numWithA +=1
                elif tryType == 'betweenInterleaved visual':  numBetV +=1     
                elif tryType == 'betweenInterleaved auditory': numBetA +=1
        
        #close the particiapnt's file
        par.close()
        
        #convert the number of corrects into a percentage  
        vPer = visCorr/numTri
        aPer = audCorr/numTri
        withvPer = withvICorr/numWithV
        withaPer = withaICorr/numWithA
        betvPer = betvICorr/numBetV
        betaPer = betaICorr/numBetA
        pairPer = pairCorr/numTri
        upairPer = unpairCorr/numTri
        vdisPer = vDisCorr/numTri        
        adisPer = aDisCorr/numTri
        
        #store said percentages in the list taken at function call        
        anz.append([subj,vPer,aPer,withvPer,withaPer,betvPer,betaPer,pairPer,upairPer,vdisPer,adisPer])

#output includes: condition, trial number, whether it's target, whether a hit, RT
def displayStat(pStats,out):
    preface = 'statistics generated on %s  from n-back task with %s paricipants\n' % (datetime.now(),str(len(pStats)))
    linebreak = '~-~ '*18 + '\n'
    
    totvisCorr = []
    totaudCorr = []
    totwithvICorr = []
    totwithaICorr = []
    totbetvICorr = []
    totbetaICorr = []
    totpairCorr = []
    totunpairCorr = []
    totvDisCorr = []
    totaDisCorr = []
    
    print >> out, preface    
    print >> out, linebreak
    print >> out, '          +++++ INDIVIDUAL STATISTICS +++++\n'
    print >> out, linebreak    
    
    for subject in pStats:
        
        #compile stats from each subject to get an average % correct for each condition
        totvisCorr.append(subject[1])
        totaudCorr.append(subject[2])
        totwithvICorr.append(subject[3])
        totwithaICorr.append(subject[4])
        totbetvICorr.append(subject[5])
        totbetaICorr.append(subject[6])
        totpairCorr.append(subject[7])
        totunpairCorr.append(subject[8])
        totvDisCorr.append(subject[9])
        totaDisCorr.append(subject[1])
        
        #for displaying individual stats, how one subject did on each condition        
        mvC = str(format(subject[1]*100,'.3f'))
        maC = str(format(subject[2]*100,'.3f'))
        mIVC = str(format(subject[3]*100,'.3f'))
        mIAC = str(format(subject[4]*100,'.3f'))
        mBVC = str(format(subject[5]*100,'.3f'))
        mBAC = str(format(subject[6]*100,'.3f'))
        pC = str(format(subject[7]*100,'.3f'))
        upC = str(format(subject[8]*100,'.3f'))
        vdC = str(format(subject[9]*100,'.3f'))
        adC = str(format(subject[10]*100,'.3f'))
        
        print >> out, linebreak
        
        line1 = '[Participant %s percentage corrects per condition]' % subject[0]
        line2 = '[Visual: %s ; Auditory: %s ;]' % (mvC,maC)
        line3 = '[Within Interleaved, Visual: %s ; Within Interleaved, Auditory: %s ;]' % (mIVC,mIAC)
        line4 = '[Between Interleaved, Visual: %s ; Between Interleaved, Auditory: %s ;]' % (mBVC,mBAC)
        line5 = '[Paired: %s ; Unpaired: %s ;]' % (pC,upC)
        line6 = '[Distractor, Visual: %s ; Distractor, Auditory: %s ;]' % (vdC,adC)
        print >> out, line1
        print >> out, line2
        print >> out, line3
        print >> out, line4
        print >> out, line5
        print >> out, line6
        
        print >> out, linebreak

    print >> out, linebreak
    print >> out, '          +++++ GROUP STATISTICS +++++\n'
    print >> out, linebreak
        
    groupmvC = str(format(mean(totvisCorr),'.3f'))
    groupmaC = str(format(mean(totaudCorr),'.3f'))
    groupmIVC = str(format(mean(totwithvICorr),'.3f'))
    groupmIAC = str(format(mean(totwithaICorr),'.3f'))
    groupmBVC = str(format(mean(totbetvICorr),'.3f'))
    groupmBAC = str(format(mean(totbetaICorr),'.3f'))
    grouppC = str(format(mean(totpairCorr),'.3f'))
    groupupC = str(format(mean(totunpairCorr),'.3f'))
    groupvdC = str(format(mean(totvDisCorr),'.3f'))
    groupadC = str(format(mean(totaDisCorr),'.3f'))     
        
    
    gline1 = '[Total percentage corrects per condition for all %s participants]' % str(len(pStats))
    gline2 = '[Visual: %s ; Auditory: %s ;]' % (groupmvC,groupmaC)
    gline3 = '[Within Interleaved, Visual: %s ; Within Interleaved, Auditory: %s ;]' % (groupmIVC,groupmIAC)
    gline4 = '[Between Interleaved, Visual: %s ; Between Interleaved, Auditory: %s ;]' % (groupmBVC,groupmBAC)
    gline5 = '[Paired: %s ; Unpaired: %s ;]' % (grouppC,groupupC)
    gline6 = '[Distractor, Visual: %s ; Distractor, Auditory: %s ;]' % (groupvdC,groupadC)
    print >> out, gline1
    print >> out, gline2
    print >> out, gline3
    print >> out, gline4
    print >> out, gline5
    print >> out, gline6
    print >> out, glinebreak 


if __name__ == '__main__':
    participantReader(pData,pAnz)
    displayStat(pAnz,output)
    output.close()