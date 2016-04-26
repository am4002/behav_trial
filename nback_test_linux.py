# -*- coding: utf-8 -*-
"""
    collection of N-back tests to be preformed (linux version)
    
    TODO:
        
    Updated date:
        April 26
    CHANGED:
        add MEG trigger and receiving response
        measured the delay between audio & visual presentation is roughly 231-260 ms
        Fixed flickring on Interleaved condition in MEG
        No break in MEG session (Gary suggested)
"""
#imports
from psychopy import visual, sound, core, event,logging
sound.init(rate=44100, stereo=True, buffer=4096)
from random import randint, shuffle
from nback_helpers import infolooper
import numpy as np
#----------Comment out this line if not in MEG session; Change it back in MEG session-----------------
#import parallel #NB not psyhopy parallel



#Global variables
colorcode=['red','blue','green','yellow']
audicode=[233.2,277.2,329.6,392]


#a function that initiate MEG-related variables

def prepMEG():
    
    #Get parallel port object
    global pport_resp, pport_trig

    pport_resp = parallel.Parallel('/dev/parport1') #right hand box
    pport_resp.setDataDir(0) #0=read
    pport_resp.getData() #getData is the basic read command
        

    pport_trig = parallel.Parallel('/dev/parport0')    
    pport_trig.setDataDir(1) #1=write
    pport_trig.setData(0) #setData is the basic write command with a value
    
        
#test functions
def vNback (fi, seqFi, nback_no, window, seq, dura, inMEG=False, trial_no=None, adaptive=False): #visual nback test

    #data structures
    trigger=1
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    rest=visual.TextStim(window,'Well done! Have a break',color='white')

    infoloop=['Press return/enter to continue',
             'This is the visual 2-back test',
             'You will see a series of coloured squares',
             'Press L if the colour of a square matches the colour of a square two steps back']

    vpicture = visual.ImageStim(window,'visual.png',pos=(0,0))        
    
    stimlist=[]
    target=[0,0]
    n=0
    
    #create stimuli list and mark down target trials
    for i in seq: #create stimuli based on the sequence passed in function argument
        stimlist.append(visual.Rect(window,width=200.0,height=200.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        if n > nback_no-1:
            #if the event match with the one n events ago (n specified by 'nback_no')
            #mark it as a target trial
            if i==seq[n-nback_no]:
                target.append(1)
            else:
                target.append(0)
        n = n+1

    if inMEG == False:        
        infolooper(infoloop,window) #present basic test info for participant (what test, etc)
        window.flip()
    conditionTx=visual.TextStim(window,'Visual 2-back test', color=(1.0,1.0,1.0), pos=(0.0,300))
    conditionTx.draw()
    vpicture.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    # to give feedback on percentage correct, miss, false hit
    per_corr=[target.count(1),0,0]
    cross.setAutoDraw(True) 
        
    #draw stimuli and record response time
    for n, trial in enumerate(stimlist):
        response=None; hit=None; time=None
        trial.draw()
        starttime=window.flip()
        #sending trigger######################################
        if inMEG == True:
            if target[n]==1:
                pport_trig.setData( (trigger*2+1))
                print 'trigger %s UP' % str(trigger*2+1) 
            else:
                pport_trig.setData( ((trigger+1)*2+1))
                print 'trigger %s UP' % str((trigger+1)*2+1)

            # wait for a response from MEG####################
            # this only matters for getting the behavioral data to csv files
            ##pport_resp.Out32(pport_resp_addr, 0) # first, clear the line
            this_resp = 0
            # now wait for duration specified
            print 'wait for response'
            while (this_resp == 0) and ((logging.defaultClock.getTime() - starttime) <= dura):
                this_resp= int(pport_resp.getData())
            if this_resp != 0:
                response=np.array([[this_resp,logging.defaultClock.getTime()]])#log the response time
                print 'response %s is logged' 
            else:
                print 'no response'
            while(logging.defaultClock.getTime() - starttime) <= dura:
                pass
            print 'waiting ended'
            print (logging.defaultClock.getTime()-starttime)
            print (this_resp)
        else: #wait for a response from normal keyboard
            #each stimulus is presented for the duration specified
            response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
            while(logging.defaultClock.getTime() - starttime) <= dura:#making sure every event duration is the same no matter getting a key or not 
                pass
                
        #RT will be recorded despite of trial types
        if response!=None:
            if target[n]==1: #if target trials and get keypress, set 'hit' to true
                hit=True
            else: #if not target trials but get keypress, set 'hit' to false
                hit=False
            time=response[0][1]-starttime #record RT for any keypress
        if hit==True: #record response accuracy
            per_corr[1]=per_corr[1]+1
        elif hit==False:
            per_corr[2]=per_corr[2]+1
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('visual', n+1, str(target[n]==1), str(hit), str(time))]) #fix response 
        
        window.flip()
        if inMEG==True:
            pport_trig.setData( 0)#set all pin low
            print 'trigger set DOWN'
        core.wait(0.5)
        #q to quit        
        if event.getKeys(keyList=['q' ,'escape']):
            cross.setAutoDraw(False)
            sure=visual.TextStim(window,'Do you want to quit?',color='white')
            sure.draw()
            window.flip()
            pressed=event.waitKeys(keyList=None)
            if pressed[0]=='return':                
                print >> seqFi, 'Testing sequence, visual:  %s \n' % str(seq)
                window.close()
                core.quit()
            else:
                cross.setAutoDraw(True)
                pass;
        if inMEG==False: #During training session give the subject a break
            if n%50==0 and n!=0:
                cross.setAutoDraw(False)
                rest.draw()
                window.flip()
                core.wait(5.0)
                ready.draw()
                window.flip()
                event.waitKeys(keyList=['return'])
                cross.setAutoDraw(True)

    #feedback to the participants
    feedback=visual.TextStim(window,'Block completed\nYour result: '+
                             str(per_corr[1])+' out of '+str(per_corr[0])+' correct\n'+
                             str(per_corr[0]-per_corr[1])+' miss\n'+
                             str(per_corr[2])+' false hit', color=(1.0,1.0,1.0))
    cross.setAutoDraw(False)
    feedback.draw()
    window.flip()
    core.wait(4.0)
    
    print >> seqFi, 'Testing sequence, visual:  %s \n' % str(seq)
    print >> seqFi, str(per_corr[1])+' out of '+str(per_corr[0])+' correct'
    print >> seqFi, str(per_corr[0]-per_corr[1])+' miss'
    print >> seqFi, str(per_corr[2])+' false hit\n'
    fi.writerow([])
    
