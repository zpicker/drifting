"""
drifting_city_generator.py
contains city generation code for drifting.py to call
"""
import numpy as np
import time
import cv2
import random
import os
dir_path = os.getcwd()

"""
sceneobs = [scene_start
            scene_time
            expected_time,
             city_res,
             growthfac,
             initial_time,
             era_times,
             slow,
             intro,
             randommode]
"""
#%%
"""
main function collates all relevant parts of the scene
"""

def main(sceneobs,params):
    
    nsizey = sceneobs[3]
    nsizex = (nsizey*2)
    growthfac = sceneobs[4]
           
    frame = sky(sceneobs,params)
    if params[6][0] > 0:
        frame = specialscene(frame,sceneobs,params)
    frame = buildings(frame,sceneobs,params)
    frame = misc(frame,sceneobs,params) 
    frame = cv2.flip(frame,flipCode=0)
    frame= cv2.resize(frame,(growthfac*nsizex,growthfac*nsizey),interpolation = cv2.INTER_NEAREST)


       
    return frame

#%%
"""
_any_ random parameter that needs to be constant for scene duration is created here
"""    


def paramaters(sceneobs):
    
    #time of day
    expected_time = sceneobs[2]
    initial_time = sceneobs[5]
    era_times = sceneobs[6]
#    scene_time = sceneobs[1]
    slow = sceneobs[7]
    intro = sceneobs[8]
    randommode = sceneobs[9]
    darkfact = 1
    
    timenow = time.time()
    
    if randommode==1:
        timenow = np.random.rand()*expected_time + initial_time

    if timenow-initial_time < expected_time*era_times[0] or timenow-initial_time > expected_time*era_times[3]:
        era = 0 #day
    if timenow-initial_time > expected_time*era_times[0] and timenow-initial_time < expected_time * era_times[1]:
        era = 1 #sunset/rise
    if timenow-initial_time > expected_time*era_times[1] and timenow-initial_time < expected_time * era_times[2]:
        era = 2 #night
    if timenow-initial_time > expected_time*era_times[2] and timenow-initial_time < expected_time * era_times[3]:
        era = 1 #sunset/rise
    if intro == 1:
        era = 0            
        
#    if randommode == 1:
#        era_times2 = np.concatenate((era_times,[1]))
#        era_times2[1:] -= era_times2[:-1].copy() #undo cumsum lol
#        era = np.random.choice([0,1,2,3,4],1,p=era_times2/np.sum(era_times2))[0]
    #pan
    lr = np.random.randint(4)
    zoom = np.random.choice([0,0,0,2+np.random.rand(),-2-np.random.rand()])
    if slow==1:
        lr = np.random.randint(2,4)
        zoom = 0
    
    #sky
    if era == 2:
#        darkfact = (1 - np.abs(((timenow-(initial_time+midlen))*2/midlen)))
        darkstart = initial_time + era_times[1]*expected_time
        darkend = initial_time + era_times[2]*expected_time
        midnight = (darkstart+darkend)/2
        darkfact = np.abs((timenow-midnight)/(darkend-darkstart))
        darkfact = np.max([darkfact,0.05])
