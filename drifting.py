"""
drifting.py
drifting: an ambient city visual effects programS by Zachary Picker

I don't suspect this is an easy piece of code to read, so good luck...
"""

import numpy as np
import cv2
import time
import drifting_city_generator as acg
import drifting_city_effects as ace
import drifting_menu as dm
from os import getcwd
dir_path = getcwd()

#%%
"""
tkinter menu screen before program starts, for setting various parameters.
"""      
outs = dm.menu()
outsfloat = np.zeros(len(outs))
for i in range(len(outs)):
    outsfloat[i] = float(outs[i])
    if outsfloat[i]==0.:
        outsfloat[i]=0.0001 # a hacky way to barely display it without breaking everything... lol
expected_time = outsfloat[0]
breakonend = outs[1]
changeeras = outs[2]
era_times = outsfloat[3:8]
effect_era_times = outsfloat[8:12]
effect_order = np.array(outs[12:16])
randommode = outs[16]
launchonblack = outs[17]
    
#%%
"""
Main video loop
"""

#displays a black screen until you advance with space/enter/j:
if outs[17]==1:
    while True:
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)                             
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)   
        cv2.imshow('window',np.zeros((100,100,3)))
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == 32 or keypress == 46 or keypress == 106:
            break  
    
#initializing more things that are not important to the user
city_res = 200
growthfac = 4
intro = 0
audioobs = []  
expected_time = expected_time*60
initial_time = time.time()
noshow = 0
blackend = 0

#city generation parameters and scene initializing
scene_start = time.time()
scene_time = np.random.randint(8,16)
era_times = (np.cumsum(era_times)/np.sum(era_times))[0:-1]
#generate special scene masks. not used in the packaged program but I'll leave it here:
#acg.maskcreate(forcenewmasks)
slow = 0
sceneobs = [scene_start,scene_time,expected_time,city_res,growthfac,initial_time,era_times,slow,intro,randommode] #collect scene related objects to pass easily to effects
sceneparams = acg.paramaters(sceneobs)
scene = acg.main(sceneobs,sceneparams)
timenow = time.time()
frame = acg.pan(scene,sceneobs,sceneparams,timenow)
frameedges = np.zeros(np.shape(frame))
sceneedges = np.zeros(np.shape(frame))

#initialize first effect:
effect_start = time.time()
effect_time = np.random.randint(5,10)
effect_era_times = np.array(effect_era_times)*expected_time/np.sum(effect_era_times)
effect_era = 0
era_start = time.time()
era_end = time.time()+effect_era_times[effect_era]
spamend=0 #some effects will make the effect timer or scene timer go quickly ie "spam" it
spamscenesend=0
effect_num = effect_order[effect_era]
if randommode==1:
    effect_num = np.random.choice(effect_order,1,p=effect_era_times/np.sum(effect_era_times))
effectobs = [effect_start,effect_time,expected_time,initial_time,effect_era,era_start,era_end,spamend,spamscenesend,effect_order,city_res,growthfac,frameedges,randommode,effect_num]
effectparams = ace.paramaters(frame,effectobs,audioobs)

