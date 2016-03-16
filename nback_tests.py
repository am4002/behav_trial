# -*- coding: utf-8 -*-
"""
    collection of N-back tests to be preformed
    
    TODO:
    +cheSeq function
    +association presentor

    CHANGED:
        duration is 0.5s now
        seqence is written into output file
        +3 more conditions
"""


#imports
from psychopy import visual, sound, core, event,logging
from random import randint, shuffle

#helper functions
def infolooper(infoloop,window): #this function loops through a list of strings for presenting test specific info to participants
    for datum in infoloop: 
        infLin=visual.TextStim(window,datum, color=(1.0,1.0,1.0),alignVert='center',alignHoriz='center') #make a text stimuli
        infLin.draw() #draw stimuli
        window.flip() #flip the window
        event.waitKeys(keyList=['return']) #wait for the subject to press return to move to the next piece of info

#test functions
def vNback (fi, nback_no, window, seq, trial_no=None, adaptive=False, duration=0.5): #visual nback test
    
    #data structures
    colorcode=['red','blue','green','yellow']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    infoloop=['Press return/enter to continue',
             'This is the visual 2-back test',
             'You will see a series of coloured squares',
             'Press L if the colour of a square matches the colour of a square two steps back']
    stimlist=[]
    target=[0,0]
    n=0
    
    #create stimuli list and mark down target trials
    for i in seq: #create stimuli based on the sequence passed in function argument
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
        #each stimulus is presented for the duration specified
        response=event.waitKeys(maxWait=duration-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= duration:
            pass
        #RT will be recorded despite of trail types
        if response!=None:
            if target[n]==1: #if target trials abd get keypress, set 'hit' to true
                hit=True
            else: #if not target trials but get keypress, set 'hit' to false
                hit=False
            time=response[0][1]-starttime #record RT for any keypress
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('visual', n+1, str(target[n]==1), str(hit), str(time))])
        n = n+1
        window.flip()
        core.wait(0.3)
    
    fi.writerow(['Testing sequence: ', seq])
    fi.writerow([])
    
def aNback (fi, nback_no, window, seq, trial_no=None, adaptive=False, duration=0.5):
    
    #data structures
    audicode=['C','D','E','F']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    infoloop=['Press return/enter to continue',
             'This is the auditory 2-back test',
             'You will see a series of audio tones',
             'Press L if the tone played matches the tone two steps back']
    stimlist=[]
    target=[0,0]
    n=0

    #create stimuli list and mark down target trials
    for i in seq:
        stimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=duration,bits=8))
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
        response=event.waitKeys(maxWait=duration-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= duration:
            pass
        if response!=None:
            if target[n]==1: #if target trials abd get keypress, set 'hit' to true
                hit=True
            else: #if not target trials but get keypress, set 'hit' to false
                hit=False
            time=response[0][1]-starttime #record RT for any keypress
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('auditory', n+1, str(target[n]==1), str(hit), str(time))])
        n = n+1
        window.flip()
        core.wait(0.5)
    fi.writerow(['Testing sequence ', seq])
    fi.writerow([])

    