#    print(era)
#    print(darkfact)
    

    color_bkg = np.random.rand(3)
    if era == 2:
        color_bkg = color_bkg*darkfact
    nsizey = sceneobs[3]
    nsizex = (nsizey*2)
    color_cum = np.random.rand(3)
    if era == 2:
        color_cum = color_cum*darkfact
    color_strat = np.random.rand(3)
    if era == 2:
        color_strat = color_strat*darkfact
    color_sun = np.random.rand(3)
    ncum = np.random.randint(3)
    if ncum > 0:
        randcenx = np.random.randint(nsizex*1/3,nsizex*2/3,2*ncum)
        randceny = np.random.randint(0,nsizey*0.3,2*ncum)
        randrad = np.random.randint(0.5*nsizey,0.7*nsizey,2*ncum)
    else:
        randcenx,randceny,randrad = [[0],[0],[0]]
    if era == 0 or era == 2:
        nstrat = np.random.choice([0,0,np.random.randint(4)])
    if era == 1:
        nstrat = np.random.randint(8)
    randh = np.random.choice(np.logspace(np.log10(nsizey*.4),np.log10(nsizey*0.95),100),nstrat)
    if nstrat>0:
        for i in range(nstrat):
            randthick = np.random.randint(1,nsizey/15) * (1+(randh[i]/nsizey))
    else:
        randthick = [0]
    nsun = np.random.choice([0,0,0,1])
    nstars = 0
    nsizes = 0
    starslocs = 0
    starsheights = 0
    if era == 2:
        nstars = int(np.random.randint(30,70)/darkfact/5)
        nsizes = np.random.randint(1,4,nstars)
        starslocs = np.random.randint(0,nsizex,nstars)
        starsheights = np.random.choice(np.logspace(np.log10(nsizey*.3),np.log10(nsizey),300),nstars)


    #buildings
    perspective = np.random.randint(2)
    nshapes = np.random.randint(20,30)
    color_bld = np.random.rand(3)*(1/2)
    if era == 0:
        color_bld = color_bld*1.5
    if era == 2:
        color_bld = color_bld*.8
    maxheight = np.random.randint(nsizey*.5,nsizey*.9)
    heights = np.random.randint(nsizey*(3/10),maxheight,nshapes) #height of top corner
    locs = np.random.randint(0,nsizex,nshapes)
    angle1 = np.random.rand()*(-np.pi*(1/4))
    angle2 = np.random.rand()*(np.pi*(1/4))
    lengths1 = np.random.randint(5,nsizex/8,nshapes)
    lengths2 = np.random.randint(5,nsizex/8,nshapes)
    lowheight = np.random.randint(nsizey*(2/10),nsizey*(3/10))
    nspires = np.random.randint(1,10)
    spiresheights = np.random.randint(nsizey*0.5,nsizey*0.9,nspires)
    spireslocs = np.random.randint(0,nsizex,nspires)
    
    #windows
    windowside = np.random.randint(0,3,nshapes)
    color_wind = np.array([0,1,1])*np.random.rand()
    if era == 0:
        color_wind = color_wind*1/2
    if era == 1:
        color_wind = color_bkg
    if era ==2:
        color_wind = np.array([0,1,1])
    winddist_x = np.random.randint(1,10,nshapes)
    winddist_y = np.random.randint(1,10,nshapes)
    winddist2_x = np.zeros((nshapes))
    winddist2_y = np.zeros((nshapes))
    for i in range(nshapes):
        winddist2_x[i] = np.random.randint(winddist_x[i])
        winddist2_y[i] = np.random.randint(winddist_y[i])

    #misc
    nposts = np.random.randint(5)   
    postlocs = np.random.randint(0,nsizex,nposts)
    postheights = np.random.randint(nsizey*.1,nsizey*.5,nposts)
    wire = [0,0]
    if nposts > 1:
        wire = np.random.randint(0,2,(nposts,nposts))
    
    
    #ducks
    nducks = np.random.choice([0,0,np.random.randint(0,16)])
    formation = np.random.randint(2)
    formation=1
    color_duck = random.choice([color_cum,color_strat,color_wind])
    if formation == 0 and nducks>0:
        ducklocs = [np.random.randint(nsizex),np.random.randint(nsizey)]
        duckangle = np.random.rand()*2*np.pi
        ducksize = np.random.randint(1,4)
    if formation == 1 and nducks>0:
        ducklocs = [np.random.randint(0,nsizex,nducks),np.random.randint(0,nsizey,nducks)]
        duckangle = np.random.rand(nducks)*2*np.pi
        ducksize = np.random.randint(1,4,nducks)
    else:
        ducklocs,duckangle,ducksize = [[[0],[0]],0,0]
    
    #special scenes, not used in packaged program
    specialind = 0
    wraploc = 0
