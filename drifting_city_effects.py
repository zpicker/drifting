"""
drifting_city_effects.py
"""
import time
import numpy as np
import cv2
"""
effectobs = [effect_start,
             effect_time,
             expected_time,
             initial_time,
             effect_era,
             era_start,
             era_end,
             spamend,
             spamscenesend,
             effect order,
             city_res,
             growthfac,
             frameedges,
             randommode,
             effect_num]
"""
#%%
"""
main function which applies effects
"""
def main(frame,effectobs,audioobs,effectparams):
    #pull relevant objects from inputs
#    effect_order = effectobs[9]
#    effect_era = effectobs[4]
    effect_num = effectobs[14]
    togetherorder = effectparams[3][0]
    togetherfuncs = [bars,kaleidoscope]
    whicheffect = effectparams[3][2]
    
    #figure out which effects to apply
    effecton = effectparams[0][1]
    if effecton == True:
        if effect_num == 0: 
            frame = bars(frame,effectobs,audioobs,effectparams)
        if effect_num == 1:
            frame = kaleidoscope(frame,effectobs,audioobs,effectparams)
        if effect_num == 2: #alltogether effect is most complicated
            if effectparams[4][8] != 4:
                frame = outlines(frame,effectobs,audioobs,effectparams)
            if whicheffect==0:
                frame = bars(frame,effectobs,audioobs,effectparams)
            if whicheffect==1:
                frame = kaleidoscope(frame,effectobs,audioobs,effectparams)
            if whicheffect in [2,3]:
                for i in range(len(togetherorder)):
                    frame = togetherfuncs[i](frame,effectobs,audioobs,effectparams)
        if effect_num == 3:
            if effectparams[4][8] != 4:
                frame = outlines(frame,effectobs,audioobs,effectparams)
            
    return frame


#%%
"""
function which determines randomized parameters for effects. called separately so that they can remain the same even as cv2 loop goes
"""
def paramaters(frame,effectobs,audioobs):

    #pull relevant objects from inputs
    era_start = effectobs[5]
    era_end = effectobs[6]