#video loop--------------------------------------------------------------------
while True:
    try:
        #generate city-too slow to do in every loop--------------------------------
        if time.time()>scene_start+scene_time:
            noshow = 0
            scene_start = time.time()
            scene_time = np.random.randint(8,16)
            if effectparams[3][2]==2:
                slow = 1
            else:
                slow = 0
            sceneobs = [scene_start,scene_time,expected_time,city_res,growthfac,initial_time,era_times,slow,intro,randommode]
            sceneparams = acg.paramaters(sceneobs)
            scene = acg.main(sceneobs,sceneparams)
            #some effects modify scene:
            if effectparams[1][6]>time.time():
                scene_time=1      
            if effect_num in [2,3]:
                edgeslice = np.random.choice([0,1,2,3,3,3])
                sceneedges = ace.edges(scene,edgeslice)

        #pan across scene
        timenow = time.time()
        if effectparams[4][8] ==4 and effect_order[effect_era] in [2,3] :
            scene = ace.edges(scene,3)
        frame = acg.pan(scene,sceneobs,sceneparams,timenow)
            
        if effect_num in [2,3]: #generating outlines for relevant effects
            frameedges = acg.pan(sceneedges,sceneobs,sceneparams,timenow)
            effectobs = [effect_start,effect_time,expected_time,initial_time,effect_era,era_start,era_end,effectparams[1][5],effectparams[1][6],effect_order,city_res,growthfac,frameedges,randommode,effect_num]
    except Exception:
        noshow = 1
        scene_time = 0
        effect_time = 0
    
    try:
        #effects-------------------------------------------------------------------
        #generate new effect
        if time.time()>effect_start+effect_time:
            noshow = 0
            effect_start = time.time()
            effect_time = np.random.randint(5,10)
            effect_num = effect_order[effect_era]
            if randommode==1:
                effect_num = np.random.choice(effect_order,1,p=effect_era_times/np.sum(effect_era_times))
            effectobs = [effect_start,effect_time,expected_time,initial_time,effect_era,era_start,era_end,effectparams[1][5],effectparams[1][6],effect_order,city_res,growthfac,frameedges,randommode,effect_num]
            effectparams = ace.paramaters(frame,effectobs,audioobs)   
            if effectparams[1][5]>time.time():
                effect_time=0.5
                
        #apply effect 
        frame = ace.main(frame,effectobs,audioobs,effectparams)
        
        #change era if required
        if time.time()>era_end and len(effect_era_times)>effect_era+1 and changeeras==0:
            noshow = 0
            effect_era += 1
            era_start = time.time()
            era_end = time.time()+effect_era_times[effect_era]
            scene_start = time.time()
            effect_num = effect_order[effect_era]
            if randommode==1:
                effect_num = np.random.choice(effect_order,1,p=effect_era_times/np.sum(effect_era_times))            
            effectobs = [effect_start,effect_time,expected_time,initial_time,effect_era,era_start,era_end,0,0,effect_order,city_res,growthfac,frameedges,randommode,effect_num]
            effectparams = ace.paramaters(frame,effectobs,audioobs)  
            if effect_num in [2,3]:
                edgeslice = np.random.choice([0,1,2,3,3,3])
                sceneedges = ace.edges(scene,edgeslice)
            
    except Exception as e:
        noshow = 1
        scene_time = 0
        effect_time = 0
        print(e)
    
#    final fix incase zero-size images come through (dont show image and skip to next scene/effect):
    if np.shape(frame)[0]<1 or np.shape(frame)[1]<1:
        noshow = 1
        scene_time = 0
        effect_time = 0
    try:   
        #cv2 image loop -----------------------------------------------------------
    
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)                             
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        if noshow == 0:
            cv2.imshow('window',frame)      
        
        #if expected time is up, start over, break, or keep going
        if time.time()>initial_time+expected_time:
            if breakonend == 0:
                initial_time = time.time()
            if breakonend == 1:
                break
        
        #input buttons--------------------------------------------------------------
        """
        Buttons
            esc:    quit stream
            space:  new scene
            enter:  new effect
            j:  next effect era
            f:  prev effect era
            q:  black screen before quit
        """
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == 27:                                          # esc: quit visualizer
            break
        if keypress == 32:                                          # space: change scene
            scene_time = 0
        elif keypress == 13:                                        #enter: change effect
            effect_time = 0
        elif keypress == 106 and len(effect_era_times)>effect_era+1: # .j: next effect era
            noshow = 0
            effect_era += 1
            era_start = time.time()
            era_end = time.time()+effect_era_times[effect_era]
            scene_start = time.time()
            scene_time = 0
            effect_num = effect_order[effect_era]
            if randommode==1:
                effect_num = np.random.choice(effect_order,1,p=effect_era_times/np.sum(effect_era_times))
            effectobs = [effect_start,effect_time,expected_time,initial_time,effect_era,era_start,era_end,0,0,effect_order,city_res,growthfac,frameedges,randommode,effect_num]
            effectparams = ace.paramaters(frame,effectobs,audioobs)   
        elif keypress == 102 and effect_era>0:                       # f: prev effect era
            noshow = 0
            effect_era -= 1
            era_start = time.time()
            era_end = time.time()+effect_era_times[effect_era]
            scene_start = time.time()
            scene_time = 0
            effect_num = effect_order[effect_era]
            if randommode==1:
                effect_num = np.random.choice(effect_order,1,p=effect_era_times/np.sum(effect_era_times))
            effectobs = [effect_start,effect_time,expected_time,initial_time,effect_era,era_start,era_end,0,0,effect_order,city_res,growthfac,frameedges,randommode,effect_num]
            effectparams = ace.paramaters(frame,effectobs,audioobs)          
        elif keypress == 113:                                        # q: black screen quit
            blackend = 1
            break
    except Exception:
        scene_time = 0
        effect_time = 0

#if you quit with q, it takes you to this black screen at the end
if blackend == 1:
    while True:
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)                             
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)   
        cv2.imshow('window',np.zeros((100,100,3)))
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == 32 or keypress == 46 or keypress == 106:                    # end: start program
            break  
        
cv2.destroyAllWindows()