#    numscenes = len(os.listdir(dir_path+'\\ambient_city_masks'))
#    specialon = 100
#    if numscenes>0:
#        specialon = np.random.randint(numscenes*expected_time/scene_time) 
#    specialind = 0
#    if specialon < 4: #ie each special scene will appear roughly four times
#        specialind = np.random.randint(1,numscenes+1)
#        heights = np.random.randint(nsizey*(3/10),nsizey*(5/10),nshapes) #height of top corner
#    wraploc = np.random.randint(nsizey)
    
    
    return [[lr,zoom],
            [color_bkg,nsizey,nsizex,color_cum,color_strat,color_sun,ncum,nstrat,nsun,randh,randthick,randcenx,randceny,randrad,nstars,nsizes,starslocs,starsheights],
            [perspective,nshapes,color_bld,heights,locs,lengths1,lengths2,angle1,angle2,lowheight,nspires,spiresheights,spireslocs],
            [windowside,color_wind,winddist_x,winddist_y,winddist2_x,winddist2_y],
            [nducks,formation,ducklocs,duckangle,ducksize,color_duck],
            [nposts,postlocs,postheights,wire],
            [specialind,wraploc]]

#%%
"""
creates frame containing sky+clouds
"""    
    
    
def sky(sceneobs,params):

    color_bkg,nsizey,nsizex,color_cum,color_strat,color_sun,ncum,nstrat,nsun,randh,randthick,randcenx,randceny,randrad,nstars,nsizes,starslocs,starsheights = params[1]   
    img = np.ones((nsizey,nsizex,3))
    img[:,:,0] = np.ones((nsizey,nsizex))*color_bkg[0]
    img[:,:,1] = np.ones((nsizey,nsizex))*color_bkg[1]
    img[:,:,2] = np.ones((nsizey,nsizex))*color_bkg[2]
    
    x = np.arange(0, np.shape(img)[1])
    y = np.arange(0, np.shape(img)[0])
    
    if nstars>0:
        for i in range(nstars):
            mask_star = (x[np.newaxis,:]>starslocs[i]) & (x[np.newaxis,:]<starslocs[i]+nsizes[i]) & (y[:,np.newaxis]>starsheights[i]) & (y[:,np.newaxis]<starsheights[i]+nsizes[i])
            img[mask_star] = np.array([1,1,1])*(np.random.randint(60,100)/100)
    
    if ncum>0:
        for i in range(ncum):
            mask_cum = ((x[np.newaxis,:]-randcenx[i])**2 + (y[:,np.newaxis]-randceny[i])**2 < randrad[i]**2) |  ((x[np.newaxis,:]-randcenx[i+ncum])**2 + (y[:,np.newaxis]-randceny[i+ncum])**2 < randrad[i+ncum]**2)
            img[mask_cum,:] = color_cum
    if nstrat>0:
        for i in range(nstrat):
            mask_strat = (y[:,np.newaxis]<randh[i]) & (y[:,np.newaxis]>randh[i]- randthick) & (x[np.newaxis,:]>0)
            img[mask_strat,:] = color_strat
            
    return img