#    effect_era=effectobs[4]
    spamend=effectobs[7]
    spamscenesend = effectobs[8]
    effect_order = effectobs[9]
    res = np.shape(frame)
    randommode = effectobs[13]
    effect_num = effectobs[14]

    
    #effect magnitude- increases as it goes on. controls likelihood and effect extremity---------------------
    tparam = (time.time() - era_start)/(era_end-era_start) #ranges from 0 to 1 during the expected effect era length, then freezes at 1
    if randommode == 1:
        tparam = np.random.rand()
    effmag = ((1 + np.sin(tparam*np.pi - (np.pi/2)))**1)/2 #sin function from 0 to 1, then freezes at 1
    if tparam>1:
        effmag = 1
    effecton = np.random.rand()<(effmag**0.5) #determines whether effect will play or not
    
    
    #bars---------------------------------------------------------------------------------------------------
    nbars = int(np.round(np.random.randint(3,12)*effmag)) #number of bars
    barorients,barlocs,barlocs2,barwidth = [0,0,0,0]
    if nbars>0 and effect_num in [0,2]:
        effecton = 1 
        barorients = np.zeros(nbars) #zeros is vertical bars, ones is horizontal bars
        if effmag > 0.1:
            if np.random.rand() > 0.5:
                barorients = np.ones(nbars)
        if effmag > 0.3:
            if np.random.rand() > 0.5:
                barorients = np.random.randint(0,2,nbars)      
                 
        barwidth = (np.random.randint(np.min([res[0],res[1]])/60,np.min([res[0],res[1]])/6,nbars)*(effmag+.5)).astype(int) #widths of bars
        barlocmax = np.max(barwidth)+1 #farthest a bar can start from the left hand side
        for i in range(nbars): #generate bar locations and the locations of bars they're copying from
            if barorients[i]==0:
                barlocs = np.random.randint(1,res[0]-barlocmax-10,nbars)
                barlocs2 = np.random.randint(1,res[0]-barlocmax-10,nbars)
            elif barorients[i]==1:
                barlocs = np.random.randint(1,res[1]-barlocmax-10,nbars)
                barlocs2 = np.random.randint(1,res[1]-barlocmax-10,nbars)
                
    #spam controls. spam activates at given values of effmag below---------------------------------------------
    if effect_num == 0:
        spammag = 0.6
        spammagend = 1
        spamscenemag = 0.85
        spamscenemagend = 1
    if effect_num == 1:
        spammag = 0.75
        spammagend = 1
        spamscenemag = 0.9
        spamscenemagend = 1       
    if effect_num == 2:
        spammagend = 1
        spammag = 1
        spamscenemag = 1
        spamscenemagend = 1
    if effect_num == 3:
        spammagend = 1
        spammag = 1
        spamscenemag =1
        spamscenemagend = 1
        
    if effmag >spammag and effmag<spammagend: #spam effect
        if time.time()>spamend and np.random.rand()>0.75:
            spamend = time.time()+np.random.randint(5,10)
    if effmag >spamscenemag and effmag<spamscenemagend: #spam scenes
        if time.time()>spamscenesend and np.random.rand()>0.75:
            spamscenesend = time.time()+np.random.randint(5,10)
       
    #kaleidoscope------------------------------------------------------------------------------------------
    ktype = np.random.randint(2) #horizontal mirror or vertical
    ktake = np.random.randint(2) #which of the two halfs to mirror
    kwhich = 0 #determines which kinds of mirroring occur in situations where there's multiple
    if effmag < 0.05 and effect_num in [1,2]:
        effecton = 0
    if effmag >0.15:
        if np.random.rand()>0.75:
            ktype = np.random.randint(2,4) #one diagonal mirror can occur
    if effmag > 0.3:
        if np.random.rand()>0.5:
            ktype = 4 #horizontal+vertical mirroring can occur (4 squares)
            kwhich = np.random.choice(range(2),2,replace=False)
            ktake = np.random.randint(0,2,2)
    if effmag > 0.45:
        effecton = 1
        if np.random.rand()>0.5:
            ktype = 5 #any two mirros can occur incl. diag
            kwhich = np.random.choice(range(4),2,replace=False)
            ktake = np.random.randint(0,2,2)
    if effmag > 0.6:
        if np.random.rand()>0.5:
            ktype = 6 #any 3 mirrors can occur
            ktake = kwhich = np.random.choice(range(4),3,replace=False)
            ktake = np.random.randint(0,2,3)
            
    #alltogether: all the functions together-------------------------------------------------
    #all these essentially sort the effects into various orders, slightly clunky
    togetherorder = np.random.choice(range(len(effect_order)-1),2,replace=False)
    whicheffect = np.random.randint(4)
    outfirst = np.random.choice([0,0,1])
    
    #outlines-----------------------------------------------------------------------------------------
    edgetype = np.random.randint(3) #determines what edges the edge-finder actually detects (ie color layers in pic)
    edgecolor = np.random.rand(3,3)*1.3 #color of edge
    modifyscene = 0 #deprecated but i'm lazy
    
    #bars for sweeping-- all parameters ~same as bars effect:
    nbarsout = np.random.randint(8,12)
    barorientsout,barlocsout,barlocs2out,barwidthout = [0,0,0,0]
    nbarsout = 1
    if nbarsout>0 and effect_num in [3,2]:
        effecton = 1
        barorientsout = np.ones(nbarsout)
        if effmag > 0.05:
            if np.random.rand() > 0.3:
                barorientsout = np.zeros(nbarsout)
        if effmag > 0.1:
                barorientsout = np.random.randint(0,2,nbarsout)      
        scenesizex = res[0] #i initially had to be more careful about size but I think this doesn't actually matter anymore
        scenesizey = res[1]
        barwidthout = (np.random.randint(np.min([scenesizex,scenesizey])/6,np.min([scenesizex,scenesizey])/2,nbarsout)).astype(int)-5
        barlocmaxout = np.max(barwidthout)
        for i in range(nbarsout):
            if barorientsout[i]==0:
                barlocsout = np.random.randint(1,scenesizex/2,nbarsout)
                barlocs2out = np.random.randint(1,scenesizex/2,nbarsout)
            elif barorientsout[i]==1:
                barlocsout = np.random.randint(1,scenesizey-barlocmaxout,nbarsout)
                barlocs2out = np.random.randint(1,scenesizey-barlocmaxout,nbarsout)
    #sweeping outlines on color
    outtype = 0
    city2 = 0
    stutter = 0
    rolldir = np.random.randint(2)
    #second city outline on top
    if effmag>0.08:
        if np.random.rand()>0.5:
            city2 = np.random.randint(1,3)
    #black boxes on color
    if effmag>0.15:
        outtype = 1
    #black boxes on black
    if effmag > 0.35:
        outtype = 2
    #stutter on black
    if effmag >0.5:
        outtype = 3
        stutter = np.random.randint(2,6)
        if effect_num==2:
            stutter=np.random.randint(4)
        spamend=0
    #exploder ie apply edge finding to itself in every cv2 loop frame. bit slow obviously
    if effmag >0.75:
        outtype = 3
        if np.random.rand()>0.2:
            outtype = 4
    #stutter on colored backgrounds
    if effmag>0.9:
        outtype = 5
        stutter = np.random.randint(2,6)
        if effect_num==2:
            stutter=stutter=np.random.randint(4)
    
    if effect_num==2:
        if effmag<0.05:
            effecton=0
            
    if effmag < 0.03:
        effecton = 0    
        
    return [[effmag,effecton],
                [nbars,barorients,barlocs,barlocs2,barwidth,spamend,spamscenesend],
                [ktype,ktake,kwhich],
                [togetherorder,outfirst,effect_num,whicheffect],
                [edgetype,edgecolor,modifyscene,nbarsout,barorientsout,barlocsout,barlocs2out,barwidthout,outtype,city2,stutter,rolldir]]