def betweenInterleaved (fi, nback_no, window, seq, trial_no=None, adaptive=False, duration=0.5):

    #data structures
    audicode=['C','D','E','F']
    colorcode=['red','blue','green','yellow']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    infoloop=['Press return/enter to continue',
             'This is the bewteen-modality interleaved 2-back test',
             'You will see a series that contains both audio tones and coloured squares SEPARATELY',
             'Press L if the tone played matches the associated colour two steps back, or vice versa']
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
                #the event it matches to from DIFFERENT modalities
                if modality[n]==modality[n-nback_no]:
                    modality[n]=not modality[n]
            else:
                target.append(0)
        # create stimlist with two modalities
        if modality[n]==True:
            stimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        else:
            stimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=duration,bits=8))
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
        response=event.waitKeys(maxWait=duration-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= duration:
            pass
        if response!=None:
            if target[n]==1: #if target trials and get keypress, set 'hit' to true
                hit=True
            else: #if not target trials but get keypress, set 'hit' to false
                hit=False
            time=response[0][1]-starttime #record RT for any keypress
        #output includes: condition, modality, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('betweenInterleaved '+mod, n+1, str(target[n]==1), str(hit), str(time))])
        n = n+1
        window.flip()
        core.wait(0.5)
    
    fi.writerow(['Testing sequence ', seq])
    fi.writerow([])


#paired nback task
#Currently auditory sequence and visual sequence are exactly the same, though it may not be the best way
#think about this later
def nPaired (fi, nback_no, window, seq, trial_no=None, adaptive=False, duration=0.5):

    #data structures
    audicode=['C','D','E','F']
    colorcode=['red','blue','green','yellow']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    infoloop=['Press return/enter to continue',
             'This is the paired 2-back test',
             'You will see a series that contains both audio tones and coloured squares together',
             'In this test, the same colour/tone pair is always presented together',
             'Press L if the colour/tone pair matches the pair two steps back']
    vstimlist=[];astimlist=[]
    target=[0,0]
    n=0

    #create two stimuli lists and mark down target trials
    for i in seq:
        vstimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=duration,bits=8))
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
        response=event.waitKeys(maxWait=duration-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= duration:
            pass
        if response!=None:
            if target[n]==1: #if target trials and get keypress, set 'hit' to true
                hit=True
            else: #if not target trials but get keypress, set 'hit' to false
                hit=False
            time=response[0][1]-starttime #record RT for any keypress

        window.flip()

#output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('paired', n+1, str(target[n]==1), str(hit), str(time))])
        n = n+1
        core.wait(0.5)
    
    fi.writerow(['Testing sequence ', seq])
    fi.writerow([])

#unpaired nback task
def nUnpaired (fi, nback_no, window,  seq, trial_no=None, adaptive=False, duration=0.5):

    #data structures
    audicode=['C','D','E','F']
    colorcode=['red','blue','green','yellow']
    vseq = seq
    aseq = list(seq)
    shuffle(aseq)
    trial_no=len(vseq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    infoloop=['Press return/enter to continue',
             'This is the unpaired 2-back test',
             'You will see a series that contains both audio tones and coloured squares together',
             'In this test, the same colours and tones are NOT paired and are entirely unrelated to eachother, although they are presented at the same time',
             'Press L if either the colour OR tone OR both matches the with the same two steps back']
    vstimlist=[];astimlist=[]
    vtarget=[0,0];atarget=[0,0]
    n=0

    #create two stimuli lists and mark down target trials
    for i in vseq:
        vstimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[aseq[n]],octave=4, sampleRate=44100, secs=duration,bits=8))
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
        response=event.waitKeys(maxWait=duration-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= duration:
            pass
        if response!=None:
            if vtarget[n]==1 or atarget[n]==1: #if target trials and get keypress, set 'hit' and 'target' to true
                hit=True;target=True
                if vtarget[n]==1: #record which modality the target is in
                    mod='visual'
                else:
                    mod='auditory'
            else: #if not target trials but get keypress, set 'hit' and 'target' to false
                hit=False;target=False
            time=response[0][1]-starttime #record RT for any keypress
        else: #if no keypress, mark down trial type
            if vtarget[n]==1 or atarget[n]==1: 
                target=True
                if vtarget[n]==1: 
                    mod='visual'
                else:
                    mod='auditory'
        window.flip()
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('unpaired '+str(mod), n+1, target, str(hit), str(time))])
        n = n+1
        core.wait(0.5)
    fi.writerow(['Visual sequence ', vseq])
    fi.writerow(['Auditory sequence ', aseq])
    fi.writerow([])


