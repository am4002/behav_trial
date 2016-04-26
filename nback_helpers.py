# -*- coding: utf-8 -*-
"""
these are helper functions that are not tests themselves

Updated date:
    April 26
Change:
    a test is added to the association trainer
    quit function added
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
    
    
def pTrainer(window): #Association learner + a short test
    colorcode=['red','blue','green','yellow']
    audicode=[233.2,277.2,329.6,392]
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
    infoloop3=['Press L if you want to rewatch the presentation',
               'Press enter if you want to start the test',]
    infoloop4=['Welcome to the association test',
               'You will first see a colour square OR hear a tone',
               'Then you will be presented TWO tones OR two colour squares',
               'Indicate which one of them is paired to the target',
               'Z for choice 1, M for choice 2',
               'You will get feedback for your answer',
               'There are 20 trials' ]

    vstimlist=[];astimlist=[]
    for i in range(4):
        vstimlist.append(visual.Rect(window,width=200.0,height=200.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=1.0,bits=8)) 
       
    infolooper(infoloop1,window)
    
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
    #adjust the number of repetition here
    n.extend(n*4)
    shuffle(n)
    #iterate the pair 5 times
    for i in n:
        vstimlist[i].draw()
        window.flip()
        astimlist[i].play()
        core.wait(1.5)
        window.flip()
        core.wait(0.7)
        #q to quit        
        if event.getKeys(keyList=['q' ,'escape']):
            sure=visual.TextStim(window,'Do you want to quit?',color='white')
            sure.draw()
            window.flip()
            pressed=event.waitKeys(keyList=None)
            if pressed[0]=='return':                
                window.close()
                core.quit()
            else:
                pass;

    s1=visual.TextStim(window,'Press L or Enter',color='white')
    infolooper(infoloop3,window)
    s1.draw()
    window.flip()
    response=event.waitKeys(keyList=['return','l'])
    
    #The subjects choose whether to view the pairings again or go to test
    while (response[0][0]=='l'):
        for i in n:
            vstimlist[i].draw()
            window.flip()
            astimlist[i].play()
            core.wait(1.5)
            window.flip()
            core.wait(0.7)
        infolooper(infoloop3,window)
        s1.draw()
        window.flip()
        response=event.waitKeys(keyList=['return','l'])
    infolooper(infoloop4,window)
    window.flip()
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    
    shuffle(n) #change the sequence 
    #some useful texts for the test
    w1=visual.TextStim(window,'Target',color='white')
    w2=visual.TextStim(window,'Choices',color='white')
    w3=visual.TextStim(window,'Choice 1',color='white',pos=(0.0,130))
    w4=visual.TextStim(window,'Choice 2',color='white',pos=(0.0,130))
    w5=visual.TextStim(window,'Which one is paired to the target?\nZ for choice 1 / M for choice 2',color='white')
    w6=visual.TextStim(window,'Good job!',color='white')
    w7=visual.TextStim(window,'Incorrect',color='white')
    w8=visual.TextStim(window,'',color='white',pos=(0.0,300))
    w8.setAutoDraw(True)
    result=[0,0]
    #test the pairs 5 times each
    #testing logic (this is so long please don't try to read it...)
    for index,i in enumerate(n):
        ind=randint(0,1)
        w8.setText('Trial '+str(index+1)) #show subjects their progress so that they have some motivation
        if ind==0: #target is visual
            w1.draw()
            window.flip()
            core.wait(1.0)
            window.flip()
            core.wait(1.0)
            vstimlist[i].draw()
            window.flip()
            core.wait(1.0)
            window.flip()
            core.wait(1.0)
            w2.draw()
            window.flip()
            core.wait(1.0)
            window.flip()
            core.wait(0.5)
            a=randint(0,1)
            if a==0: #show correct answer first
                w3.draw() 
                astimlist[i].play()
                window.flip()
                core.wait(1.0)
                window.flip()
                core.wait(1.0)
                b=randint(0,3)
                while b==i:#make sure incorrect answer is different from correct
                    b=randint(0,3)
                w4.draw()
                astimlist[b].play()
                window.flip()
                core.wait(1.0)
                window.flip()
                core.wait(1.0)
            else:# show incorrect answer first
                w3.draw()
                b=randint(0,3)
                while b==i:#make sure incorrect answer is different from correct
                    b=randint(0,3)
                astimlist[b].play()
                window.flip()
                core.wait(1.0)
                window.flip()
                core.wait(1.0)
                w4.draw() 
                astimlist[i].play()
                window.flip()
                core.wait(1.0)
                window.flip()
                core.wait(1.0)
        else:#target is auditory
            w1.draw()
            window.flip()
            core.wait(1.0)
            window.flip()
            core.wait(1.0)
            cross.draw()
            astimlist[i].play()
            window.flip()
            core.wait(1.0)
            window.flip()
            core.wait(1.0)
            w2.draw()
            window.flip()
            core.wait(1.0)
            window.flip()
            core.wait(1.0)
            a=randint(0,1)
            if a==0: #show correct answer first
                w3.draw() 
                vstimlist[i].draw()
                window.flip()
                core.wait(1.0)
                window.flip()
                core.wait(1.0)
                b=randint(0,3)
                while b==i:#make sure incorrect answer is different from correct
                    b=randint(0,3)
                w4.draw()
                vstimlist[b].draw()
                window.flip()
                core.wait(1.0)
                window.flip()
                core.wait(1.0)
            else:# show incorrect answer first
                w3.draw()
                b=randint(0,3)
                while b==i:#make sure incorrect answer is different from correct
                    b=randint(0,3)
                vstimlist[b].draw()
                window.flip()
                core.wait(1.0)
                window.flip()
                core.wait(1.0)
                w4.draw() 
                vstimlist[i].draw()
                window.flip()
                core.wait(1.0)
                window.flip()
                core.wait(1.0)
        #q to quit        
        if event.getKeys(keyList=['q' ,'escape']):
            sure=visual.TextStim(window,'Do you want to quit?',color='white')
            sure.draw()
            window.flip()
            pressed=event.waitKeys(keyList=None)
            if pressed[0]=='return':                
                window.close()
                core.quit()
            else:
                pass;        
        w5.draw() #ask for answers
        window.flip()
        answer=event.waitKeys(keyList=['z','m'])
        if (a==0 and answer[0][0]=='z') or (a==1 and answer[0][0]=='m'):#subject chooses correctly
            w6.draw()
            window.flip()
            core.wait(1.0)
            result[0]=result[0]+1
        else: #choose wrong
            w7.draw()
            window.flip()
            core.wait(1.0)
            result[1]=result[1]+1
    w8.setAutoDraw(False)
    infoloop5=['Test completed',
               'Your final result:',
               str(result[0])+' correct\n'+str(result[1])+' incorrect',
               'Thanks for completing the Association Trainer',
               'Press enter/return to start N-Back exercise']
    infolooper(infoloop5,window)
    print('association test: '+ str(result[0])+' correct') #output of test result for the experimenter
    print(str(result[1])+' incorrect')


    
    
    
    
    
 
 