#%% just bars hey
"""
this effect grabs a slice ("bar") of the image and copies it to another portion of the image
"""
def bars(frame,effectobs,audioobs,effectparams):
    res = np.shape(frame)
    nbars,barorients,barlocs,barlocs2,barwidth,spam,spamscenes = effectparams[1]
    if nbars>0:
        for i in range(nbars):
            if barorients[i]==0: #swap vertical bars with other vertical bars
                width = np.min([barwidth[i],res[0]-barlocs[i],res[0]-barlocs2[i]])
                if width > 1:
                    frame[barlocs[i]:barlocs[i]+width, :, :] = frame[barlocs2[i]:barlocs2[i]+width, :, :]
            elif barorients[i]==1: #same but horizontally
                width = np.min([barwidth[i],res[1]-barlocs[i],res[1]-barlocs2[i]])
                if width > 1:
                    frame[:, barlocs[i]:barlocs[i]+width, :] = frame[:, barlocs2[i]:barlocs2[i]+width, :]
    return frame
#%%
"""
mirrors various halfs of the image
"""    

def kaleidoscope(frame,effectobs,audioobs,effectparams):
    ktype,ktake,kwhich = effectparams[2]
    res = np.shape(frame)
    #see paramaters function for what the various combinations are
    if ktype < 4: #hor/vert/diag flips
        frame = kflip(frame,ktype,ktake,res)
    if ktype == 4 or ktype == 5: #2 flips
        frame = kflip(frame,kwhich[0],ktake[0],res)
        res = np.shape(frame)
        frame = kflip(frame,kwhich[1],ktake[1],res)
    if ktype == 6: #3 flips
        frame = kflip(frame,kwhich[0],ktake[0],res)
        res = np.shape(frame)
        frame = kflip(frame,kwhich[1],ktake[1],res)
        res = np.shape(frame)
        frame = kflip(frame,kwhich[2],ktake[2],res)
    return frame

