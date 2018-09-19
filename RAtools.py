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

import Tkinter, tkMessageBox,tkSimpleDialog, os, datetime, json

def decom(fname):
    fn = fname.split('.')[0]
    i=0
    cap = cv2.VideoCapture(fn+'.mp4')
    last = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if int(cv2.__version__[0])==3 else int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    while cap.isOpened():
        ret, frame = cap.read()        
        if ret==True:
            frame = cv2.resize(frame, None, fx=0.75, fy=0.75)
            cv2.imwrite(fn+"{0:0>5}".format(i)+'.jpg',frame)
            if i%500 is 0:
                cv2.imshow('win',frame)
                print 'Now at frame',i,'/',last,'. Hit q to abort'
            i=i+1
            if (cv2.waitKey(1) & 0xFF) in [27,ord('q')]:
                break
    print i,'frames extracted'
    cap.release()
    cv2.destroyAllWindows()


# read the existing NTXY records
def f2l(fname):
    lst = []
    try:    
        with open(fname+'.ntxy','r') as file:
            for line in file:
                row = [int(c) for c in line.split(' ')]
                lst.append(row)
        print len(lst),'rows read'
    except IOError:
        print 'No data file found'
    return lst    

# overwrite the NTXY records    
def l2f(R,fn):
    try:
        os.rename(fn+'.ntxy',datetime.datetime.now().strftime("%Y%m%d-%H%M")+'H.ntxy')
    except:
        print 'error creating backup'
    with open(fn+'.ntxy','w') as file:
        for row in R:
            if len(row)<5:
                file.write(' '.join(map(str, row))+"\n")

def lop(tupl):
    f,img,n,i,R,auto = tupl
    key = cv2.waitKey(0) & 0xFF
  
    if key == ord('+'):     # inc car number
        tupl[2]=n+1
    elif key == ord('-'):   # dec car number
        if n>=0:
            tupl[2]=n-1
    elif key == ord('a'):   # toggles the auto next feature (frame advances after a click)
        tupl[5] = not tupl[5]
    elif key == ord('d'):   # delete current i,n
        ind = [idx for idx,val in enumerate(R) if val[0]==n and val[1]==i]
        if len(ind)>0:
            print 'removing',R[ind[0]]
            del R[ind[0]]
        else:
            print 'nothing to delete'
    elif key == ord('s'):                   # overwrite data to file
        l2f(R,f)       
    elif key in [ord('l'),ord(' ')]:   # next frame
        tupl[3]=i+1
        tupl[1]=getImg(f,i+1)
    elif key == ord('r'):   # previous frame 
        if i>1:
            tupl[3]=i-1
            tupl[1]=getImg(f,i-1)
    elif key == ord('z'):   # go to frame previously clicked 
        tupl[3] =  R[-1][1]
    elif chr(key) in ['c','q','f'] or key == 27:
        root = Tkinter.Tk()
        root.withdraw()
        if key == ord('c'):
            cc = tkSimpleDialog.askinteger('car number','Jump to Car Number',initialvalue=n)
            if cc is not None:
                tupl[2] = cc
        elif key == ord('f'):
            cc = tkSimpleDialog.askinteger('frame number','Go to Frame Number',initialvalue=i)
            if cc is not None:
                tupl[3] = cc
                tupl[1] = getImg(f,cc)
        elif key in [ord('q'),27]: # quit q or esc
            if len(R)> 0 and (tkMessageBox.askquestion("Closing window", "You want to save the coordinates first?", icon='warning') == 'yes'):
                l2f(R,f)
                print 'coordinates saved at',f
            else:
                print len(R),'program exited'
        root.destroy()    
    else:
        print 'ignoring',key
    
    return key

def getImg(fname,i):    
    try:
        I = cv2.imread(fname+"{0:0>5}".format(i)+'.jpg')        
#        print 'fetching image at',t,cap.get(cv2.CAP_PROP_POS_MSEC)        
        return I
    except:
        print 'an error ooccured while fetching an image'
        return None
    
