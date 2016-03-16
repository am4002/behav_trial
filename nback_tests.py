# -*- coding: utf-8 -*-
"""
    collection of N-back tests to be preformed
    
    TODO:
    
    -add other test conditions
        +auditory distractor test
        +visual distractor test
    
"""


#imports
from psychopy import visual, sound, core, event,logging
from random import randint, shuffle
from nback_helpers import infolooper,sSeqChq, pSeqChq


#test functions
def vNback (fi, nback_no, window, seq, dura, trial_no=None, adaptive=False): #visual nback test

    #test the sequence to make sure it has enough potential corrects    
    #sSeqChq(seq, 0.25)

    #data structures
    colorcode=['red','blue','green','yellow']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    infoloop=['press return/enter to continue',
             'this is the visual 2-Nback test',
             'you will see a series of coloured squares',
             'press enter if the colour of a square matches the colour of a square two steps back']
    stimlist=[]
    target=[0,0]
    n=0
    
    #create stimuli list and mark down target trials
    for i in seq:
        stimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        if n > nback_no-1:
            #if the event match with the one n events ago (n specified by 'nback_no')
            #mark it as a target trial
            if i==seq[n-nback_no]:
                target.append(1)
            else:
                target.append(0)
        n = n+1
    infolooper(infoloop,window) #present basic test info for participant (what test, etc)
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    n=0
    #draw stimuli and record response time
    for trial in stimlist:
        response=None; hit=None; time=None
        trial.draw()
        starttime=window.flip()
        #each stimulus is presented for the dura specified
        response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= dura:
            pass
        #Currently only RT for catch trials will be recorded
        if target[n]==1:
            hit=False
            if response!=None:
                time=response[0][1]-starttime
                hit=True
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('visual', n+1, str(target[n]==1), str(hit), str(time))])
        n = n+1
        window.flip()
        core.wait(0.3)
    
def aNback (fi, nback_no, window, seq, dura, trial_no=None, adaptive=False):
    
    #test the sequence to make sure it has enough potential corrects    
    #sSeqChq(seq, 0.25)    
    
    #data structures
    audicode=['C','D','E','F']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    infoloop=['press return/enter to continue',
             'this is the auditory 2-Nback test',
             'you will see a series of audio tones',
             'press enter if the tone played matches the tone two steps back']
    stimlist=[]
    target=[0,0]
    n=0

    #create stimuli list and mark down target trials
    for i in seq:
        stimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=dura,bits=8))
        if n > nback_no-1:
            #if the event match with the one n events ago (n specified by argument 'nback_no')
            #mark it as a target trial
            if i==seq[n-nback_no]:
                target.append(1)
            else:
                target.append(0)
        n = n+1
    infolooper(infoloop,window) #present basic test info for participant (what test, etc)
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    n=0
    #play stimuli and record response time
    for trial in stimlist:
        response=None; hit=None; time=None
        cross.draw()
        trial.play()
        starttime=window.flip()
        #each stimulus is played for the duration specified
        response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= dura:
            pass
        #Currently only RT for catch trials will be recorded
        if target[n]==1:
            hit=False
            if response!=None:
                time=response[0][1]-starttime
                hit=True
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('auditory', n+1, str(target[n]==1), str(hit), str(time))])
        n = n+1
        window.flip()
        core.wait(0.5)
    
    
def nInterleaved (fi, nback_no, window, seq, dura, trial_no=None, adaptive=False):

    #test the sequence to make sure it has enough potential corrects    
    #sSeqChq(seq, 0.25)

    #data structures
    audicode=['C','D','E','F']
    colorcode=['red','blue','green','yellow']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    infoloop=['press return/enter to continue',
             'this is the interleaved 2-Nback test',
             'you will see a series that contains both audio tones and coloured squares seperately',
             'press enter if the tone played matches the tone two steps back, or if the colour matches a colour two steps back']
    stimlist=[]
    target=[0,0];modality=[]
    n=0

    #decide stimuli modality
    for i in range(len(seq)):
        modality.append(randint(0,1)==0)
    for i in seq:
        if n > nback_no-1:
            #if the event match with the one n events ago (n specified by argument 'nback_no')
            #mark it as a target trial
            if i==seq[n-nback_no]:
                target.append(1)
                #adjust stimuli modality to make the target and
                #the event it matches to from different modalities
                if modality[n]==modality[n-nback_no]:
                    modality[n]=not modality[n]
            else:
                target.append(0)
        # create stimlist with two modalities
        if modality[n]==True:
            stimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        else:
            stimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=dura,bits=8))
        n=n+1
    infolooper(infoloop,window) #present basic test info for participant (what test, etc)
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    n=0
    mod=None
    #play/draw stimuli and record response time
    for trial in stimlist:
        response=None; hit=None; time=None
        if modality[n]==True:
            trial.draw()
            mod='visual'
        else:
            trial.play()
            cross.draw()
            mod='auditory'
        starttime=window.flip()
        #each stimulus is displayed for the duration specified
        response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= dura:
            pass
        #Currently only RT for catch trials will be recorded
        if target[n]==1:
            hit=False
            if response!=None:
                time=response[0][1]-starttime
                hit=True
        #output includes: condition, modality, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %s, %d, %s, %s, %s\n'%('interleaved', mod, n+1, str(target[n]==1), str(hit), str(time))])
        n = n+1
        window.flip()
        core.wait(0.5)
    
    
