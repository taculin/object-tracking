# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:14:53 2018

@author: alquine
"""

import cv2

FPS = 8


def col(i):
    C = [(0,255,0),(102,102,255),(255,102,255),(255,255,102),(102,102,0),(153,204,255),(153,0,153),(255,102,0)]
    return C[i%len(C)]

import Tkinter, tkFileDialog, tkMessageBox
def openf():    
    Tkinter.Tk().withdraw()
    path = tkFileDialog.askopenfilename()
    fname = path.split('/').pop().encode('ascii','ignore')
    return fname
# read the existing NTXY records
def f2l(fname):
    lst = []
    try:    
        with open(fname.split('.')[0]+'.dat','r') as file:
            for line in file:
                row = [int(c) for c in line.split(' ')]
                lst.append(row)
        print len(lst),'rows read'
    except IOError:
        print 'No data file found'
    return lst    
def readf():
    f = openf()
    if f:
        cap = cv2.VideoCapture(f)
        return cap, f2l(f), f
    else:
        return None, None, None

#fc,fh,fw,fps
def capStat(cap):
    return int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FPS))


# overwrite the NTXY records    
def l2f(R,fname):
    with open(fname.split('.')[0]+'.dat','w') as file:
        for row in R:
            if len(row)<5:
                file.write(' '.join(map(str, row))+"\n")



def lop(f,R,I,i,n):
    key = cv2.waitKey(0)
    # inc/dec car number
    if key == ord('+'):
        n=n+1
    elif key == ord('-'):
        if n>=0:
            n=n-1
    # delete most recent coord (pop stack)
    elif key == ord('d'):
        print 'removed recent item ',R.pop()
    # overwrite data to file
    elif key == ord('s'):
        l2f(R,f)       
    # navigate frame: next/back commands 
    elif key == ord('l'):
        i=i+1
        if i>=I:
            i=0
    elif key == ord('r'):
        i=i-1
        if i<0:
            i=I-1
    elif key == ord(' '):
        n,i,x,y =  R[-1]
    elif key == ord('q') or key == 27:
        if len(R)> 0 and (tkMessageBox.askquestion("Closing window", "You want to save the coordinates first?", icon='warning') == 'yes'):
            l2f(R,f)
    return key,i,n

def getImg(cap,i):    
    t = (i/FPS)*1000+((i%FPS)*(1000.0/FPS))
    try:
        cap.set(cv2.CAP_PROP_POS_MSEC,t)
        print 'fetching image at',cap.get(cv2.CAP_PROP_POS_MSEC)
        ret, I = cap.read()
        return I
    except:
        return None
    
def shoImg(f,img,N,i,R):
    path = [r for r in R if r[1]<=i and r[1]>=i-10]
    for n,t,x,y in path:
        cv2.circle(img, (x,y),2,col(n), -1)   
    # stats
    currClicked = [n for (n,t,x,y) in path if t==i]
    currCarClicked = [n for n in currClicked if n==N]
    h,w = img.shape[:2]
    c = col(N)
    s = .4    
    frame = '[f:'+str(i)+','+str(len(currClicked))+']'
    count = '[c:'+str(N)+','+str(len(currCarClicked))+']'
    cv2.putText(img,frame,(5,5),cv2.FONT_HERSHEY_SIMPLEX,s,c)
    cv2.putText(img,count,(60,5),cv2.FONT_HERSHEY_SIMPLEX,s,c)
    # show
    cv2.imshow(f,img)

     

def main():   
    cap,R,f = readf()
    if not cap:
        return
    i,N = 0,0
    img=getImg(cap,i)
    shoImg(f,img,N,i,R)

    
    def onMseClk(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            img=getImg(cap,i)
            R.append([N,i,x,y])
            shoImg(f,img,N,i,R)
            print 'added (',x,',',y,') for car ',N,' at frame ',i
        if event == cv2.EVENT_MOUSEMOVE:
            img=getImg(cap,i)
            h,w=img.shape[:2]
            cv2.putText(img,str(x)+','+str(y),(w-200,40),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255))
            shoImg(f,img,N,i,R)
            
    cv2.setMouseCallback(f, onMseClk)
    
    
    fcs,_,_,fps = capStat(cap)
    L = fcs/fps*FPS
    print 'len:',L,' frcount:',fcs,'rate:',fps
    key=0
    while not key==ord('q'):
        img=getImg(cap,i)
        shoImg(f,img,N,i,R)
        key,i,N = lop(f,R,L,i,N)
        if key in [ord('l'),ord('r')]:
            print i,cap.get(cv2.CAP_PROP_POS_MSEC)

    cap.release()
    cv2.destroyAllWindows()
            