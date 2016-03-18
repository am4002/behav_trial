# -*- coding: utf-8 -*-
"""
these are helper functions that are not tests themselves
"""
#imports
from random import randint, shuffle
from psychopy import visual, event, sound, core


#helper functions
def infolooper(infoloop,window): #this function loops through a list of strings for presenting test specific info to participants
    for datum in infoloop: 
        infLin=visual.TextStim(window,datum, color=(1.0,1.0,1.0)) #make a text stimuli
        infLin.draw() #draw stimuli
        window.flip() #flip the window
        event.waitKeys(keyList=['return']) #wait for the subject to press return to move to the next piece of info

def seqGen(length, pCorr): #this is for generating test sequences, returns a list of int in range 0-3 of desired length, with around a specified %correct
    seq = []   
    idealNum = int(length*pCorr) #how many should be correct
    correctNum = 0
    finished = False   
    
    print "around "+str(idealNum)+" correct trials should be created"
    while finished == False:
        #fill the list with randoms 
        seq[:] = []#reset the list to be empty
        correctNum = 0 #reset the amount correct to 0
        for i in range(length):
            seq.append(randint(0,3))
            
        #see how many correct trials occur just from the random filling
        for each in seq: #for each element in the sequence
            if each == seq[each-2]: #if that element is the same as the element two back
                correctNum = correctNum + 1 #add one to the counter of potentially correct responses
 
        if correctNum < (idealNum-(int(length/8))) or correctNum > (idealNum+(int(length/8))): #if the % correct is more than +/-15% of the specified amount
            print "new generated sequence has "+str(correctNum)+ " potentially correct trials"        
            print "try generating again"
        else:
            finished = True
            print "final generated sequence has "+str(correctNum)+ " potentially correct trials" #report how many corrects are possible (should be slightly larger than initial target)

    return seq #return finished sequence
'''
def sSeqChq(sq, pCorr): #checks sequences to make sure they have enough potentially correct trials
    print "starting sequence check"
    correctNum = 0 #for keeping track of how many correct trials there are
    lSq = len(sq) #var for holding the length of the sequence, because it's easier than referring to it endlessly
    idealNum = int(lSq*pCorr) #roughly how many should idealy be correct tirals   
    
    for each in sq: #for each element in the sequence
        if each == sq[each-2]: #if that element is the same as the element two back
            correctNum = correctNum + 1 #add one to the counter of potentially correct responses
            
    print "there are "+str(correctNum)+" potential corrects out of "+str(lSq)+" in this sequence; there should be around "+str(idealNum)

    if correctNum < (idealNum-(int(lSq/10))): #if there is too high or too low a % of sequences correct
        print "too few corrects"        
        for r in range(2,int(lSq/3)):  #then for each element in roughly a 1/3 of the sequence, avoiding the first two     
            try:
                pointMut = randint(2,lSq)  #choose a random point in the sequence
                changeTo = sq[(pointMut-2)] #corce point value to change int the same as 2 back
                print "mutate into: "+ str(changeTo) 
                sq[pointMut] = changeTo #enact change, creating new potential correct in the sequence
            except IndexError:
                print "out of index range, just try again"      
        sSeqChq(sq, pCorr) #recursively call this function
    
    elif correctNum > (idealNum+(int(lSq/10))):
        print "too many corrects"
        for r in range(2,int(lSq/3)):  #then for each element in roughly a 1/3 of the sequence, avoiding the first two     
            try:           
                pointMut = randint(2,lSq)  #choose a random point in the sequence
                changeTo = randint(0,3) #choose a random new value for trial
                print "mutate into: "+ str(changeTo)
                sq[pointMut] = changeTo #enact change, randomizing one point in the sequence
            except IndexError:
                print "out of index range, just try again"
        sSeqChq(sq, pCorr) #recursively call this function       
        
    else:
        print "% correct within acceptable range"
        return 0
'''
def pSeqChq(sq1, sq2, pCorrect): #checks two sequences against eachother to make sure they have enough potential matches    
    return 0
    
    
def pTrainer(window):
    colorcode=['red','blue','green','yellow']
    audicode=['C','D','E','F']
    
    #text infomation
    cross=visual.TextStim(window,'+',color='white')
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    pair=visual.TextStim(window,'Pair ',color='white')
    
    infoloop1=['Welcome to the Association Trainer',
             'You will see/hear a series of PAIRED colour squares and audio tones',
             'Try your best to remember them',
             'You will be tested on how well you remember them later',
             'Press return/enter to continue']
    
    infoloop2=['You have been presented with the 4 pairs sequentially',
               'Now you will be shown the pairs simultaneously and randomly',
               'For a couple of times',
               'Press return/enter to continue']

    quit=visual.TextStim(window,'Thanks for completing the association trainer!', color=(1.0,1.0,1.0))
    s1=visual.TextStim(window,'Press L to rewatch the presentation or Q to start the task', color=(1.0,1.0,1.0))    
    vstimlist=[];astimlist=[]
    
    #create stimuli list
    for i in range(4):
        vstimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=1.0,bits=8)) 
       
    infolooper(infoloop1,window)
    #show the pairings sequentially
    for i,v in enumerate(vstimlist):
        pair.setText('Pair '+str(i+1))
        pair.draw()
        window.flip()
        core.wait(1.0)
        window.flip()
        core.wait(1.0)
        v.draw()
        window.flip()
        core.wait(1.0)
        window.flip()
        core.wait(1.0)
        cross.draw()
        window.flip()
        astimlist[i].play()
        core.wait(1.0)
        window.flip()
        core.wait(1.0)
    
    infolooper(infoloop2,window)
    n=[0,1,2,3]
    n.extend(n*4)
    shuffle(n)
    #iterate the pair 5 times
    for i in n:
        vstimlist[i].draw()
        window.flip()
        astimlist[i].play()
        core.wait(0.75)
        window.flip()
        core.wait(0.2)
    
#Ask if they want to rewatch the associations or proceed to n-back task
    s1.draw()
    window.flip()
    response=event.waitKeys(keyList=['q','l'])
    while (response[0][0]=='l'): #subjects could repeat how many times they want
        for i in n:
            vstimlist[i].draw()
            window.flip()
            astimlist[i].play()
            core.wait(1.0)
            window.flip()
            core.wait(1.0)
        s1.draw()
        window.flip()
        response=event.waitKeys(keyList=['q','l'])
        
    quit.draw()
    window.flip()
    core.wait(2.0)
