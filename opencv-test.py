# opencv-test.py

import cv2
import time
import imutils
import sys
from threading import Thread
import subprocess
import re
import argparse


def init():
    # parse command line arguments
    parser = argparse.ArgumentParser(
            description='Camera Test',
            allow_abbrev=False)
    # Options
    parser.add_argument('-rotate', action='store_true', help='If omitted = Do not rotate')
    parser.add_argument('-time', type=int, nargs=1, default=[15], help='Image display time - default 15 sec')
    args = vars(parser.parse_args())

    global rotateimage, display

    rotateimage = args['rotate']
    display = abs(args['time'][0])

class VideoStream:
    # initialize with safe defaults
    def __init__(self, src=0, res=[800,600,'BGR3'], frate=15, name="VideoStream"):
        # initialize the video camera stream and read the first frame
        self.stream = cv2.VideoCapture(src)
        if isinstance(src, int):  #  Assume cv2 can manipulate
            try:
                self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, res[0])
                self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, res[1])
                format = res[2]
                fourcc = cv2.VideoWriter_fourcc(*format)
                self.stream.set(cv2.CAP_PROP_FOURCC, fourcc)
                #self.stream.set(cv2.CAP_PROP_FPS, frate)
                #self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Just to keep things tidy and small
            except Exeption as e:
                print('opencv error')
                print(e)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            if self.stopped:
                self.stream.release()
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.grabbed, self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

def findCameras():
    return findopencvCameras()

def findopencvCameras():
    available_cameras = []
    for index in range(0, 20):
        stream = cv2.VideoCapture(index)
        if stream.read()[0]:  # use instead of isOpened as it confirms it can be read
            available_cameras.append(str(index))   # using string for convenience
        stream.release()
    return available_cameras

def getCameraname(cam):
    return ''

def getResolutions(cam):
    return getopencvResolutions()

def getopencvResolutions():
    resolution = []                  # Note: needs to be ordered in size to support later comparisons
    resolution.append([3280, 2464])
    resolution.append([2048, 1080])
    resolution.append([1920, 1800])
    resolution.append([1640, 1232])
    resolution.append([1280, 720])
    resolution.append([800, 600])
    resolution.append([720, 480])
    resolution.append([640, 480])
    resolution.append([320, 240])
    allowed_formats = ('BGR3', 'YUY2', 'MJPG','JPEG', 'H264', 'IYUV')

    available_res = []
    available_resolutions_str = []
    print('\nScanning for resolutions and formats -- this can take some time ...')

    for res in resolution:
        print('.', end='', flush=True)
        width = res[0]
        height = res[1]
        for form in allowed_formats:
            print('.', end='', flush=True)
            stream = cv2.VideoCapture(int(camera)) # Make sure we have a new clean connection
            if not stream.isOpened:
                print('Could not open camera: ' + str(camera))
                stream.release()
                break
            try:
                stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                fourcc = cv2.VideoWriter_fourcc(*form)
                stream.set(cv2.CAP_PROP_FOURCC, fourcc)
                # Now try to read back
                camwidth = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
                camheight = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
                cc = stream.get(cv2.CAP_PROP_FOURCC)
            except Exeption as e:
                print('opencv error')
                print(e)
            camformat = "".join([chr((int(cc) >> 8 * i) & 0xFF) for i in range(4)])
            reported_resolution = [camwidth, camheight, camformat]
            if reported_resolution not in available_res and camformat in allowed_formats:
                available_res.append(reported_resolution)
                available_resolutions_str.append(str(camwidth) + 'x' + str(camheight) + '(' + camformat + ')  ')
            stream.release()
            
    available_resolutions = sorted(available_res, key=lambda x:int(x[0]))        
    resolutions_str = ''.join(available_resolutions_str)
    return resolutions_str, available_resolutions 

def camdisplay(cam, res):
    print('\n\n ===============  Camera ' + str(cam) + '  ===================== \n\n')
    print('Will attempt to display the following resolution for ' + str(display) + ' seconds\n')
    print('Any keypress will close the display\n')

    print('################################################')
    print(res)
    print('################################################')
    print('\n')
    time.sleep(1)

    if auto is False:
        print('\nPress any key to continue...')
        input()
        # start the stream capture
    framerate = 10 # keep it low for testing
    windowname = 'Camera ' + str(cam) + ' ' + str(res[0]) + ' x ' + str(res[1]) + ' format ' + str(res[2])

    stream = VideoStream(cam, res, framerate)
    stream.start()
    
    #cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)
    newwidth = 640  # Display resolution width
    reads = 0
    errors = 0
    timeout = 0
    starttime = time.time()
    while  time.time() - starttime < display:
        time.sleep(1/framerate) # Don't ask for frames any quicker than possible
        ret = None
        frame = None
        try:
            reads = reads + 1
            ret, frame = stream.read()
        except Exception as e:
            errors = errors + 1
            if frame is None:
                pass
            else:
                print('There was an error reading from the camera')
                print(e)
            continue
        
        if ret is False or ret is None:
            if timeout == 0:
                print('Possible missed frame')
            print('.', end='', flush=True)
            timeout = timeout + 1
            if timeout > framerate*(display-1):  # Mostly no frames  
                print('\nConnection timed out')
                break
            continue
        else:
            timeout = 0  # reset if it starts displaying     
            frame = imutils.resize(frame, width=newwidth, inter=cv2.INTER_LINEAR)    
            if rotateimage:
                frame = imutils.rotate(frame, 180)
            cv2.imshow(windowname, frame)
        if cv2.waitKey(1) != -1:
            break

    stream.stop() 
    cv2.destroyAllWindows()
    print('\n There were ' +str(reads) + ' reads with ' + str(errors) + ' errors and ' +  str(timeout) + ' timeouts')
    return

def testCamera(cam):
    resolution_str, resolutions = getResolutions(int(cam))
    if resolution_str != '':
        print('\nThe following resolutions are POSSIBLE from camera:  ' + str(cam) + '\n' + resolution_str)
    else:
        print('\n The camera did not provide any resolution information')
        
    for res in resolutions:
        camdisplay(int(cam), res)

## Start of program
if __name__ == "__main__":

    init()

    keypress=''
    while keypress not in ['a', 'm', 'q']:        
        print('\nSelect an option and press enter\n')
        print('(a) - automatic, will cycle through all combinations')
        print('(m) - manual, changes combinations on keypress')
        print('(q) - quit')
        keypress = input()
       
    auto = False
    if keypress == 'a':
        auto = True
    elif keypress == 'q':
        sys.exit(0)
       
    cameras = findCameras()
    if len(cameras) == 0:
        print('No cameras were found')
        sys.exit(1)   
    else:
        keypress = ''
        while keypress not in cameras and keypress != 'a':
            print('\nSelect which camera(s) to test and press enter\n')
            for camera in cameras:
                camname = getCameraname(camera)
                if camname != '':
                    camname = ' - ' + camname
                print('Camera index: ' + str(camera) + camname)
            print('\n(a) - will cycle through all cameras')
            print('(n) - "n" is a camera index')
            keypress = input()
    camera = ''    
    if keypress == 'a':
        pass
    else:
        camera = keypress
        
        
    if camera == '':
        for camera in cameras:
            testCamera(camera)
    else:
        testCamera(camera)