#%%
"""
generates buildings, windows, spires
"""
def buildings(img,sceneobs,params):
    
    perspective,nshapes,color_bld,heights,locs,lengths1,lengths2,angle1,angle2,lowheight,nspires,spiresheights,spireslocs = params[2]
    windowside,color_wind,winddist_x,winddist_y,winddist2_x,winddist2_y = params[3]
    
    x = np.arange(0, np.shape(img)[1])
    y = np.arange(0, np.shape(img)[0])
    mask_low =  (y[:,np.newaxis]<lowheight) & (x[np.newaxis,:]>=0)
    img[mask_low,:]=color_bld*1/2
    
    for i in range(nspires):
        #rightside:
        mask_rs =  (x[np.newaxis,:] > spireslocs[i]) & (x[np.newaxis,:] < spireslocs[i] +np.random.randint(2,5)) & (y[:,np.newaxis] < spiresheights[i]+((x[np.newaxis,:]-spireslocs[i])*np.tan(angle1)) )
        img[mask_rs,:] = color_bld
        #leftside:
        mask_ls = (x[np.newaxis,:] > spireslocs[i]+1 - np.random.randint(2,5)) & (x[np.newaxis,:] < spireslocs[i]+1) & (y[:,np.newaxis] < spiresheights[i]-((-x[np.newaxis,:]+spireslocs[i])*np.tan(angle2)) )
        img[mask_ls,:] = color_bld * 1/2

    for i in range(nshapes):
        #rightside:
        mask_r =  (x[np.newaxis,:] > locs[i]) & (x[np.newaxis,:] < locs[i] +lengths1[i]) & (y[:,np.newaxis] < heights[i]+((x[np.newaxis,:]-locs[i])*np.tan(angle1)) )
        img[mask_r,:] = color_bld
        #leftside:
        mask_l = (x[np.newaxis,:] > locs[i]+1 - lengths2[i]) & (x[np.newaxis,:] < locs[i]+1) & (y[:,np.newaxis] < heights[i]-((-x[np.newaxis,:]+locs[i])*np.tan(angle2)) )
        img[mask_l,:] = color_bld * 1/2
        if windowside[i] == 0:
            mask_w = (mask_r) & (np.mod(x[np.newaxis,:]-winddist2_x[i],winddist_x[i])==0) & (np.mod((y[:,np.newaxis]-((x[np.newaxis,:]-locs[i])*np.tan(angle1))).astype(int)-winddist2_y[i],winddist_y[i])==0)
            img[mask_w,:] = color_wind
        if windowside[i] == 1:
            mask_w = (mask_l) & (np.mod(x[np.newaxis,:]-winddist2_x[i],winddist_x[i])==0) & (np.mod((y[:,np.newaxis]+((-x[np.newaxis,:]+locs[i])*np.tan(angle2))).astype(int)-winddist2_y[i],winddist_y[i])==0)
            img[mask_w,:] = color_wind*(1/2)
            
    return img
#%%
"""
generates miscellaneous city details
"""
def misc(img,sceneobs,params):
    nposts,postlocs,postheights,wire = params[5]
    perspective,nshapes,color_bld,heights,locs,lengths1,lengths2,angle1,angle2,lowheight,nspires,spiresheights,spireslocs = params[2]

    x = np.arange(0, np.shape(img)[1])
    y = np.arange(0, np.shape(img)[0])
    #wires
    if nposts > 1:
        for i in range(nposts):
            #rightside:
            mask_rs =  (x[np.newaxis,:] > postlocs[i]) & (x[np.newaxis,:] < postlocs[i] +np.random.randint(2,4)) & (y[:,np.newaxis] < postheights[i]+((x[np.newaxis,:]-postlocs[i])*np.tan(angle1)) )
            img[mask_rs,:] = color_bld*1.1
            #leftside:
            mask_ls = (x[np.newaxis,:] > postlocs[i]+1 - np.random.randint(2,4)) & (x[np.newaxis,:] < postlocs[i]+1) & (y[:,np.newaxis] < postheights[i]-((-x[np.newaxis,:]+postlocs[i])*np.tan(angle2)) )
            img[mask_ls,:] = color_bld * 2/3 
            for j in range(nposts):
                if wire[i,j] == 1 and i!=j:
                    x1 = np.min([postlocs[i],postlocs[j]])
                    x2 = np.max([postlocs[i],postlocs[j]])
                    if x1==x2:
                        break
                    y1 = postheights[np.where(postlocs==x1)[0]][0]
                    y2 = postheights[np.where(postlocs==x2)[0]][0]
                    if x1+1==x2:
                        x2+=2
                    x3 = np.random.randint(x1+1,x2)
                    if x2==x3:
                        x2+=1
                    y3 = np.random.randint(1+(np.min([y1,y2])/3), 2+(np.min([y1,y2])/2))
                    denom = (x1-x2)*(x1-x3)*(x2-x3)
                    A = ((x3 * (y2 - y1)) + (x2 * (y1 - y3)) + (x1 * (y3 - y2))) / denom
                    B = (((x3**2) * (y1 - y2)) + ((x2**2) * (y3 - y1)) + ((x1**2) * (y2 - y3))) / denom
                    C = (((x2**2)*((x3*y1)-(x1*y3)))+(x2*(((x1**2)*y3)-((x3**2)*y1)))+((x1*x3*y2)*(x3-x1))) / denom
                    offset = 0
                    if i>j:
                        offset = 3
                    mask_wire = (x[np.newaxis,:] > x1) & (x[np.newaxis,:] < x2) & (y[:,np.newaxis] < (A*(x[np.newaxis,:]**2)) + (B*x[np.newaxis,:]) + C-offset) & (y[:,np.newaxis] > (A * (x[np.newaxis,:]**2)) + (B*x[np.newaxis,:]) + C -np.random.randint(1,3)-offset)
                    img[mask_wire,:] = color_bld*1.5
    return img

