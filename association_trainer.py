# -*- coding: utf-8 -*-
"""
TODO:
    +comments:(
"""
#imports
from psychopy import visual, sound, core,event
from nback_tests import infolooper
from random import randint,shuffle

wnd = visual.Window([1024,768],fullscr=False,allowGUI=False,units='pix',color=(-1,-1,-1))


def trainer(window):
    colorcode=['red','blue','green','yellow']
    audicode=['C','D','E','F']
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
               'Press Q if you want to proceed to N-back task',]
    quit=visual.TextStim(window,'Thanks for completing the association trainer!', color=(1.0,1.0,1.0))
    s1=visual.TextStim(window,'Press L or Q', color=(1.0,1.0,1.0))    
    vstimlist=[];astimlist=[]
    for i in range(4):
        vstimlist.append(visual.Rect(window,width=100.0,height=100.0,lineColor=colorcode[i],fillColor=colorcode[i], pos=(0,0)))
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
    n.extend(n*3)
    shuffle(n)
    #iterate the pair 5 times
    for i in n:
        vstimlist[i].draw()
        window.flip()
        astimlist[i].play()
        core.wait(0.1)
        window.flip()
        core.wait(0.1)
    

    infolooper(infoloop3,window)
    s1.draw()
    window.flip()
    response=event.waitKeys(keyList=['q','l'])
    if response[0][0]=='l':
        for i in n:
            vstimlist[i].draw()
            window.flip()
            astimlist[i].play()
            core.wait(0.1)
            window.flip()
            core.wait(0.1)
        quit.draw()
        window.flip()
        core.wait(2.0)
    else:
        quit.draw()
        window.flip()
        core.wait(2.0)

trainer(wnd)

    
    
    
    
    
 
 