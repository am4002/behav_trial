# -*- coding: utf-8 -*-
"""
these are helper functions that are not tests themselves
"""
#imports
from random import randint
from psychopy import visual, event


#helper functions
def infolooper(infoloop,window): #this function loops through a list of strings for presenting test specific info to participants
    for datum in infoloop: 
        infLin=visual.TextStim(window,datum, color=(1.0,1.0,1.0)) #make a text stimuli
        infLin.draw() #draw stimuli
        window.flip() #flip the window
        event.waitKeys(keyList=['return']) #wait for the subject to press return to move to the next piece of info

def seqGen(length): #this is for generating test sequences, returns a list of int in range 0-3 of desired length
    seq = []    
    for i in range(length):
        seq.append(randint(0,3))
    return seq        

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

def pSeqChq(sq1, sq2, pCorrect): #checks two sequences against eachother to make sure they have enough potential matches
    
        
    
    return 0