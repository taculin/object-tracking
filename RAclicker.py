# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:14:53 2018

Version: 2018 Sep 09

@author: alquine
"""

import cv2

def decom(fname):
    fn = fname.split('.')[0]
    i=0
    cap = cv2.VideoCapture(fn+'.mp4')
    last = 5# int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while(cap.isOpened()) and i<last:
        ret, frame = cap.read()        
        if ret==True:
            frame = cv2.resize(frame, None, fx=0.75, fy=0.75)
            cv2.imwrite(fn+"{0:0>5}".format(i)+'.jpg',frame)    
            i=i+1
    print i,'frames extracted'
    cap.release()
    cv2.destroyAllWindows()

def col(i):
    C = [(0,0,255),(0,255,255),(255,127,0),(123,255,0),(255,0,255),(27,152,214),(140,0,255),(226,97,179),(237,255,0)]
    return C[i%len(C)]

import Tkinter, tkMessageBox, tkSimpleDialog
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
import os,datetime
def l2f(R,fn):
    try:
        os.rename(fn+'.ntxy',datetime.datetime.now().strftime("%Y%m%d-%H%M")+'H.ntxy')
    except:
        print 'error creating backup'
    with open(fn+'.ntxy','w') as file:
        for row in R:
            if len(row)<5:
                file.write(' '.join(map(str, row))+"\n")



def lop(f,R,i,n):
    key = cv2.waitKey(0)
  
    if key == ord('+'):     # inc car number
        n=n+1
    elif key == ord('-'):   # dec car number
        if n>=0:
            n=n-1
    elif key == ord('d'):   # delete current i,n
        ind = [idx for idx,val in enumerate(R) if val[0]==n and val[1]==i]
        if len(ind)>0:
            print 'removing',R[ind[0]]
            del R[ind[0]]
        else:
            print 'nothing to delete'
    # overwrite data to file
    elif key == ord('s'):
        l2f(R,f)       
    elif chr(key) in ['l',' ']:   # next frame
        i=i+1
    elif key == ord('r'):   # previous frame 
        i=i-1
        if i<0:
            i=0
            print 'cant go to previous frame'
    elif key == ord('z'):   # go to frame previously clicked 
        n,i,x,y =  R[-1]
    elif chr(key) in ['c','q','f'] or key == 27:
        root = Tkinter.Tk()
        root.withdraw()
        if key == ord('c'):
            cc = tkSimpleDialog.askinteger('car number','Jump to Car Number',initialvalue=n)
            if cc is not None:
                n = cc
        elif key == ord('f'):
            cc = tkSimpleDialog.askinteger('frame number','Go to Frame Number',initialvalue=i)
            if cc is not None:
                i = cc
        elif key in [ord('q'),27]: # quit q or esc
            if len(R)> 0 and (tkMessageBox.askquestion("Closing window", "You want to save the coordinates first?", icon='warning') == 'yes'):
                l2f(R,f)
                print 'coordinates saved at',f
            else:
                print len(R),'program exited'
        root.destroy()    
    else:
        print 'ignoring',key
    
    return key,i,n

def getImg(fname,i):    
    try:
        I = cv2.imread(fname+"{0:0>5}".format(i)+'.jpg')        
#        print 'fetching image at',t,cap.get(cv2.CAP_PROP_POS_MSEC)        
        return I
    except:
        print 'an error ooccured while fetching an image'
        return None
    
def shoImg(f,img,N,i,R):
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
    cv2.putText(img,frame,(15,20),cv2.FONT_HERSHEY_SIMPLEX,s,c)
    cv2.putText(img,count,(15,40),cv2.FONT_HERSHEY_SIMPLEX,s,c)
    # show
    cv2.imshow(f,img)
    
def click(f):
    f=f.split('.')[0]
    R=f2l(f)
    i,N = 0,0
    img=getImg(f,i)
    shoImg(f,img.copy(),N,i,R)
    
    def onMseClk(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            im = img.copy()
            R.append([N,i,x,y])
            shoImg(f,im,N,i,R)
            print 'added (',x,',',y,') for car ',N,' at frame ',i
        if event == cv2.EVENT_MOUSEMOVE:
            im = img.copy()
            h,w=img.shape[:2]
            cv2.putText(im,str(x)+','+str(y),(w-200,40),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255))
            shoImg(f,im,N,i,R)
    cv2.namedWindow(f)        
    cv2.setMouseCallback(f, onMseClk)
    
    key=0
    while not key in [ord('q'),27]:
        img=getImg(f,i)        
        if (img is None) and (i>0):
            i = 0
            img = getImg(f,i)
            print 'wrapping around'
        shoImg(f,img.copy(),N,i,R)
        key,i,N = lop(f,R,i,N)


    cv2.destroyAllWindows()
            
    
