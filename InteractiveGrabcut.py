
# coding: utf-8

# In[27]:
# import numpy as np
def initVars():
    COLOR=(255,255,255)
    BRUSH_SIZE=2
    prevX=0
    prevY=0
    localMouseDownFinish=False
    # refineMask=np.zeros(img.shape[:2],np.uint8)
    # mask = np.zeros(img.shape[:2],np.uint8)
    # finalMask=refineMask.copy()
    # helperImage=backupImage.copy()

    # backupImage=img.copy()
    # cv2.namedWindow('Grabcut')
    # cv2.setMouseCallback('Grabcut',mouseEvent)
    img=None
    backupImage=None
    xx=0
    yy=0
    XX=0
    YY=0
    XX_=0
    YY_=0
    localMouseDown=False



# returns false if not time to apply the grabcut finally
# returns true when to apply the grabcut and exit the while(True) main loop

def noMouseEvent(event,x,y,flags,params):
    pass

def mouseEvent(event,x,y,flags,params):
    global backupImage,img,xx,yy,XX,YY,XX_,YY_,topRectangle, bottomRectange,localMouseDown

    if event==cv2.EVENT_LBUTTONDOWN:
        img=backupImage.copy()
        xx=x
        yy=y
        topRectangle=(xx,yy)
        localMouseDown=True
        print('Start Point is : ',xx,yy)

        #return False
    elif event== cv2.EVENT_MOUSEMOVE and localMouseDown:
        img=backupImage.copy()
        XX=x
        YY=y
        cv2.rectangle(img,(xx,yy),(XX,YY),(0,255,255),2)
        cv2.imshow('Grabcut',img)
        #return False

    elif event== cv2.EVENT_LBUTTONUP:
        XX_=x
        YY_=y
        bottomRectangle=(XX_,YY_)
        img=backupImage.copy() # remove the rectangle from the image
        cv2.imshow('Grabcut',img)
        localMouseDown=False
        print('End Point is : ',XX_,YY_)
        if(xx==XX_ or yy==YY_):
            xx=yy=XX_=YY_=0
            return # we dont want that the selection is a line or even a point



# In[28]:


# interactive paint to make selections on the masks.
def mouseEventFinish(event,x,y,flags,params):
    global helperImage,refineMask,COLOR,prevX,prevY,localMouseDownFinish,BRUSH_SIZE
    if event==cv2.EVENT_LBUTTONDOWN:
        cv2.circle(helperImage,(x,y),BRUSH_SIZE,COLOR,-1)
        cv2.circle(refineMask,(x,y),BRUSH_SIZE,COLOR,-1)
        prevX=x
        prevY=y
        localMouseDownFinish=True
    elif event== cv2.EVENT_MOUSEMOVE and localMouseDownFinish:
        cv2.line(helperImage,(prevX,prevY),(x,y),COLOR,BRUSH_SIZE)
        cv2.line(refineMask,(prevX,prevY),(x,y),COLOR,BRUSH_SIZE)
        prevX=x
        prevY=y
        return
    elif event==cv2.EVENT_LBUTTONUP:
        cv2.line(helperImage,(prevX,prevY),(x,y),COLOR,BRUSH_SIZE)
        cv2.line(refineMask,(prevX,prevY),(x,y),COLOR,BRUSH_SIZE)
        prevX=x
        prevY=y
        localMouseDownFinish=False



# In[31]:


import cv2
import numpy as np
import time
import os



print('Apply grabcut algorithm','Please make a selection by clicking and dragging on the image')


# IN THEORY #


# load an image
# add an ability to add a rectangle to the image (use code of cut, zoom in and zoom out )
# take that selection and apply the grabcut on that part.
# display the grabcut part
# make a mask over the image
# allow user to mordify the grabcut using the masks and finally end the editing
# This is a real life interactive project and an implementaion of the famous content aware cut algorithm in
# adobe photoshop
def initializeGrabCut(img):
    # img=cv2.imread('blocks.jpg')
    # img=img
    backupImage=img.copy()
    cv2.namedWindow('Grabcut')
    cv2.setMouseCallback('Grabcut',mouseEvent)
    xx=0
    yy=0
    XX=0
    YY=0
    XX_=0
    YY_=0
    localMouseDown=False
    initVars()

    while(True):
        cv2.imshow('Grabcut',img)
        topRectangle=[]
        bottomRectangle=[]
    #     print('xx: ',xx,'yy:',yy,'XX:',XX_,'YY:',YY_)

        k=cv2.waitKey(1) & 0xFF
        if k==ord('q') or k==ord('Q'):
            break

        if xx!=0 and yy!=0 and XX_!=0 and YY_!=0:
            break
        else:
            continue


    # apply the grabcut
    if xx and yy and XX_ and YY_:
        mask = np.zeros(img.shape[:2],np.uint8)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        # rect=tuple(topRectangle[0][0],topRectangle[0][1],bottomRectangle[0][0],bottomRectangle[0][1])
        rect=[xx,yy,XX_,YY_]
        rect=tuple(rect)
        cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        img = img*mask2[:,:,np.newaxis]
        cv2.imshow('Grabcut',img)


    cv2.setMouseCallback('Grabcut',noMouseEvent)

    # refineCode #
    cv2.namedWindow('refineSelection')
    COLOR=(255,255,255)
    BRUSH_SIZE=2
    prevX=0
    prevY=0
    localMouseDownFinish=False
    refineMask=np.zeros(img.shape[:2],np.uint8)
    # mask = np.zeros(img.shape[:2],np.uint8)
    finalMask=refineMask.copy()
    helperImage=backupImage.copy()
    cv2.setMouseCallback('refineSelection',mouseEventFinish)
    print('Press S or s to subtract from image')
    print('Else Press A or a to add to image')
    print('Increase brush size by pressing M or m')
    print('Decrease brush size by pressing N or n')

    # make mask & refine cut
    while(True):
        cv2.imshow('refineSelection',helperImage) # both helper image and mask are changed (see the callBack of mouse)

        k=cv2.waitKey(1) & 0xFF
        if k==ord('q') or k==ord('Q'):
            break
        elif k==ord('s') or k==ord('S'):
            COLOR=(0,0,0)
        elif k==ord('a') or k==ord('A'):
            COLOR=(255,255,255)
        elif k==ord('m') or k==ord('M'):
            BRUSH_SIZE+=1
        elif k==ord('n') or k==ord('N'):
            BRUSH_SIZE-=1
            if(BRUSH_SIZE<1): BRUSH_SIZE=1 #CANT BE LESS THAN 1



    # Apply grabcut the the mask.

    # whereever it is marked white (sure foreground), change mask=1
    # whereever it is marked black (sure background), change mask=0
    finalMask[refineMask == 0] = 0
    finalMask[refineMask == 255] = 1

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    #reset helperImage
    helperImage=backupImage.copy()

    #apply mask, The code is not working for some reason, I think, my implementation is spot on! :(
    finalMask,_,_=cv2.grabCut(helperImage,finalMask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
    finalMask = np.where((finalMask==2)|(finalMask==0),0,1).astype('uint8')
    helperImage = img + helperImage*finalMask[:,:,np.newaxis]

    cv2.imshow('refineSelection',helperImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return helperImage






