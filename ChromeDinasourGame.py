
# coding: utf-8

# In[22]:


import cv2
import numpy as np
import pyautogui
import math

GREEN=[0,255,0]
BLUE=[255,0,0]
RED=[0,0,255]

def preprocess(frame):
    image=cv2.cvtColor(frame,cv2.COLOR_BGR2LAB)
    image=cv2.inRange(image[:,:,2],140,220)
    kernel = np.ones((5,5),np.uint8)
    image=cv2.morphologyEx(image,cv2.MORPH_OPEN,kernel)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel,iterations=5)
    return image
    

def findLargestContour(contours):
    largestArea=-10000
    cIndex=-1
    for ID in range(len(contours)):
        area=cv2.contourArea(contours[ID])
        if(area>largestArea):
            largestArea=area
            cIndex=ID
    return cIndex,contours[cIndex]

def getDefectCount(img,preprocessedFrame,defects,largestContour):
    # so defects has 4 values [s,e,ptOfDisobedience,dist]
    fingerCount=0
    for i in range(defects.shape[0]):
        s,e,pt,d = defects[i,0]
        s=tuple(largestContour[s][0])
        e=tuple(largestContour[e][0])
        pt=tuple(largestContour[pt][0])
        cv2.line(img,s,e,RED,2)
        cv2.line(img,s,pt,BLUE,2)
        cv2.line(img,s,pt,BLUE,2)
        cv2.circle(img,pt,2,BLUE,-1) # circle, center, radius, color, fill
        
        a=np.sqrt(((s[0]-e[0])**2 + (s[1]-e[1])**2))
        b=np.sqrt(((s[0]-pt[0])**2 + (s[1]-pt[1])**2))
        c=np.sqrt(((pt[0]-e[0])**2 + (pt[1]-e[1])**2))
        
        # see the angle formed by triangle
        theta=(math.acos((b**2+c**2-a**2)/(2*b*c)))*180/3.14
        
        if(theta<90):
            fingerCount+=1
            cv2.circle(img,pt,2,BLUE,-1) # circle, center, radius, color, fill
            
            
#         print theta
    
    cv2.imshow('temp',img)
    return fingerCount
            
        
    

#frame dimensions
fx=50
fy=60
fw=300
fh=300

def action():
    cap=cv2.VideoCapture(0) 
#     frame=cv2.imread('hand.jpg')
    while(True):
        ret,frame=cap.read()
        try:
            ret=True
            if(ret==False):
                print('Unable to read image')
                continue

            # read 
    #         frame=cv2.imread('hand.jpg')        

            # draw a frame around the image
            detectionFrame=frame[fx:fx+fh,fy:fy+fw].copy()
            cv2.rectangle(frame,(fx,fy),(fx+fh,fy+fw),(0,255,255),3)
            preprocessedFrame=preprocess(detectionFrame)

            # finding the largest contour by area
            _,contours,_=cv2.findContours(preprocessedFrame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cIndex,largestContour=findLargestContour(contours)


            # finding defects in image
            cv2.imshow('preprocessedImage',preprocessedFrame)


            # finding defects
            hull = cv2.convexHull(largestContour,returnPoints = False)
            defects = cv2.convexityDefects(largestContour,hull)


            #finding if the frame is of open or closed hand
            countDefects=getDefectCount(detectionFrame,preprocessedFrame,defects,largestContour) # this has to be checked

            if (countDefects>3):
                pyautogui.press('space')
    #         else:
    #             print 'Fingers seen is : ' , countDefects




            cv2.imshow('frame',frame)
            cv2.imshow('preprocessedImage',preprocessedFrame)
        except:
            continue

        k = cv2.waitKey(1) & 0xFF
        if k==ord('q') or k==ord('Q'):
            cv2.destroyAllWindows()                       
            break          