#visual distractor condition
def vDistractor (fi, nback_no, window,  seq, trial_no=None, adaptive=False, duration=0.5):

    #data structures
    audicode=['C','D','E','F']
    colorcode=['red','blue','green','yellow']
    vseq = seq
    aseq = list(seq) #make auditory sequence different from visual one
    shuffle(aseq)
    trial_no=len(vseq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    infoloop=['Press return/enter to continue',
             'This is the visual distractor 2-back test',
             'You will see a series that contains both audio tones and coloured squares together',
             'In this test, please only pay attention to the visual colour squares, and ignore the tones',
             'Press press L if the colour matches with the one two steps back']
    vstimlist=[];astimlist=[]
    vtarget=[0,0];atarget=[0,0]
    n=0

    #create two stimuli lists and mark down target trials
    for i in vseq:
        vstimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[aseq[n]],octave=4, sampleRate=44100, secs=duration,bits=8))
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
        response=None; hit=None; time=None;target=False
        vtrial.draw()
        astimlist[n].play()
        starttime=window.flip()
        #each stimulus is displayed for the duration specified
        response=event.waitKeys(maxWait=duration-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= duration:
            pass
        if response!=None:
            if vtarget[n]==1: #if target trials and get keypress, set 'hit' and 'target' to true
                hit=True;target=True
            else: #if not target trials but get keypress, set 'hit' and 'target' to false
                hit=False;target=False
            time=response[0][1]-starttime #record RT for any keypress
        else: #if no keypress, mark down trial type
            if vtarget[n]==1:
                target=True

        window.flip()
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('vDistractor ', n+1, target, str(hit), str(time))])
        n = n+1
        core.wait(0.5)
    fi.writerow(['Visual sequence ', vseq])
    fi.writerow(['Auditory sequence ', aseq])
    fi.writerow([])
   
   
#Auditory distractor condition
def aDistractor (fi, nback_no, window,  seq, trial_no=None, adaptive=False, duration=0.5):

    #data structures
    audicode=['C','D','E','F']
    colorcode=['red','blue','green','yellow']
    vseq = seq
    aseq = list(seq) #make auditory sequence different from visual one
    shuffle(aseq)
    trial_no=len(vseq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    infoloop=['Press return/enter to continue',
             'This is the auditory distractor 2-back test',
             'You will see a series that contains both audio tones and coloured squares together',
             'In this test, please only pay attention to the audio tones, and ignore the coloured squares',
             'Press press L if the tone matches with the one two steps back']
    vstimlist=[];astimlist=[]
    vtarget=[0,0];atarget=[0,0]
    n=0

    #create two stimuli lists and mark down target trials
    for i in vseq:
        vstimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[aseq[n]],octave=4, sampleRate=44100, secs=duration,bits=8))
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
        response=None; hit=None; time=None;target=False
        vtrial.draw()
        astimlist[n].play()
        starttime=window.flip()
        #each stimulus is displayed for the duration specified
        response=event.waitKeys(maxWait=duration-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= duration:
            pass
        if response!=None:
            if atarget[n]==1: #if target trials and get keypress, set 'hit' and 'target' to true
                hit=True;target=True
            else: #if not target trials but get keypress, set 'hit' and 'target' to false
                hit=False;target=False
            time=response[0][1]-starttime #record RT for any keypress
        else: #if no keypress, mark down trial type
            if atarget[n]==1:
                target=True

        window.flip()
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('aDistractor ', n+1, target, str(hit), str(time))])
        n = n+1
        core.wait(0.5)
    fi.writerow(['Visual sequence ', vseq])
    fi.writerow(['Auditory sequence ', aseq])
    fi.writerow([])
   
   
# a-a/v-v interleaved condition
def withinInterleaved (fi, nback_no, window, seq, trial_no=None, adaptive=False, duration=0.5):

    #data structures
    audicode=['C','D','E','F']
    colorcode=['red','blue','green','yellow']
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    infoloop=['Press return/enter to continue',
             'This is the within-modality interleaved 2-back test',
             'You will see a series that contains both audio tones and coloured squares SEPARATELY',
             'Press L if the tone played matches the tone two steps back, or if the colour matches the colour two steps back']
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
                #the event it matches to from the SAME modality
                if modality[n]!=modality[n-nback_no]:
                    modality[n]=not modality[n]
            else:
                target.append(0)
        # create stimlist with two modalities
        if modality[n]==True:
            stimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        else:
            stimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=duration,bits=8))
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
        response=event.waitKeys(maxWait=duration-(1/120.0),keyList=['l'],timeStamped=True)
        while(logging.defaultClock.getTime() - starttime) <= duration:
            pass
        if response!=None:
            if target[n]==1: #if target trials and get keypress, set 'hit' to true
                hit=True
            else: #if not target trials but get keypress, set 'hit' to false
                hit=False
            time=response[0][1]-starttime #record RT for any keypress
        #output includes: condition, modality, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('withinInterleaved '+mod, n+1, str(target[n]==1), str(hit), str(time))])
        n = n+1
        window.flip()
        core.wait(0.5)
    
    fi.writerow(['Testing sequence ', seq])
    fi.writerow([])