#this function actually handles the flipping
def kflip(frame,kftype,ktake,res): #seperate def for hor/vert/diagonal flips
    if kftype == 0: #vertical flip (I think...)
        size = res[0]
        if np.mod(size,2)==1:
            size -= 1
        ktake2 = abs(ktake-1)
        frame[int((size/2)*ktake):int((size/2)+((size/2)*ktake)),:,:] = np.flip(frame[int((size/2)*ktake2):int((size/2)+((size/2)*ktake2)),:,:],0)
    if kftype == 1: #horizontal flip (I think...)
        size = res[1]
        if np.mod(size,2)==1:
            size -= 1
        ktake2 = abs(ktake-1)
        frame[:,int((size/2)*ktake):int((size/2)+((size/2)*ktake)),:] = np.flip(frame[:,int((size/2)*ktake2):int((size/2)+((size/2)*ktake2)),:],1)
    if kftype == 2: #diagonal flip, tl-br
        sizex,sizey = [res[0],res[1]] 
        if np.mod(sizex,2)==1:
            sizex-=1
        if np.mod(sizey,2)==1:
            sizey-=1
        size = np.min([sizex,sizey])
        xstart = int((sizex-size)/2)
        xend = sizex-xstart
        ystart = int((sizey-size)/2)
        yend = sizey-ystart
        frame = frame[xstart:xend,ystart:yend,:]
        frame = cv2.resize(frame,(np.shape(frame)[0],np.shape(frame)[1]))
        if ktake == 0 or ktake==1:
            mask = np.triu((frame[:,:,0]+1),+1)>0
        if ktake == 1:
            mask = np.tril((frame[:,:,0]+1),-1)>0
        frame[mask,:]=  [0,0,0]
        frame = frame + np.transpose(frame,(1,0,2))
    if kftype ==3: #diagonal flip, bl-tr
        sizex,sizey = [res[0],res[1]]
        if np.mod(sizex,2)==1:
            sizex-=1
        if np.mod(sizey,2)==1:
            sizey-=1
        size = np.min([sizex,sizey])
        xstart = int((sizex-size)/2)
        xend = sizex-xstart
        ystart = int((sizey-size)/2)
        yend = sizey-ystart
        frame = frame[xstart:xend,ystart:yend,:]
        frame = cv2.resize(frame,(np.shape(frame)[0],np.shape(frame)[1]))
        frame = np.flip(frame,0)
        if ktake == 0:
            mask = np.triu((frame[:,:,0]+1),1)>0
        if ktake == 1:
            mask = np.tril((frame[:,:,0]+1),-1)>0
        frame[mask,:]=  [0,0,0]
        frame = frame + np.transpose(frame,(1,0,2))
        frame = np.flip(frame,0)
    return frame

#%%
"""
adds outlines to image with various iterations on the kind of effect produced
"""    

