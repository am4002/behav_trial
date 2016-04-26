#!/usr/bin/env python
'''
    framework for running behavioral N-back tests (linux version)
    
    UPDATE:
        4.18 MEG related
    
'''
        
#imports
from psychopy import visual,core,gui,event
from random import shuffle
import csv
from datetime import datetime
from nback_test_linux import vNback, aNback, withinInterleaved, betweenInterleaved, nPaired, nUnpaired, vDistractor, aDistractor, prepMEG
from nback_helpers import infolooper, seqGen, pTrainer
     

#structures

funcLis = [] #list to hold all testing functions


#functions
def popFuncLis(lis): #creates a list of test functions shuffled in a random order.
    '''
    
    within here all the test functions should be appeneded to the funcLis list, ie. all the tests we will run.
    if new functi
    
    
    
    ons are created, they need to be added here.
    '''
    
    lis.append(vNback)
    lis.append(aNback)
    
    #lis.append(withinInterleaved)
    lis.append(betweenInterleaved)
    lis.append(nPaired)
    #lis.append(nUnpaired)
    lis.append(vDistractor)
    lis.append(aDistractor)
    '''
    lis.extend(1)
    '''
    shuffle(lis) #randomize order of tests performed
    return 0


#main routine
if __name__ == '__main__':
    data={}
    data['expname']='N-Back'
    data['expdate']=datetime.now().strftime('%Y%m%d_%H%M')
    data['participantid']=''
    data['MEG']=False
    data['Training']=False
    dlg=gui.DlgFromDict(data,title='Input info',fixed=['expname','expdate'],order=['expname','expdate','MEG','Training','participantid'])
    if not dlg.OK:
        core.quit()
    MEG=data['MEG']
    Training=data['Training']
    outName='%s_%s.csv'%(data['participantid'],data['expdate'])
    outFile = open(outName, 'wb')
    outWr = csv.writer(outFile) # a .csv file with that name. Could be improved, but gives us some control
    outWr.writerow(['%s, %s, %s, %s, %s\n'%('condition', 'trial_no', 'target', 'response', 'Reaction time')]) # write out header
    wnd = visual.Window([1024,768],fullscr=True,allowGUI=False,units='pix',color=(-1,-1,-1)) #psychopy window    

    
    outTXT ='%s_%s.txt'%(data['participantid'],data['expdate'])
    outTxFile = open(outTXT, 'wb')

    popFuncLis(funcLis) #populate list of test functions 
    wnd.flip() #initialize window 
    
    #list that holds introductory information for the subject
    startInfo = ['Press return to continue',
             'Welcome participant '+data['participantid'],
             'In this experiment you will preform a series of N-back tests that involve visual and auditory components',
             'Each test is prefaced by a short explanation',
             'If you have any remaining questions, or would no longer like to take part in this pilot study, please notify an experimenter now']
    infolooper(startInfo, wnd) #loop through initial information 
    
    if Training==True:
        pTrainer(wnd) #present the audio/visual stimuli pairings to subject
    if MEG == True:
        prepMEG()
        
    #loop that executes test functions
    for test in funcLis:
        tSq = seqGen(150,0.25) #here is where we specify how long the test sequence is going to be, and what % correct is desired
        print "generation complete"        
        print str(test)+": test started"
        if MEG==True:
            test(outWr, outTxFile, 2, wnd, tSq, 1.5,inMEG=True)
        else:
            test(outWr, outTxFile, 2, wnd, tSq, 1.5) #filled with the generic arguments for all our test functions, change the number in seqGen() to make the list longer/shorter
        print str(test)+": test ended"

    
    '''
    cleanup/file closing/participant thank you message
    '''
    outFile.close() #close the output file
    thanks=visual.TextStim(wnd,'thank you for your participation, all tests are concluded', color=(1.0,1.0,1.0)) #thank the subject for their participation
    thanks.draw()
    wnd.flip()
    event.waitKeys(keyList=['return'])    
    wnd.close()     #close the psychopy windo
    print "all tests concluded"    
    

    
    