#%%
"""
called in main code loop, moves scene around
"""
def pan(img,sceneobs,params,timenow):
    
    scene_start = sceneobs[0]
    scene_time = sceneobs[1]
    nsizex = np.shape(img)[1]
    nsizey = np.shape(img)[0]
    lr,zoom = params[0]
    if lr == 0:
        img = img[:,int(((timenow-scene_start)/scene_time)*nsizex/2):int((nsizex/2)+(((timenow-scene_start)/scene_time)*nsizex/2))]
    if lr == 1:
        img = img[:,int((nsizex/2)-(((timenow-scene_start)/scene_time)*nsizex/2)):int(nsizex-(((timenow-scene_start)/scene_time)*nsizex/2))]
    if lr == 2:
        img = img[:,int(nsizex*(1/3))+int(((timenow-scene_start)*1/3/scene_time)*nsizex/2):int(nsizex*(1/3))+int((nsizex/2)+(((timenow-scene_start)/scene_time*1/3)*nsizex/2))]
    if lr == 3:
        img = img[:,int((nsizex/2)-(((timenow-scene_start)*1/3/scene_time)*nsizex/2)):int(nsizex-(((timenow-scene_start)*1/3/scene_time)*nsizex/2))]
    
    if zoom > 0:
        scale = (((timenow-scene_start)/scene_time)+zoom)/zoom
        if scale>0 and scale<1:
            img = cv2.resize(img,(int(scale*nsizex),int(scale*nsizey)))
            img = img[int(((nsizey*scale)-nsizey)*(1/2)) : int(((nsizey*scale)+nsizey)*(1/2)) , 
                  int(((nsizex*scale)-nsizex)*(1/2)) : int(((nsizex*scale)+nsizex)*(1/2))]
    elif zoom < 0:
        scale = -((1-((timenow-scene_start)/scene_time))-zoom)/zoom
        if scale>0 and scale<1:
            img = cv2.resize(img,(int(scale*nsizex),int(scale*nsizey)))
            img = img[int(((nsizey*scale)-nsizey)*(1/2)) : int(((nsizey*scale)+nsizey)*(1/2)) , 
                  int(((nsizex*scale)-nsizex)*(1/2)) : int(((nsizex*scale)+nsizex)*(1/2))]
    return img

#%%
"""
a few pre-drawn special scenes
"""
def specialscene(img,sceneobs,params):
    special_ind,wraploc = params[6]
    perspective,nshapes,color_bld,heights,locs,lengths1,lengths2,angle1,angle2,lowheight,nspires,spiresheights,spireslocs = params[2]
    windowside,color_wind,winddist_x,winddist_y,winddist2_x,winddist2_y = params[3]
    name = os.listdir(dir_path+'\\ambient_city_masks')[special_ind-1]
    maskobj = np.load(dir_path+'\\ambient_city_masks\\'+name).astype(bool)
    maskobj = np.roll(maskobj,wraploc,axis=1)
    img[maskobj[:,:,0],:]=color_bld
    img[maskobj[:,:,1],:]=color_bld*1/2
    img[maskobj[:,:,2],:]=color_wind
    img[maskobj[:,:,3],:]=color_wind*1/2
    
    return img

