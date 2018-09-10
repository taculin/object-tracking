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
    
def recon(fn,lastFr=100, scale=.25):
    fn = fn.split('.')[0]
    
    H = np.array(json.load(open(fn+'.map','r')))
    
    L = []
    with open(fn+'.ntxy','r') as file:
        for line in file:
            L.append([eval(w) for w in line.split(' ')])
    
    T = cv2.perspectiveTransform(np.array(L).reshape((-1,1,2)),H)
    
    LT = [[L[i][0],L[i][1],L[i][2],L[i][3],T[i][0],T[i][1]] for i in range(len(L))]

    try:
        os.rename(fn+'_H.avi',datetime.datetime.now().strftime("%Y%m%d-%H%M")+'H.avi')
    except:
        print 'nothing to backup'

    h,w,_ = cv2.imread(fn+"{0:0>5}".format(0)+'.jpg').shape        
    out = cv2.VideoWriter(fn+'_H.avi',cv2.VideoWriter_fourcc(*"DIVX"),28,(w*2*scale,h*scale))

    
    for i in range(lastFr):
        im1 = cv2.imread(fn+"{0:0>5}".format(i)+'.jpg')        
        im2 = cv2.warpPerspective(im1, H)
        D = [v for v in LT if (i-50)<=v[1]<=i]
        for n,t,x,y,u,v in D:
            cv2.circle(im1,(x,y),2,col(n),2)
            cv2.circle(im2,(u,v),2,col(n),2)
            if i==t:
                cv2.putText(im1,str(n),(x,y),cv2.FONT_HERSHEY_SIMPLEX,.7,col(n),1)        
                cv2.putText(im2,str(n),(u,v),cv2.FONT_HERSHEY_SIMPLEX,.7,col(n),1)                 
 
        im3 = np.hstack((cv2.resize(im1,None,fx=scale,fy=scale),cv2.resize(im2,None,fx=scale,fy=scale)))
        out.write(im3)
        if i%100==0:
            print 'now at frame',i,'/',lastFr
            
    
    out.release()
        

        
    

    