def outlines(frame,effectobs,audioobs,effectparams):
    
    #pull relevant objects from inputs
    edgetype,edgecolor,modifyscene,nbarsout,barorientsout,barlocsout,barlocs2out,barwidthout,outtype,city2,stutter,rolldir = effectparams[4]
    res = np.shape(frame)
    effect_start = effectobs[0]
    effect_time = effectobs[1]
    tpar = (time.time()-effect_start)/effect_time
    effect_num = effectobs[14]
    barlocsout = (barlocsout + tpar*res[0]/2).astype(int)
    barlocs2out = (barlocs2out + tpar*res[0]/2).astype(int)
    frameedge0 = effectobs[12]*edgecolor[0]
    if city2 == 1:
        frame = frame + np.roll(frameedge0,int(res[0]/2),1)    
    #outlines only occur in 'bars' which move across the image.
    if outtype <3:
        if nbarsout>0:
            for i in range(nbarsout):
                if barorientsout[i]==0:
                    width = np.min([barwidthout[i],res[0]-barlocsout[i]])
                    if width > 1:
                        if outtype==0:
                            frame[barlocsout[i]:barlocsout[i]+width, :, :] = frame[barlocsout[i]:barlocsout[i]+width, :, :] + frameedge0[barlocsout[i]:barlocsout[i]+width, :, :]/2
                        if outtype==1:
                            frame[barlocsout[i]:barlocsout[i]+width, :, :] = frameedge0[barlocsout[i]:barlocsout[i]+width, :, :]*2
                        if outtype==2 and effect_num!=2:
                            frame = np.zeros(res)
                            frame[barlocsout[i]:barlocsout[i]+width, :, :] = frameedge0[barlocsout[i]:barlocsout[i]+width, :, :]*2
                elif barorientsout[i]==1:
                    width = np.min([barwidthout[i],res[1]-barlocsout[i],res[1]-barlocs2out[i]])
                    if width > 1:
                        if outtype==0:
                            frame[:, barlocsout[i]:barlocsout[i]+width, :] = frame[:, barlocsout[i]:barlocsout[i]+width, :] + frameedge0[:, barlocsout[i]:barlocsout[i]+width, :]/2
                        if outtype==1:
                            frame[:, barlocsout[i]:barlocsout[i]+width, :] = frameedge0[:, barlocsout[i]:barlocsout[i]+width, :]*2
                        if outtype==2 and effect_num!=2:
                            frame = np.zeros(res)
                            frame[:, barlocsout[i]:barlocsout[i]+width, :] = frameedge0[:, barlocsout[i]:barlocsout[i]+width, :]*2
        else:
            frame = frameedge0*1.5

    #special altogether case
    if outtype==2 and effect_num==2: 
        frame = frameedge0*1.5
    
    #produce multiple moving reverberations on black background
    if outtype == 3:
        frame = frameedge0*1.5 
        if np.shape(frame)[0]==np.shape(frame)[1]:
            if stutter>0:
                for i in range(np.min([int(tpar*60),stutter])):
                    frame = frame + np.roll(frameedge0,int(i*50*tpar),rolldir)    
    #do nothing, meanwhile the edge finding will actually occur in cv2 loop for cool effect
    if outtype == 4:
        frame = frameedge0*1.5 
    #back to stuttering/reverbarations but on color image
    if outtype == 5:
        if np.shape(frame)[0]==np.shape(frame)[1]:
            if stutter>0:
                for i in range(np.min([int(tpar*60),stutter])):
                    frame = frame + np.roll(frameedge0,int(i*50*tpar),rolldir)
        else:
            frame = frame+frameedge0
    #add a new city outline on top that is not in line (exactly 1/2 image out of line)
    if city2 == 2:
        frame = frame + np.roll(frameedge0,int(res[0]/2),1)  
    return frame  

#actual function which generates the edges, as a new image
def edges(scene,edgeslice):
    sceneedge = np.zeros((np.shape(scene)[0],np.shape(scene)[1],3))
    if edgeslice < 3: #use only one of the color layers to find edges
        lines = cv2.Canny((255*scene[:,:,edgeslice]).astype('uint8'),100,200)/255.
        sceneedge[:,:,0] =lines
        sceneedge[:,:,1] =lines
        sceneedge[:,:,2] =lines
    if edgeslice == 3: #use all 3 color layers to find edges
        lines = cv2.Canny((255*scene[:,:,0]).astype('uint8'),100,200)/255.+cv2.Canny((255*scene[:,:,1]).astype('uint8'),100,200)/255.+cv2.Canny((255*scene[:,:,2]).astype('uint8'),100,200)/255.
        sceneedge[:,:,0] =lines
        sceneedge[:,:,1] =lines
        sceneedge[:,:,2] =lines
    return sceneedge