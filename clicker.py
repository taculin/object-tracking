# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:14:53 2018

@author: alquine
"""

import cv2

    
#filename is full (include extension)
def v2pALL(fnameWithExtn, fps=4):
    cap = cv2.VideoCapture(fnameWithExtn)
    last, frate =  int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), int(cap.get(cv2.CAP_PROP_FPS))
    k=frate/fps 
    i,j=0,0
    print frate,k,'extracting', (last/k), 'items (out of', last,')'
    while(cap.isOpened()) and i<last and i<10:
        ret, frame = cap.read()
        if ret==True and (j%k)==0:
            cv2.imwrite(fnameWithExtn.split('.')[0]+"_r{0:0>2}".format(fps)+"_n{0:0>5}".format(i)+'.jpg',frame)    
            i=i+1
            print '.',
        j=j+1
    cap.release()
    cv2.destroyAllWindows()

def col(i):
    C = [(0,255,0),(102,102,255),(255,102,255),(255,255,102),(102,102,0),(153,204,255),(153,0,153),(255,102,0)]
    return C[i%len(C)]

import Tkinter, tkFileDialog, tkMessageBox
# read the existing NTXY records
def f2l(fname):
    lst = []
    try:    
        with open(fname+'.dat','r') as file:
            for line in file:
                row = [int(c) for c in line.split(' ')]
                lst.append(row)
        print len(lst),'rows read'
    except IOError:
        print 'No data file found'
    return lst    

# overwrite the NTXY records    
def l2f(R,fname):
    with open(fname+'.dat','w') as file:
        for row in R:
            if len(row)<5:
                file.write(' '.join(map(str, row))+"\n")



def lop(f,R,I,i,n):
    key = cv2.waitKey(0)
  
    if key == ord('+'):     # inc car number
        n=n+1
    elif key == ord('-'):   # dec car number
        if n>=0:
            n=n-1
    elif key == ord('d'):   # delete most recent coord (pop stack)
        print 'removed recent item ',R.pop()
    # overwrite data to file
    elif key == ord('s'):
        l2f(R,f)       
    
    elif key == ord('l'):   # next frame
        i=i+1
        if i>=I:
            i=0
    elif key == ord('r'):   # previous frame 
        i=i-1
        if i<0:
            i=I-1
    elif key == ord(' '):   # go to frame previously clicked 
        n,i,x,y =  R[-1]
    elif key == ord('q') or key == 27: # quit q or esc
        root = Tkinter.Tk()
        root.withdraw()
        if len(R)> 0 and (tkMessageBox.askquestion("Closing window", "You want to save the coordinates first?", icon='warning') == 'yes'):
            l2f(R,f)
            print 'coordinates saved at',f
        else:
            print len(R),'coordinates discarded'
        root.destroy()    
    return key,i,n

#we need to modularize this to catch input errors
def getImg(fname,i):   
    return cv2.imread(fname+"_n{0:0>5}".format(i)+'.jpg')
    
def shoImg(f,img,N,i,R):
    path = [r for r in R if r[1]<=i and r[1]>=i-10]
    for n,t,x,y in path:
        cv2.circle(img, (x,y),2,col(n), -1)   
    # stats
    currClicked = [n for (n,t,x,y) in path if t==i]
    currCarClicked = [n for n in currClicked if n==N]
    h,w = img.shape[:2]
    c = col(N)
    s = .6    
    frame = '[f:'+str(i)+','+str(len(currClicked))+']'
    count = '[c:'+str(N)+','+str(len(currCarClicked))+']'
    cv2.putText(img,frame,(20,40),cv2.FONT_HERSHEY_SIMPLEX,s,c)
    cv2.putText(img,count,(100,40),cv2.FONT_HERSHEY_SIMPLEX,s,c)
    # show
    cv2.imshow(f,img)
    
def main(f,L):   
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
            
    cv2.setMouseCallback(f, onMseClk)
    key=0
    while not key==ord('q'):
        img=getImg(f,i)
        shoImg(f,img.copy(),N,i,R)
        key,i,N = lop(f,R,L,i,N)
        if key in [ord('l'),ord('r')]:
            print i

    cv2.destroyAllWindows()
            