def aNback (fi, seqFi, nback_no, window, seq, dura, inMEG=False,trial_no=None, adaptive=False):#auditory n-back task

    #data structures
    trigger=3
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    rest=visual.TextStim(window,'Well done! Have a break',color='white')

    infoloop=['Press return/enter to continue',
             'This is the auditory 2-back test',
             'You will see a series of audio tones',
             'Press L if the tone played matches the tone two steps back']
    apicture = visual.ImageStim(window,'auditory.png',pos=(0,0))
    stimlist=[]
    target=[0,0]
    n=0

    #create stimuli list and mark down target trials
    for i in seq:
        stimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=dura,bits=32))
        if n > nback_no-1:
            #if the event match with the one n events ago (n specified by argument 'nback_no')
            #mark it as a target trial
            if i==seq[n-nback_no]:
                target.append(1)
            else:
                target.append(0)
        n = n+1

    if inMEG == False:        
        infolooper(infoloop,window) #present basic test info for participant (what test, etc)
        window.flip()
    conditionTx=visual.TextStim(window,'Auditory 2-back test', color=(1.0,1.0,1.0),pos=(0.0,300))
    conditionTx.draw()
    apicture.draw()
    window.flip()
    event.waitKeys(keyList=['return']) #present basic test info for participant (what test, etc)
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    per_corr=[target.count(1),0,0]
    cross.setAutoDraw(True)

    #play stimuli and record response time
    for n, trial in enumerate(stimlist):
        response=None; hit=None; time=None
        window.flip()
        trial.play()
        if inMEG ==True:
            window.multiFlip(15)
        
        #sending trigger######################################
        if inMEG == True:
            if target[n]==1:
                pport_trig.setData( (trigger*2+1))
                print 'trigger %s UP' % str(trigger*2+1)
            else:
                pport_trig.setData( ((trigger+1)*2+1))
                print 'trigger %s UP' % (str((trigger+1)*2+1))

        starttime=window.flip()
        if inMEG==True:
            # wait for a response from MEG####################
            # this only matters for getting the behavioral data to csv files
            
            #pport_resp.Out32(pport_resp_addr, 0) # first, clear the line
            this_resp = 0
            # now wait for duration specified
            print 'wait for response'
            while (this_resp ==0) and ((logging.defaultClock.getTime() - starttime) <= dura):
                this_resp= int(pport_resp.getData())
            if this_resp !=0:#need to be adjusted depending on which button the participant is using
                response=np.array([[this_resp,logging.defaultClock.getTime()]])#log the response time
                print 'response is logged'
            while(logging.defaultClock.getTime() - starttime) <= dura:
                pass
            print 'waiting ended'
            print (logging.defaultClock.getTime()-starttime)
            print (this_resp)
        else:
            #each stimulus is played for the duration specified
            response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
            while(logging.defaultClock.getTime() - starttime) <= dura:
                pass
                
        if response!=None:
            if target[n]==1: #if target trials aand get keypress, set 'hit' to true
                hit=True
            else: #if not target trials but get keypress, set 'hit' to false
                hit=False
            time=response[0][1]-starttime #record RT for any keypress
        if hit==True: #record response accuracy
            per_corr[1]=per_corr[1]+1
        elif hit==False:
            per_corr[2]=per_corr[2]+1
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('auditory', n+1, str(target[n]==1), str(hit), str(time))])
        window.flip()
        if inMEG==True:
            pport_trig.setData( 0) #set all pin low
            print 'trigger set DOWN'
        core.wait(0.5)
        #q to quit        
        if event.getKeys(keyList=['q' ,'escape']):
            cross.setAutoDraw(False)
            sure=visual.TextStim(window,'Do you want to quit?',color='white')
            sure.draw()
            window.flip()
            pressed=event.waitKeys(keyList=None)
            if pressed[0]=='return':
                print >> seqFi, 'Testing sequence, auditory:  %s \n' % str(seq)
                window.close()
                core.quit()
            else:
                cross.setAutoDraw(True)
                pass;        
        if inMEG==False:
            if n%50==0 and n!=0:
                cross.setAutoDraw(False)
                rest.draw()
                window.flip()
                core.wait(5.0)
                ready.draw()
                window.flip()
                event.waitKeys(keyList=['return'])
                cross.setAutoDraw(True)
        
    feedback=visual.TextStim(window,'Block completed\nYour result: '+
                             str(per_corr[1])+' out of '+str(per_corr[0])+' correct\n'+
                             str(per_corr[0]-per_corr[1])+' miss\n'+
                             str(per_corr[2])+' false hit', color=(1.0,1.0,1.0))
    cross.setAutoDraw(False)

    feedback.draw()
    window.flip()
    core.wait(4.0)
    print >> seqFi, 'Testing sequence, auditory:  %s \n' % str(seq)
    print >> seqFi, str(per_corr[1])+' out of '+str(per_corr[0])+' correct'
    print >> seqFi, str(per_corr[0]-per_corr[1])+' miss'
    print >> seqFi, str(per_corr[2])+' false hit\n'
    fi.writerow([])