#%%
"""
called in main code loop, animates ducks
"""
#broken for now don't even bother...

#def ducks(img,sceneobs,params):
#    scene_start = sceneobs[0]
#    scene_time = sceneobs[1]
#    growthfac = sceneobs[4]
#    nsizex = np.shape(img)[1]
#    nsizey = np.shape(img)[0]
#    nduck,formation,ducklocs,duckangle,ducksize,color_duck = params[4]
#    ducksize = np.array(ducksize)*growthfac
#    ducklocs = np.array(ducklocs)*growthfac
#    
#    x = np.arange(0, np.shape(img)[1])
#    y = np.arange(0, np.shape(img)[0])
#
#    if formation == 1 and nduck > 0:
#        for i in range(nduck):
#            motionx = ((time.time()-scene_start)/scene_time)*(nsizex/150)*ducksize[i]*np.cos(duckangle[i])
#            motiony =((time.time()-scene_start)/scene_time)*(nsizex/150)*ducksize[i]*np.sin(duckangle[i])
#            if ducklocs[1][i]+motiony > nsizey-1 or ducklocs[1][i]+motiony < 1:
#                motiony = -motiony
#            if ducklocs[0][i]+motionx > nsizey-1 or ducklocs[0][i]+motionx < 1:
#                motionx = -motionx
##             img2[int(ducklocs[1][i]+motiony),int(ducklocs[0][i]+motionx):int(ducklocs[0][i]+motionx + 0.5*ducksize[i]),:]=color_duck*2
#            mask_wing = (x[np.newaxis,:]>ducklocs[0][i]+motionx) & (x[np.newaxis,:]<ducklocs[0][i]+motionx+ducksize[i]) & (y[:,np.newaxis]<ducklocs[1][i]+motiony +(x[np.newaxis,:]-ducklocs[0][i])**2) & (y[:,np.newaxis]>ducklocs[1][i]+motiony-ducksize[i] +(x[np.newaxis,:]-ducklocs[0][i])**2)
#            img[mask_wing,:] = color_duck
#    return img

#%%
"""
create special scene masks
"""
def maskcreate(forcenewmasks):
    #create masks of any new images. see image specifications...
    if not os.path.exists((dir_path+'\\ambient_city_masks')):
        os.mkdir(dir_path+'\\ambient_city_masks')
    if not len(os.listdir(dir_path+'\\ambient_city_scenes'))==0:
        for scenepic in os.listdir(dir_path+'\\ambient_city_scenes'):
            filename = os.path.splitext(scenepic)[0]
            if not os.path.exists((dir_path+'\\ambient_city_masks\\'+filename+'.npy')) or forcenewmasks == 1:
                sceneimg = cv2.imread(dir_path+'\\ambient_city_scenes\\'+scenepic)
                sceneimg = cv2.cvtColor(sceneimg, cv2.COLOR_BGR2RGB)
                sceneimg = cv2.flip(sceneimg,flipCode=0)
                mask_obj = np.ones((np.shape(sceneimg)[0],np.shape(sceneimg)[1],4))
                mask_main_light = (sceneimg[:,:,2] == 255) & (sceneimg[:,:,0]==0)
                mask_obj[:,:,0] = mask_main_light
                mask_main_dark = (sceneimg[:,:,2] > 0) & (sceneimg[:,:,2] < 255) & (sceneimg[:,:,0]==0)
                mask_obj[:,:,1] = mask_main_dark
                mask_glow_light = (sceneimg[:,:,0] == 255) & (sceneimg[:,:,2]==0)
                mask_obj[:,:,2] = mask_glow_light
                mask_glow_dark = (sceneimg[:,:,0] > 0) & (sceneimg[:,:,0] < 255) & (sceneimg[:,:,2]==0)
                mask_obj[:,:,3] = mask_glow_dark
                np.save(dir_path+'\\ambient_city_masks\\'+filename+'.npy',mask_obj)     
    return