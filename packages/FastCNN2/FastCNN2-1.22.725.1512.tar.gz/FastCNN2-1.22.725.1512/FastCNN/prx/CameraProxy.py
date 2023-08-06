import cv2
import time
import base64
import os
from threading import Thread,Lock


class CV2Camera:
    def __init__(self):
        self._img = None
        self._thx = None
        self._run = False
        self._fps = 0.0
        self._width = 2592
        self._heigh = 1944
        self._w = 2592
        self._h = 1944
        self._f = 60
        self._lock = Lock()
        self.setSize()
        self.setExposure(1000)
        pass
    
    def startCapture(self):
        if self._thx == None:
            
            self._thx = Thread(target=self.doCapture)
            self._run = True
            self._thx.start()
            time.sleep(0.5)
        pass
    
    def stopCapture(self):
        if self._thx:
            self._run = False
            time.sleep(0.5)
        pass
    
    def isGrabbing(self):
        return not (self._img is None)
    
    def doCapture(self):
        cap = cv2.VideoCapture(0)
        cap.set(3,self._width)
        cap.set(4,self._heigh)
        cap.set(5,self._f)
        
        while self._run:
            if cap.isOpened():
                s = time.time()
                suc,img = cap.read()
                e = time.time()
                
                if suc:
                    with self._lock:
                        
                        self._img = cv2.resize(img,(self._w,self._h))
                        self._fps = round(1/(e-s),2)
                else:
                    self._run = False
                
            else:
                self._run = False
            
                
            time.sleep(0.003)
        cap.release()
        self._img = None
        self._thx = None
        self._fps = 0.0
        #cv2.destroyAllWindows()
        pass
            
    def getCapture(self):

        rtn = {"width":str(self._w),"heigh":str(self._h)}
        with self._lock:
            if not (self._img is None):
                rtn["fps"] = str(self._fps)
                rtn["stream"] = str(base64.b64encode(self._img))[2:-1]
            
        return rtn
        
    def setSize(self,size=800000):
        dlt = 800000/(self._width*self._heigh)
        self._w = int(self._width*dlt)
        self._h = int(self._heigh*dlt)
        pass
    
    def setFps(self,fps = 60):
        self._f = fps
        pass
    
    def setExposure(self,exp):
        os.system("v4l2-ctl -d /dev/video0 -c exposure_absolute={}".format(exp))
        pass


if __name__ == "__main__":
    cam = CV2Camera()
    cam.startCapture()
    while True:
        print(cam.getCapture())
        s = input()
        if s== 'c':
            break
    
    