#paired nback task
#Currently auditory sequence and visual sequence are exactly the same, though it may not be the best way
#think about this later
def nPaired (fi, seqFi, nback_no, window, seq, dura, inMEG=False, trial_no=None, adaptive=False):

    #data structures
    trigger=5
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    rest=visual.TextStim(window,'Well done! Have a break',color='white')

    infoloop=['Press return/enter to continue',
             'This is the paired 2-back test',
             'You will see a series that contains both audio tones and coloured squares together',
             'In this test, the same colour/tone pair is always presented together',
             'Press L if the colour/tone pair matches the pair two steps back']
             
    ppicture = visual.ImageStim(window,'paired.png',pos=(0,0))
    vstimlist=[];astimlist=[]
    target=[0,0]
    n=0

    #create two stimuli lists and mark down target trials
    for i in seq:
        vstimlist.append(visual.Rect(window,width=200.0,height=200.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))        
        astimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=dura,bits=32))
        if n > nback_no-1:
            #if the event match with n events ago (n specified by 'nback_no')
            #mark it as a target trial
            if i==seq[n-nback_no]:
                target.append(1)
            else:
                target.append(0)
        n = n+1

    if inMEG == False:        
        infolooper(infoloop,window) #present basic test info for participant (what test, etc)
        window.flip()
    conditionTx=visual.TextStim(window,'Paired 2-back test', color=(1.0,1.0,1.0),pos=(0.0,300))
    conditionTx.draw()
    ppicture.draw()
    window.flip()
    event.waitKeys(keyList=['return']) #present basic test info for participant (what test, etc)
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    per_corr=[target.count(1),0,0]
    cross.setAutoDraw(True)

    #play/draw stimuli and record response time
    for n, vtrial in enumerate(vstimlist):
        response=None; hit=None; time=None
        window.flip()
        astimlist[n].play()
        if inMEG ==True:
            window.multiFlip(15)
        vtrial.draw()
        #sending trigger######################################
        if inMEG == True:
            if target[n]==1:
                pport_trig.setData( (trigger*2+1))
            else:
                pport_trig.setData( ((trigger+1)*2+1))
            #print 'trigger set UP'
        starttime=window.flip()

        if inMEG==True:
        
            # wait for a response from MEG####################
            # this only matters for getting the behavioral data to csv files
            ## pport_resp.Out32(pport_resp_addr, 0) # first, clear the line
            this_resp = 0
            # now wait for duration specified
            #print 'wait for response'
            while (this_resp ==0) and ((logging.defaultClock.getTime() - starttime) <= dura):
                this_resp= int(pport_resp.getData())
            if this_resp != 0:#need to be adjusted depending on which button the participant is using
                response=np.array([[this_resp,logging.defaultClock.getTime()]])#log the response time
                #print 'response is logged'
            while(logging.defaultClock.getTime() - starttime) <= dura:
                pass
            #print 'waiting ended'
            #print (this_resp)
            #print (logging.defaultClock.getTime()-starttime)
        else: #wait for a response from normal keyboard
            #each stimulus is presented for the duration specified
            response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
            while(logging.defaultClock.getTime() - starttime) <= dura:#making sure every event duration is the same no matter getting a key or not 
                pass

        if response!=None:
            if target[n]==1: #if target trials and get keypress, set 'hit' to true
                hit=True
            else: #if not target trials but get keypress, set 'hit' to false
                hit=False
            time=response[0][1]-starttime #record RT for any keypress

        if hit==True: #record response accuracy
            per_corr[1]=per_corr[1]+1
        elif hit==False:
            per_corr[2]=per_corr[2]+1
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('paired', n+1, str(target[n]==1), str(hit), str(time))])
        window.flip()
        if inMEG==True:
            pport_trig.setData( 0)#set all pin low
            #print 'trigger set DOWN'
        core.wait(0.5)
        #q to quit        
        if event.getKeys(keyList=['q' ,'escape']):
            cross.setAutoDraw(False)
            sure=visual.TextStim(window,'Do you want to quit?',color='white')
            sure.draw()
            window.flip()
            pressed=event.waitKeys(keyList=None)
            if pressed[0]=='return':
                print >> seqFi, 'Testing sequence, paired:  %s \n' % str(seq)
                window.close()
                core.quit()
            else:
                cross.setAutoDraw(True)
                pass;        
        if inMEG==False:
            if n%50==0 and n!=0:
                cross.setAutoDraw(False)
                rest.draw()
                window.flip()
                core.wait(5.0)
                ready.draw()
                window.flip()
                event.waitKeys(keyList=['return'])
                cross.setAutoDraw(True)
            
    feedback=visual.TextStim(window,'Block completed\nYour result: '+
                             str(per_corr[1])+' out of '+str(per_corr[0])+' correct\n'+
                             str(per_corr[0]-per_corr[1])+' miss\n'+
                             str(per_corr[2])+' false hit', color=(1.0,1.0,1.0))
    cross.setAutoDraw(False)
    feedback.draw()
    window.flip()
    core.wait(4.0)
    print >> seqFi, 'Testing sequence, paired:  %s \n' % str(seq)
    print >> seqFi, str(per_corr[1])+' out of '+str(per_corr[0])+' correct'
    print >> seqFi, str(per_corr[0]-per_corr[1])+' miss'
    print >> seqFi, str(per_corr[2])+' false hit\n'
    fi.writerow([])


