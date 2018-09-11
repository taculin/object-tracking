# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:14:53 2018

Version: 2018 Sep 09

@author: alquine
"""

import cv2, numpy as np

def col(i):
    C = [(0,0,255),(0,255,255),(255,127,0),(123,255,0),(255,0,255),(27,152,214),(140,0,255),(226,97,179),(237,255,0)]
    return C[i%len(C)]

import Tkinter, tkMessageBox, os, datetime, json

def mapModel(fn):
    fn = fn.split(' ')[0]

    Img = {}
    Img[0] = cv2.imread(fn+"{0:0>5}".format(0)+'.jpg')        
    Img[1] = cv2.imread(fn+'.jpg')  
    sh,_,_ = Img[0].shape
    mh,_,_ = Img[1].shape    
    ratio = .9*sh/mh
    Img[1] = cv2.resize(Img[1],None,fx=ratio, fy=ratio)
    
    Lst = [[],[]]

    Win = ['original perspective','target perspective',0]
    for i in range(2):
        cv2.imshow(Win[i],Img[i])

    def end(k):
        root = Tkinter.Tk()
        root.withdraw()
        if idx() == 0:
            answer = tkMessageBox.askyesnocancel("Terminating", "Compute and save homography matrix H?")
            if answer is True:
                H,_ = cv2.findHomography(np.array(Lst[0]),np.array(Lst[1]))
                try:
                    os.rename(fn+'.map',datetime.datetime.now().strftime("%Y%m%d-%H%M")+'H.map')
                except:
                    print 'error creating backup'
                with open(fn+'.map','w') as file:
                    json.dump(H.tolist(),file)
                print 'Matrix saved'
            elif answer is None:
                k = 0
        else:
            answer = tkMessageBox.askokcancel("Warning", "Mapping not complete. Are you sure you want to exit?")
            if answer is not True:
                k = 0
        root.destroy()
        return k

    def undo():
        if Win[2] > 0:
            del Lst[idx(-1)][-1]
            cv2.setMouseCallback(Win[idx()], onMseClk)            
            print 'last item removed'
        else:
            print 'Cant undo anymore'

    def idx(i=0):
        Win[2] += i
        return Win[2]%2
    
    def plotAndShow(event,xx=None,yy=None):
        im = Img[idx()].copy()
        for k,v in enumerate(Lst[idx()]):
            x,y = v
            cv2.putText(im,str(k),(x,y),cv2.FONT_HERSHEY_SIMPLEX,.5,col(k))            
            cv2.circle(im, (x,y),2,col(k), -1)  
        if event == 1:
            _,w,_ = im.shape
            cv2.putText(im,str(xx)+','+str(yy),(w-200,40),cv2.FONT_HERSHEY_SIMPLEX,0.75,(10,200,0))
        cv2.imshow(Win[idx()],im)
                                
    def onMseClk(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            Lst[idx()].append((x,y))
            plotAndShow(0)
            print Win[idx()],'[',(len(Lst[idx()])-1),']: (',x,',',y,')' 
            cv2.setMouseCallback(Win[idx(1)], onMseClk)
        if event == cv2.EVENT_MOUSEMOVE:
            plotAndShow(1,x,y)
        
    cv2.setMouseCallback(Win[idx()], onMseClk)
    k,i=0,0
    while k not in [ord('q'),27]:
        plotAndShow(0)
        k = cv2.waitKey(0)
        if chr(k) == 'd':
            undo()
        elif chr(k) == 'l':
            i +=1
            Img[0] = cv2.imread(fn+"{0:0>5}".format(i)+'.jpg')
        elif chr(k) == 'r':
            i = 0 if i==0 else (i-1)
            Img[0] = cv2.imread(fn+"{0:0>5}".format(i)+'.jpg')            
        elif k in [ord('q'),27]:
            k = end(k)                
    print Lst
    cv2.destroyAllWindows()



    
    #==============================

#specify the last Frame. Also scale can be adjusted, although 0.25 or 1/4 will fit better in standard screen 
def recon(fn,lastFr=100, scale=.25):
    fn = fn.split('.')[0]
    
    H = np.array(json.load(open(fn+'.map','r')))
    
    L = []
    with open(fn+'.ntxy','r') as file:
        for line in file:
            r = [eval(w) for w in line.split(' ')]
            if r[1]<=lastFr:        # exclude unnecessaary rows right from the start
                L.append(r)
    L = np.array(L,dtype=np.float32)
    
    T = cv2.perspectiveTransform(L[:,2:4].reshape((-1,1,2)),H)
    print 'Transforming',len(L),' ntxy entries.'
        
    L = np.concatenate((L,T.reshape((-1,2))),axis=1)
    

    try:
        os.rename(fn+'_H.avi',datetime.datetime.now().strftime("%Y%m%d-%H%M")+'H.avi')
    except:
        print 'nothing to backup'

    h,w,_ = cv2.imread(fn+"{0:0>5}".format(0)+'.jpg').shape        
    out = cv2.VideoWriter(fn+'_H.avi',cv2.VideoWriter_fourcc(*"DIVX"),28,(int(w*2*scale),int(h*scale)),True)
    
    for i in range(lastFr):
        k = cv2.waitKey(0)
        im1 = cv2.imread(fn+"{0:0>5}".format(i)+'.jpg')        
        im2 = cv2.warpPerspective(im1, H, (w,h))
        D = [v for v in L if (i-50)<=v[1]<=i]
        for n,t,x,y,u,v in D:
            n,t = int(n),int(t)
            cv2.circle(im1,(x,y),2,col(n),2)
            cv2.circle(im2,(u,v),2,col(n),2)
            if i==t:
                cv2.putText(im1,str(n),(x,y),cv2.FONT_HERSHEY_SIMPLEX,.7,col(n),1)        
                cv2.putText(im2,str(n),(u,v),cv2.FONT_HERSHEY_SIMPLEX,.7,col(n),1)                 
 
        im3 = np.hstack((cv2.resize(im1,None,fx=scale,fy=scale),cv2.resize(im2,None,fx=scale,fy=scale)))
        out.write(im3)
        if i%100==0:
            print 'now at frame',i,'/',lastFr,'. Press q or esc to abort'
        if k in [27,ord('q')]:
            break
    out.release()
