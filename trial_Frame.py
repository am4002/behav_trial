#!/usr/bin/env python
'''
    framework for running behavioral N-back tests  
    
    UPDATE:
        3.14 new gui
    
'''
        
#imports
<<<<<<< HEAD
from psychopy import visual,core,event,gui
from random import shuffle
import csv
from datetime import datetime
from nback_tests import vNback, aNback, nInterleaved, nPaired, nUnpaired
from nback_helpers import infolooper, seqGen
=======
from psychopy import visual,core,gui,event
from random import randint, shuffle
import csv
from datetime import datetime
from nback_tests import vNback, aNback, withinInterleaved, betweenInterleaved, nPaired, nUnpaired, vDistractor, aDistractor, infolooper
>>>>>>> refs/remotes/origin/p1-clone


     
#structures


wnd = visual.Window([1024,768],fullscr=False,allowGUI=True,units='pix',color=(-1,-1,-1)) #psychopy window
funcLis = [] #list to hold all testing functions

<<<<<<< HEAD

#functions    
=======
#functions
def seqGen(length): #this is for generating test sequences, returns a list of int in range 0-3 of desired length
    seq = []    
    for i in range(length):
        seq.append(randint(0,3))
    return seq        

    
>>>>>>> refs/remotes/origin/p1-clone
def popFuncLis(lis): #creates a list of test functions shuffled in a random order.
    '''
    within here all the test functions should be appeneded to the funcLis list, ie. all the tests we will run.
    if new functions are created, they need to be added here.
    '''
    lis.append(vNback)
    lis.append(aNback)
    lis.append(withinInterleaved)
    lis.append(betweenInterleaved)
    lis.append(nPaired)
    lis.append(nUnpaired)
    lis.append(vDistractor)
    lis.append(aDistractor)
        
    shuffle(lis) #randomize order of tests performed
    return 0


#main routine
if __name__ == '__main__':
    data={}
    data['expname']='N-Back'
    data['expdate']=datetime.now().strftime('%Y%m%d_%H%M')
    data['participantid']=''
    dlg=gui.DlgFromDict(data,title='Input data',fixed=['expname','expdate'],order=['expname','expdate','participantid'])
    if not dlg.OK:
        core.quit()
        
    outName='P%s_%s.csv'%(data['participantid'],data['expdate'])
    outFile = open(outName, 'wb')
    outWr = csv.writer(outFile) # a .csv file with that name. Could be improved, but gives us some control
    popFuncLis(funcLis) #populate list of test functions 
    wnd.flip() #initialize window 
    
    #list that holds introductory information for the subject
    startInfo = ['Press return to continue',
             'Welcome subject '+data['participantid'],
             'In this experiment you will preform a series of N-back tests that involve visual and auditory components',
             'Each test is prefaced by a short explanation',
             'If you have any remaining questions, or would no longer like to take part in this pilot study, please notify an experimenter now']
    infolooper(startInfo, wnd) #loop through initial information 
    #loop that executes test functions
    for test in funcLis:
        tSq = seqGen(30) #here is where we specify how long the test sequence is going to be
        print "generation complete"        
        print str(test)+": test started"
<<<<<<< HEAD
        test(outWr, 2, wnd, tSq, 0.75) #filled with the generic arguments for all our test functions, change the number in seqGen() to make the list longer/shorter
        print str(test)+": test ended"
        
    '''
    cleanup/file closing/participant thank you message
    '''
    outFile.close() #close the output file
    thanks=visual.TextStim(wnd,'thank you for your participation, all tests are concluded', color=(1.0,1.0,1.0)) #thank the subject for their participation
    thanks.draw()
=======
        test(outWr, 2, wnd, seqGen(3)) #filled with the generic arguments for all our test functions, change the number in seqGen() to make the list longer/shorter
        print str(test)+": test ended"        
    outFile.close() #close the output file
    ready=visual.TextStim(wnd,'Thank you for your participation, all tests are concluded?', color=(1.0,1.0,1.0)) #thank the subject for their participation
    ready.draw()
>>>>>>> refs/remotes/origin/p1-clone
    wnd.flip()
    event.waitKeys(keyList=['return'])    
    wnd.close()     #close the psychopy windo
    print "all tests concluded"    
    

    
    