#visual distractor condition
def vDistractor (fi, seqFi, nback_no, window,  seq, dura, inMEG=False,trial_no=None, adaptive=False):

    #data structures
    trigger=9
    vseq = seq
    aseq = list(seq) #make auditory sequence different from visual one
    shuffle(aseq)
    trial_no=len(vseq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    rest=visual.TextStim(window,'Well done! Have a break',color='white')

    infoloop=['Press return/enter to continue',
             'This is the visual distractor 2-back test',
             'You will see a series that contains both audio tones and coloured squares together',
             'In this test, please only pay attention to the visual colour squares, and ignore the tones',
             'Press press L if the colour matches with the one two steps back']
    vdpicture = visual.ImageStim(window,'visual_distractor.png',pos=(0,0))
    vstimlist=[];astimlist=[]
    vtarget=[0,0];atarget=[0,0]
    n=0

    #create two stimuli lists and mark down target trials
    for i in vseq:
        vstimlist.append(visual.Rect(window,width=200.0,height=200.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[aseq[n]],octave=4, sampleRate=44100, secs=dura,bits=32))
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

    if inMEG == False:        
        infolooper(infoloop,window) #present basic test info for participant (what test, etc)
        window.flip()
    conditionTx=visual.TextStim(window,'Visual distractor 2-back test', color=(1.0,1.0,1.0),pos=(0.0,300))
    conditionTx.draw()
    vdpicture.draw()
    window.flip()
    event.waitKeys(keyList=['return']) #present basic test info for participant (what test, etc)
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    per_corr=[vtarget.count(1),0,0]
    cross.setAutoDraw(True)

    #play/draw stimuli and record response time
    for n,vtrial in enumerate(vstimlist):
        response=None; hit=None; time=None;target=False
        window.flip()
        astimlist[n].play() 
        if inMEG ==True:
            window.multiFlip(15)
        vtrial.draw()
        
        #sending trigger######################################
        if inMEG == True:
            if vtarget[n]==1:
                pport_trig.setData( (trigger*2+1))
            else:
                pport_trig.setData( ((trigger+1)*2+1))
            #print 'trigger set UP'
        starttime=window.flip()
        if inMEG==True:
        
            # wait for a response from MEG####################
            # this only matters for getting the behavioral data to csv files
            ##pport_resp.Out32(pport_resp_addr, 0) # first, clear the line
            this_resp = 0
            # now wait for duration specified
            #print 'wait for response'
            while (this_resp ==0) and ((logging.defaultClock.getTime() - starttime) <= dura):
                this_resp= int(pport_resp.getData())
            if this_resp !=0:#need to be adjusted depending on which button the participant is using
                response=np.array([[this_resp,logging.defaultClock.getTime()]])#log the response time
                #print 'response is logged'
            while(logging.defaultClock.getTime() - starttime) <= dura:
                pass
            #print 'waiting ended'
            #print (logging.defaultClock.getTime()-starttime)
            #print (this_resp)
        else: #wait for a response from normal keyboard
            #each stimulus is presented for the duration specified
            response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
            while(logging.defaultClock.getTime() - starttime) <= dura:#making sure every event duration is the same no matter getting a key or not 
                pass
                
        if response!=None:
            if vtarget[n]==1: #if target trials and get keypress, set 'hit' and 'target' to true
                hit=True;target=True
                per_corr[1]=per_corr[1]+1
            else: #if not target trials but get keypress, set 'hit' and 'target' to false
                hit=False;target=False
                per_corr[2]=per_corr[2]+1
            time=response[0][1]-starttime #record RT for any keypress
        else: #if no keypress, mark down trial type
            if vtarget[n]==1:
                target=True

        window.flip()
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('vDistractor ', n+1, target, str(hit), str(time))])
        if inMEG==True:
            pport_trig.setData( 0)#set all pin low
            #print 'trigger set DOWN'
        core.wait(0.5)
        #q to quit        
        if event.getKeys(keyList=['q' ,'escape']):
            cross.setAutoDraw(False)
            sure=visual.TextStim(window,'Do you want to quit?',color='white')
            sure.draw()
            window.flip()
            pressed=event.waitKeys(keyList=None)
            if pressed[0]=='return':
                print >> seqFi, 'Testing sequence, visual distractor, visual:  %s \n' % str(vseq)
                print >> seqFi, 'Testing sequence, visual distractor, auditory:  %s \n' % str(aseq)
                window.close()
                core.quit()
            else:
                cross.setAutoDraw(True)
                pass;        
        if inMEG==False:
            if n%50==0 and n!=0:
                cross.setAutoDraw(False)
                rest.draw()
                window.flip()
                core.wait(5.0)
                ready.draw()
                window.flip()
                event.waitKeys(keyList=['return'])
                cross.setAutoDraw(True)
    feedback=visual.TextStim(window,'Block completed\nYour result: '+
                             str(per_corr[1])+' out of '+str(per_corr[0])+' correct in visual sequence\n'+
                             str(per_corr[0]-per_corr[1])+' miss\n'+
                             str(per_corr[2])+' false hit', color=(1.0,1.0,1.0))
    cross.setAutoDraw(False)
    feedback.draw()
    window.flip()
    core.wait(2.0)
    print >> seqFi, 'Testing sequence, visual distractor, visual:  %s \n' % str(vseq)
    print >> seqFi, 'Testing sequence, visual distractor, auditory:  %s \n' % str(aseq)
    print >> seqFi, str(per_corr[1])+' out of '+str(per_corr[0])+' correct'
    print >> seqFi, str(per_corr[0]-per_corr[1])+' miss'
    print >> seqFi, str(per_corr[2])+' false hit\n'
    fi.writerow([])
   
   