def shoImg(tupl, img):
    f,_,N,i,R,auto = tupl
    c = col(N)
    s = .5    
    path = [r for r in R if r[1]<=i and r[1]>=i-10]
    for n,t,x,y in path:
        if i==t and n==N:            
            cv2.circle(img, (x,y),4,col(n), -1)   
            cv2.circle(img, (x,y),2,(0,0,0), -1)   
            cv2.putText(img,str(n),(x,y),cv2.FONT_HERSHEY_SIMPLEX,s,col(n))            
        else:
            cv2.circle(img, (x,y),2,col(n), -1)   
    # stats
    currClicked = [n for (n,t,x,y) in path if t==i]
    currCarClicked = [n for n in currClicked if n==N]
    frame = 'F:'+str(i)+','+str(len(currClicked))
    count = 'C:'+str(N)+','+str(len(currCarClicked))
    autonext = 'Auto: ON' if auto is True else 'Auto: OFF'
    cv2.putText(img,frame,(15,20),cv2.FONT_HERSHEY_SIMPLEX,s,c)
    cv2.putText(img,count,(15,40),cv2.FONT_HERSHEY_SIMPLEX,s,c)
    cv2.putText(img,autonext,(15,60),cv2.FONT_HERSHEY_SIMPLEX,s,c)    
    # show
    cv2.imshow(f,img)
    
def click(f, autonext=False):
    f=f.split('.')[0] 
    T = [f,getImg(f,0),0,0,f2l(f), autonext]              # pack nonlocal variables to a mutable tuple
    shoImg(T,T[1].copy())
    
    def onMseClk(event,x,y,flags,param):
        f,img,N,i,R,auto = T                         # unpactk the tuple
        if event == cv2.EVENT_LBUTTONDOWN:
            R.append([N,i,x,y])
            print 'added (',x,',',y,') for car ',N,' at frame ',i
            if auto is True:
                T[1] = getImg(f,i+1)                # update the frame to the next
                T[3] = i+1                          # increment i and repack updated values
            shoImg(T,T[1].copy())
        if event == cv2.EVENT_MOUSEMOVE:
            im = img.copy()
            h,w=im.shape[:2]
            cv2.putText(im,str(x)+','+str(y),(w-200,40),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255))
            shoImg(T,im)
    cv2.namedWindow(f)        
    cv2.setMouseCallback(f, onMseClk)
    
    key=0
    while not key in [ord('q'),27]:
        shoImg(T,T[1].copy())
        key = lop(T)
    cv2.destroyAllWindows()

#=======================

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
        k = cv2.waitKey(0) & 0xFF
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

#specify the last Frame. Also scale can be adjusted, although 0.4 or less than 1/2 will fit better in standard screen 
def recon(fn,lastFr=100, scale=.4):
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
            cv2.putText(im3,'PREVIEW',(10,int(h*scale*.5)),cv2.FONT_HERSHEY_SIMPLEX,int(20*scale),(255,255,255),int(25*scale))
            cv2.imshow('reconstructing video',im3)
            print 'now at frame',i,'/',lastFr,'. Press q or esc to abort'
            print 'aborting at frame',i
            break
    print 'saving file'
    cv2.destroyAllWindows()
    out.release()
    

import sys
if len(sys.argv)>=3:
    if sys.argv[1]=='decom':
        decom(sys.argv[2])
    elif sys.argv[1]=='click':
        if len(sys.argv)==3:
            click(sys.argv[2])
        elif len(sys.argv)==4 and sys.argv[3].lower()=='on':
            click(sys.argv[2],True)
    elif sys.argv[1]=='map':
        mapModel(sys.argv[2])
    elif sys.argv[1]=='recon':
        if len(sys.argv)>4:
            recon(sys.argv[2],sys.argv[3],sys.argv[4])
        elif len(sys.argv)>3:
            recon(sys.argv[2],sys.argv[3])
        elif len(sys.argv)==3:
            recon(sys.argv[2])            
    else:
        print 'Cant identify the method. Pls try again'
else:
    print 'Pls specify the method to run. Try again.'