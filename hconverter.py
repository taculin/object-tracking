# -*- coding: utf-8 -*-
"""
Created on Mon Jun 04 17:04:09 2018

@author: alquine
"""

import cv2
import numpy as np


# read the row records. probably first line is a header description
def dread(fname,separator):
    lst = []
    header = []
    try:    
        with open(fname,'r') as file:
            for line in file:
                row = line.split(separator)
                if not row[0].isdigit():
                    header = row
                elif row[3] != '':
                    lst.append(map(eval,row))
        print len(lst),'rows read'
    except IOError:
        print fname,'not file found'
    return header, lst    

def mread(fn,mn):
    mod,lst = dread(fn+'.tsv','\t')
    desc,dim,pmap = eval(mod[mn])
    return [[i,(vx,vy),(px,py),trans((vx,vy),pmap)] for i,vx,vy,px,py in lst]
    

def trans(point, pmap):
    x,y = point
    s,xt,yt,ymax = pmap
    return ((x+xt)*s, (ymax-(y+yt))*s)

def showm(im,lst):
    for n,v,p,h in lst:
        print n,h
        x,y=h
        cv2.putText(im,str(n),(int(x),int(y)),cv2.FONT_HERSHEY_SIMPLEX,.5,(175,175,0),1)
        cv2.circle(im,(int(x),int(y)),2,(0,175,0),3)
    cv2.imshow('win',im)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
#shows the model and the mapping of visio coords to the jpeg of model number    
def main_m(fn='shopwise',modNum=1):
    xys = mread(fn,modNum)
    showm(cv2.imread(fn+'_m'+str(modNum)+'.jpg'),xys)
    
    
#shows the model, world, warped world    
def main_mf(fn='shopwise',mN =1):
    imgm = cv2.imread(fn+'_m'+str(mN)+'.jpg')
    imgf = cv2.imread(fn+'00000'+'.jpg')
    
    xys = mread(fn,mN)
    H,M = cv2.findHomography(np.array([p for i,v,p,h in xys]),np.array([h for i,v,p,h in xys]),cv2.RANSAC)
    
    h,w,c = imgm.shape
    imH = cv2.warpPerspective(imgf,H,(w,h))
    
    cv2.imshow('win',imH)
    cv2.imshow('won',imgm)
    cv2.imshow('wan',imgf)
    cv2.waitKey()
    cv2.destroyAllWindows()


def plot_f(im,i,ntxy,l):
    cv2.putText(im,str(i),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,150,255))    
    for n,t,x,y in ntxy:
        if t<=i and t>=i-l:
            cv2.circle(im,(int(x),int(y)),1,(0,175,0),2)
            if i==t:
                cv2.putText(im,str(int(n)),(int(x),int(y)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),1)
    return im

    
#shows n frames of the world and warped world - with ntxy, catenates them, save 
def main_f(fn,mn,last):
    xys = mread(fn,mn)
    H,M = cv2.findHomography(np.array([p for i,v,p,h in xys]),np.array([h for i,v,p,h in xys]),cv2.RANSAC)

    imG = cv2.imread(fn+'_m'+str(mn)+'.jpg')
    h,w,c = imG.shape    

    _,ntxy = dread(fn+'_ntxy.dat',' ')
    if ntxy:
        ntxy = np.array(ntxy,dtype=np.float32)
        nt = ntxy[:,0:2]
        xy = ntxy[:,2:4]
        new_xy = cv2.perspectiveTransform(xy.reshape((-1,1,2)),H)
        htxy = np.concatenate((nt,new_xy.reshape((-1,2))),axis=1)
    else:
        htxy=[]
#    fcc = cv2.VideoWriter_fourcc(*"XVID")
    print 'finding codec'
    try:
        out = cv2.VideoWriter('weh'+str(mn)+'.mpg',-1,20,(w,h))
    except:
        print 'error'
        return
    print 'codec found'
    i=0
    
    for i in range(last):
        imG = cv2.imread(fn+"{0:0>5}.jpg".format(i))
        imGp = plot_f(imG.copy(),i,ntxy,50)
        imGrs = cv2.resize(imGp.copy(),(w,h),interpolation=cv2.INTER_AREA)
        
        imH = cv2.warpPerspective(imG,H,(w,h))                
        imHp = plot_f(imH,i,htxy,50)
        imgsbs = np.hstack((imHp,imGrs))
        out.write(imgsbs)        
        cv2.imshow('win',imgsbs)        
        if cv2.waitKey(1) == 27:
            print 'terminating. esc key pressed'
            break
    
    out.release()
    cv2.destroyAllWindows()



# same as above, shows 3 windows
def main_show3(fn,mn,last):
    xys = mread(fn,mn)
    H,M = cv2.findHomography(np.array([p for i,v,p,h in xys]),np.array([h for i,v,p,h in xys]),cv2.RANSAC)

    imM = cv2.imread(fn+'_m'+str(mn)+'.jpg')
    h,w,c = imM.shape    

    _,ntxy = dread(fn+'_ntxy.dat',' ')
    htxy = []
    if ntxy:
        ntxy = np.array(ntxy,dtype=np.float32)
        nt = ntxy[:,0:2]
        xy = ntxy[:,2:4]
        new_xy = cv2.perspectiveTransform(xy.reshape((-1,1,2)),H)
        htxy = np.concatenate((nt,new_xy.reshape((-1,2))),axis=1)

    i=0
    
    for i in range(last):
        imG = cv2.imread(fn+"{0:0>5}.jpg".format(i))
        imGp = plot_f(imG.copy(),i,ntxy,50)
        imGrs = cv2.resize(imGp,(w,h),interpolation=cv2.INTER_AREA)
        cv2.imshow('orig',imGrs)
        
        imH = cv2.warpPerspective(imG,H,(w,h))                
        imHp = plot_f(imH,i,htxy,50)
        cv2.imshow('warped',imHp)

        cv2.imshow('model',plot_f(imM,i,htxy,50))       
        if cv2.waitKey(1) == 27:
            print 'terminating. esc key pressed'
            break
        
    cv2.destroyAllWindows()
    
    
int_regis = 'Regis\MAH07553\MAH07553'
int_westdrive = 'west drive\mar\mar'
int_cubao = 'Shopwise-Cubao\MAH07557\MAH07557'

codecs = ['DIVX', 'IYUV', 'CRAM', 'MSVC', 'WHAM', 'CVID', 'PIM1', 'MJPG', 'MP42', 'DIV3', 'U263', 'I263', 'FLV1']