#Auditory distractor condition
def aDistractor (fi, seqFi, nback_no, window,  seq, dura, inMEG=False, trial_no=None, adaptive=False):

    #data structures
    trigger=11
    vseq = seq
    aseq = list(seq) #make auditory sequence different from visual one
    shuffle(aseq)
    trial_no=len(vseq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    rest=visual.TextStim(window,'Well done! Have a break',color='white')

    infoloop=['Press return/enter to continue',
             'This is the auditory distractor 2-back test',
             'You will see a series that contains both audio tones and coloured squares together',
             'In this test, please only pay attention to the audio tones, and ignore the coloured squares',
             'Press press L if the tone matches with the one two steps back']
    adpicture = visual.ImageStim(window,'auditory_distractor.png',pos=(0,0))         
    vstimlist=[];astimlist=[]
    vtarget=[0,0];atarget=[0,0]
    n=0

    #create two stimuli lists and mark down target trials
    for i in vseq:
        vstimlist.append(visual.Rect(window,width=200.0,height=200.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[aseq[n]],octave=4, sampleRate=44100, secs=dura,bits=32))
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


    if inMEG == False:        
        infolooper(infoloop,window) #present basic test info for participant (what test, etc)
        window.flip()
    conditionTx=visual.TextStim(window,'Auditory distractor 2-back test', color=(1.0,1.0,1.0),pos=(0.0,300))
    conditionTx.draw()
    adpicture.draw()
    window.flip()
    event.waitKeys(keyList=['return']) #present basic test info for participant (what test, etc)
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    per_corr=[atarget.count(1),0,0]
    cross.setAutoDraw(True)
    #play/draw stimuli and record response time
    for n, vtrial in enumerate(vstimlist):
        response=None; hit=None; time=None;target=False
        window.flip()
        astimlist[n].play()
        if inMEG ==True:
            window.multiFlip(15)
        vtrial.draw()

        #sending trigger######################################
        if inMEG == True:
            if atarget[n]==1:
                pport_trig.setData( (trigger*2+1))
            else:
                pport_trig.setData( ((trigger+1)*2+1))
            #print 'trigger set UP'
        starttime=window.flip()
        
        if inMEG==True:

            # wait for a response from MEG####################
            # this only matters for getting the behavioral data to csv files
            ##pport_resp.Out32(pport_resp_addr, 0) # first, clear the line
            this_resp = 0
            # now wait for duration specified
            #print 'wait for response'
            while (this_resp ==0) and ((logging.defaultClock.getTime() - starttime) <= dura):
                this_resp= int(pport_resp.getData())
            if this_resp !=0:#need to be adjusted depending on which button the participant is using
                response=np.array([[this_resp,logging.defaultClock.getTime()]])#log the response time
                #print 'response is logged'
            while(logging.defaultClock.getTime() - starttime) <= dura:
                pass
            #print 'waiting ended'
            #print (logging.defaultClock.getTime()-starttime)
            #print (this_resp)
        else: #wait for a response from normal keyboard
            #each stimulus is presented for the duration specified
            response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
            while(logging.defaultClock.getTime() - starttime) <= dura:#making sure every event duration is the same no matter getting a key or not 
                pass

        if response!=None:
            if atarget[n]==1: #if target trials and get keypress, set 'hit' and 'target' to true
                hit=True;target=True
                per_corr[1]=per_corr[1]+1
            else: #if not target trials but get keypress, set 'hit' and 'target' to false
                hit=False;target=False
                per_corr[2]=per_corr[2]+1
            time=response[0][1]-starttime #record RT for any keypress
        else: #if no keypress, mark down trial type
            if atarget[n]==1:
                target=True

        window.flip()
        #output includes: condition, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('aDistractor ', n+1, target, str(hit), str(time))])
        if inMEG==True:
            pport_trig.setData( 0)#set all pin low
            #print 'trigger set DOWN'
        core.wait(0.5)
        #q to quit        
        if event.getKeys(keyList=['q' ,'escape']):
            cross.setAutoDraw(False)
            sure=visual.TextStim(window,'Do you want to quit?',color='white')
            sure.draw()
            window.flip()
            pressed=event.waitKeys(keyList=None)
            if pressed[0]=='return':
                print >> seqFi, 'Testing sequence, auditory distractor, visual:  %s \n' % str(vseq)
                print >> seqFi, 'Testing sequence, auditory distractor, auditory:  %s \n' % str(aseq)
                window.close()
                core.quit()
            else:
                cross.setAutoDraw(True)
                pass;        
        if inMEG==False:
            if n%50==0 and n!=0:
                cross.setAutoDraw(False)
                rest.draw()
                window.flip()
                core.wait(5.0)
                ready.draw()
                window.flip()
                event.waitKeys(keyList=['return'])
                cross.setAutoDraw(True)
            
    feedback=visual.TextStim(window,'Block completed\nYour result: '+
                             str(per_corr[1])+' out of '+str(per_corr[0])+' correct in audio sequence\n'+
                             str(per_corr[0]-per_corr[1])+' miss\n'+
                             str(per_corr[2])+' false hit', color=(1.0,1.0,1.0))
    cross.setAutoDraw(False)
    feedback.draw()
    window.flip()
    core.wait(4.0)
    print >> seqFi, 'Testing sequence, auditory distractor, visual:  %s \n' % str(vseq)
    print >> seqFi, 'Testing sequence, auditory distractor, auditory:  %s \n' % str(aseq)
    print >> seqFi, str(per_corr[1])+' out of '+str(per_corr[0])+' correct'
    print >> seqFi, str(per_corr[0]-per_corr[1])+' miss'
    print >> seqFi, str(per_corr[2])+' false hit\n'
    fi.writerow([])
   

def betweenInterleaved (fi, seqFi, nback_no, window, seq, dura, inMEG=False,trial_no=None, adaptive=False):

    #data structures
    trigger=15
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    rest=visual.TextStim(window,'Well done! Have a break',color='white')

    infoloop=['Press return/enter to continue',
             'This is the bewteen-modality interleaved 2-back test',
             'You will see a series that contains both audio tones and coloured squares SEPARATELY',
             'Press L if the tone played matches the associated colour two steps back, or vice versa']
    bipicture = visual.ImageStim(window,'interleaved.png',pos=(0,0))
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
            stimlist.append(visual.Rect(window,width=200.0,height=200.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        else:
            stimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=dura,bits=32))
        n=n+1

    if inMEG == False:        
        infolooper(infoloop,window) #present basic test info for participant (what test, etc)
        window.flip()
    conditionTx=visual.TextStim(window,'Audio-visual interleaved 2-back test', color=(1.0,1.0,1.0),pos=(0.0,300))
    conditionTx.draw()
    bipicture.draw()
    window.flip()
    event.waitKeys(keyList=['return']) #present basic test info for participant (what test, etc)
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    mod=None
    per_corr=[target.count(1),0,0]
    cross.setAutoDraw(True)
    #play/draw stimuli and record response time
    for n, trial in enumerate(stimlist):
        response=None; hit=None; time=None
        window.flip()        
        
        if modality[n]==False:
            trial.play()
            mod='auditory'
        if inMEG ==True:
            window.multiFlip(15)
        if modality[n]==True:
            trial.draw()
            mod='visual'
        #sending trigger######################################
        if inMEG == True:
            if target[n]==1:
                pport_trig.setData( (trigger*2+1))
            else:
                pport_trig.setData( ((trigger+1)*2+1))
            #print 'trigger set UP'


        starttime=window.flip()
        if inMEG==True:
            # wait for a response from MEG####################
            # this only matters for getting the behavioral data to csv files
            ##pport_resp.Out32(pport_resp_addr, 0) # first, clear the line
            this_resp = 0
            # now wait for duration specified
            #print 'wait for response'
            while (this_resp ==0) and ((logging.defaultClock.getTime() - starttime) <= dura):
                this_resp= int(pport_resp.getData())
            if this_resp !=0:#need to be adjusted depending on which button the participant is using
                response=np.array([[this_resp,logging.defaultClock.getTime()]])#log the response time
                #print 'response is logged'
            while(logging.defaultClock.getTime() - starttime) <= dura:
                pass
            #print 'waiting ended'
            #print (logging.defaultClock.getTime()-starttime)
            #print (this_resp)
        else: #wait for a response from normal keyboard
            #each stimulus is presented for the duration specified
            response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
            while(logging.defaultClock.getTime() - starttime) <= dura:#making sure every event duration is the same no matter getting a key or not 
                pass

        if response!=None:
            if target[n]==1: #if target trials and get keypress, set 'hit' to true
                hit=True
            else: #if not target trials but get keypress, set 'hit' to false
                hit=False
            time=response[0][1]-starttime #record RT for any keypress
        if hit==True: #record response accuracy
            per_corr[1]=per_corr[1]+1
        elif hit==False:
            per_corr[2]=per_corr[2]+1
        #output includes: condition, modality, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('betweenInterleaved '+mod, n+1, str(target[n]==1), str(hit), str(time))])
        window.flip()
        if inMEG==True:
            pport_trig.setData( 0)#set all pin low
            #print 'trigger set DOWN'
        core.wait(0.5)
        #q to quit        
        if event.getKeys(keyList=['q' ,'escape']):
            cross.setAutoDraw(False)
            sure=visual.TextStim(window,'Do you want to quit?',color='white')
            sure.draw()
            window.flip()
            pressed=event.waitKeys(keyList=None)
            if pressed[0]=='return':
                print >> seqFi, 'Testing sequence, between interleaved:  %s \n' % str(seq)
                window.close()
                core.quit()
            else:
                cross.setAutoDraw(True)
                pass;        
        if inMEG==False:
            if n%50==0 and n!=0:
                cross.setAutoDraw(False)
                rest.draw()
                window.flip()
                core.wait(5.0)
                ready.draw()
                window.flip()
                event.waitKeys(keyList=['return'])
                cross.setAutoDraw(True)
    feedback=visual.TextStim(window,'Block completed\nYour result: '+
                             str(per_corr[1])+' out of '+str(per_corr[0])+' correct\n'+
                             str(per_corr[0]-per_corr[1])+' miss\n'+
                             str(per_corr[2])+' false hit', color=(1.0,1.0,1.0))
    cross.setAutoDraw(False)
    feedback.draw()
    window.flip()
    core.wait(4.0)
    print >> seqFi, 'Testing sequence, between interleaved:  %s \n' % str(seq)
    print >> seqFi, str(per_corr[1])+' out of '+str(per_corr[0])+' correct'
    print >> seqFi, str(per_corr[0]-per_corr[1])+' miss'
    print >> seqFi, str(per_corr[2])+' false hit\n'
    fi.writerow([])

#Conditions not used for this experiment
#unpaired nback task
def nUnpaired (fi, seqFi, nback_no, window,  seq, dura,inMEG=False, trial_no=None, adaptive=False):

    #data structures
    trigger=7
    vseq = seq
    aseq = list(seq)
    shuffle(aseq)
    trial_no=len(vseq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    infoloop=['Press return/enter to continue',
             'This is the unpaired 2-back test',
             'You will see a series that contains both audio tones and coloured squares together',
             'In this test, the same colours and tones are NOT paired and are entirely unrelated to eachother, although they are presented at the same time',
             'Press L if either the colour OR tone OR both matches the with the same two steps back']
    uppicture = visual.ImageStim(window,'unpaired_dual_back.png',pos=(0,0))
    vstimlist=[];astimlist=[]
    vtarget=[0,0];atarget=[0,0]
    n=0

    #create two stimuli lists and mark down target trials
    for i in vseq:
        vstimlist.append(visual.Rect(window,width=200.0,height=200.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        astimlist.append(sound.Sound(audicode[aseq[n]],octave=4, sampleRate=44100, secs=dura,bits=32))
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
    conditionTx=visual.TextStim(window,'Unpaired dual 2-back test', color=(1.0,1.0,1.0))
    conditionTx.draw()
    window.flip()
    event.waitKeys(keyList='return')
    if inMEG == False:        
        infolooper(infoloop,window) #present basic test info for participant (what test, etc)
    window.flip()
    uppicture.draw()
    window.flip()
    event.waitKeys(keyList=['return']) #present basic test info for participant (what test, etc)
    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    per_corr=[vtarget.count(1),0,atarget.count(1),0,0]
    cross.setAutoDraw(True)
    #play/draw stimuli and record response time
    for n, vtrial in enumerate(vstimlist):
        response=None; hit=None; time=None;mod=None;target=False
        vtrial.draw()
        starttime=window.flip()
        #sending trigger######################################
        if inMEG == True:
            if vtarget[n]==1 or atarget[n]==1:
                pport_trig.setData( (trigger*2+1))
            else:
                pport_trig.setData( ((trigger+1)*2+1))
            #print 'trigger set UP'
        astimlist[n].play()
        
        if inMEG==True:
            # wait for a response from MEG####################
            # this only matters for getting the behavioral data to csv files
            ##pport_resp.Out32(pport_resp_addr, 0) # first, clear the line
            this_resp = 0
            # now wait for duration specified
            #print 'wait for response'
            while (this_resp ==0) and ((logging.defaultClock.getTime() - starttime) <= dura):
                this_resp= int(pport_resp.getData())
            if this_resp !=0:#need to be adjusted depending on which button the participant is using
                response=np.array([[this_resp,logging.defaultClock.getTime()]])#log the response time
                #print 'response is logged'
            while(logging.defaultClock.getTime() - starttime) <= dura:
                pass
            #print 'waiting ended'
            #print (this_resp)
            #print (logging.defaultClock.getTime()-starttime)
        else: #wait for a response from normal keyboard
            #each stimulus is presented for the duration specified
            response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
            while(logging.defaultClock.getTime() - starttime) <= dura:#making sure every event duration is the same no matter getting a key or not 
                pass
                
        if response!=None:
            if vtarget[n]==1 or atarget[n]==1: #if target trials and get keypress, set 'hit' and 'target' to true
                hit=True;target=True
                if vtarget[n]==1: #record which modality the target is in
                    mod='visual'
                    per_corr[1]=per_corr[1]+1
                else:
                    mod='auditory'
                    per_corr[3]=per_corr[3]+1
            else: #if not target trials but get keypress, set 'hit' and 'target' to false
                hit=False;target=False
                per_corr[4]=per_corr[4]+1
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
        if inMEG==True:
            pport_trig.setData( 0)#set all pin low
            #print 'trigger set DOWN'        
        core.wait(0.5)

    feedback=visual.TextStim(window,'Block completed\nYour result: '+
                             str(per_corr[1])+' out of '+str(per_corr[0])+' correct in visual sequence\n'+
                             str(per_corr[3])+' out of '+str(per_corr[2])+' correct in audio sequence\n'+
                             str(per_corr[0]-per_corr[1])+' miss in visual sequence\n'+
                             str(per_corr[2]-per_corr[3])+' miss in audio sequence\n'+
                             str(per_corr[4])+' false hit', color=(1.0,1.0,1.0))
    cross.setAutoDraw(False)
    feedback.draw()
    window.flip()
    core.wait(5.0)
    print >> seqFi, 'Testing sequence, unpaired, visual:  %s \n' % str(vseq)
    print >> seqFi, 'Testing sequence, unpaired, auditory:  %s \n' % str(aseq)
    fi.writerow([])


# a-a/v-v interleaved condition
def withinInterleaved (fi, seqFi, nback_no, window, seq, dura, inMEG=False, trial_no=None, adaptive=False):

    #data structures
    trigger= 13
    trial_no=len(seq)
    ready=visual.TextStim(window,'ready?', color=(1.0,1.0,1.0))
    cross=visual.TextStim(window,'+',color='white')
    infoloop=['Press return/enter to continue',
             'This is the within-modality interleaved 2-back test',
             'You will see a series that contains both audio tones and coloured squares SEPARATELY',
             'Press L if the tone played matches the tone two steps back, or if the colour matches the colour 2 steps back']
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
            stimlist.append(visual.Rect(window,width=200.0,height=200.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
        else:
            stimlist.append(sound.Sound(audicode[i],octave=4, sampleRate=44100, secs=dura,bits=32))
        n=n+1
        
    infolooper(infoloop,window) #present basic test info for participant (what test, etc)

    ready.draw()
    window.flip()
    event.waitKeys(keyList=['return'])
    mod=None
    per_corr=[target.count(1),0,0]
    cross.setAutoDraw(True)
    #play/draw stimuli and record response time
    for n, trial in enumerate(stimlist):
        response=None; hit=None; time=None
        if modality[n]==True:
            trial.draw()
            mod='visual'
        starttime=window.flip()
        
        #sending trigger######################################
        if inMEG == True:
            if target[n]==1:
                pport_trig.setData( (trigger*2+1))
            else:
                pport_trig.setData( ((trigger+1)*2+1))
            #print 'trigger set UP'

        if modality[n]==False:
            trial.play()
            mod='auditory'
        if inMEG==True:

            # wait for a response from MEG####################
            # this only matters for getting the behavioral data to csv files
            ##pport_resp.Out32(pport_resp_addr, 0) # first, clear the line
            this_resp = 0
            # now wait for duration specified
            #print 'wait for response'
            while (this_resp ==0) and ((logging.defaultClock.getTime() - starttime) <= dura):
                this_resp= int(pport_resp.getData())
            if this_resp !=0:#need to be adjusted depending on which button the participant is using
                response=np.array([[this_resp,logging.defaultClock.getTime()]])#log the response time
                #print 'response is logged'
            while(logging.defaultClock.getTime() - starttime) <= dura:
                pass
            #print 'waiting ended'
            #print (logging.defaultClock.getTime()-starttime)
            #print (this_resp)
        else: #wait for a response from normal keyboard
            #each stimulus is presented for the duration specified
            response=event.waitKeys(maxWait=dura-(1/120.0),keyList=['l'],timeStamped=True)
            while(logging.defaultClock.getTime() - starttime) <= dura:#making sure every event duration is the same no matter getting a key or not 
                pass
        
        if response!=None:
            if target[n]==1: #if target trials and get keypress, set 'hit' to true
                hit=True
                per_corr[1]=per_corr[1]+1
            else: #if not target trials but get keypress, set 'hit' to false
                hit=False
                per_corr[2]=per_corr[2]+1
            time=response[0][1]-starttime #record RT for any keypress
        #output includes: condition, modality, trial number, whether it's target, whether a hit, RT
        fi.writerow(['%s, %d, %s, %s, %s\n'%('withinInterleaved '+mod, n+1, str(target[n]==1), str(hit), str(time))])
        window.flip()

        if inMEG==True:
            pport_trig.setData( 0)#set all pin low
            #print 'trigger set DOWN'
        core.wait(0.5)
    feedback=visual.TextStim(window,'Block completed\nYour result: '+
                             str(per_corr[1])+' out of '+str(per_corr[0])+' correct\n'+
                             str(per_corr[0]-per_corr[1])+' miss\n'+
                             str(per_corr[2])+' false hit', color=(1.0,1.0,1.0))
    cross.setAutoDraw(False)
    feedback.draw()
    window.flip()
    core.wait(4.0)
    print >> seqFi, 'Testing sequence, within interleaved:  %s \n' % str(seq)
    fi.writerow([])