#paired nback task
#Currently auditory sequence and visual sequence are exactly the same, though it may not be the best way
#think about this later
def nPaired (fi, nback_no, window, seq, dura, trial_no=None, adaptive=False):
    
    #test the sequence to make sure it has enough potential corrects    
    #sSeqChq(seq, 0.25)    
    
    #data structures
    audicode=['C','D','E','F']
    colorcode=['red','blue','green','yellow']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    infoloop=['press return/enter to continue',
             'this is the paired 2-Nback test',
             'you will see a series that contains both audio tones and coloured squares together',
             'in this test, the same colour/tone pair is always presented together',
             'press enter if the colour/tone pair matches the pair two steps back']
    vstimlist=[];astimlist=[]
    target=[0,0]
    n=0

    #create two stimuli lists and mark down target trials
    for i in seq:
        vstimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=dura,bits=8))
        if n > nback_no-1:
            #if the event match with n events ago (n specified by 'nback_no')
            #mark it as a target trial
            if i==seq[n-nback_no]:
                target.append(1)
            else:
                target.append(0)
        n = n+1
    infolooper(infoloop,window) #present basic test info for participant (what test, etc)
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    n=0
    #play/draw stimuli and record response time
    for vtrial in vstimlist:
        response=None; hit=None; time=None
        vtrial.draw()
        astimlist[n].play()
        starttime=window.flip()
        #each stimulus is displayed for the duration specified
        response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= dura:
            pass
        #Currently only RT for catch trials will be recorded
        if target[n]==1:
            hit=False
            if response!=None:
                time=response[0][1]-starttime
                hit=True
        window.flip()

#output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('paired', n+1, str(target[n]==1), str(hit), str(time))])
        n = n+1
        core.wait(0.5)
    

#unpaired nback task
def nUnpaired (fi, nback_no, window,  seq, dura, trial_no=None, adaptive=False):

    #data structures
    audicode=['C','D','E','F']
    colorcode=['red','blue','green','yellow']
    vseq = seq
    aseq = list(seq)
    shuffle(aseq)
    trial_no=len(vseq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    infoloop=['press return/enter to continue',
             'this is the unpaired 2-Nback test',
             'you will see a series that contains both audio tones and coloured squares together',
             'in this test, the same colours and tones are NOT paired and are entirely unrelated to eachother, although they are presented at the same time',
             'press enter if either the colour OR tone OR both matches the with the same two steps back']
    vstimlist=[];astimlist=[]
    vtarget=[0,0];atarget=[0,0]
    n=0

    #create two stimuli lists and mark down target trials
    for i in vseq:
        vstimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[aseq[n]],octave=4, sampleRate=44100, secs=dura,bits=8))
        #the line above throws an error, needs looking over again when I'm less tired...
        if n > nback_no-1:
            #if the event match with n events ago (n specified by 'nback_no')
            #mark it as a target trial
            if i==vseq[n-nback_no]:
                vtarget.append(1)
            else:
                vtarget.append(0)
            if aseq[n]==aseq[n-nback_no]:
                atarget.append(1)
            else:
                atarget.append(0)
        n = n+1
    infolooper(infoloop,window) #present basic test info for participant (what test, etc)
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    n=0
    #play/draw stimuli and record response time
    for vtrial in vstimlist:
        response=None; hit=None; time=None;mod=None;target=False
        vtrial.draw()
        astimlist[n].play()
        starttime=window.flip()
        #each stimulus is displayed for the duration specified
        response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= dura:
            pass
        #Currently only RT for catch trials will be recorded
        if vtarget[n]==1 or atarget[n]==1:
            hit=False;target=True
            if vtarget[n]==1:
                mod='visual'
            else:
                mod='auditory'
            if response!=None:
                time=response[0][1]-starttime
                hit=True
        window.flip()
        #output includes: condition, trial number, whether it's target, modality of target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s, %s\n'%('unpaired', n+1, target, str(mod), str(hit), str(time))])
        n = n+1
        core.wait(0.5)