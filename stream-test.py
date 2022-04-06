#stream-test.py

import cv2
import time
import imutils
import subprocess
import argparse
from threading import Thread
import sys

def init():
    # parse command line arguments
    parser = argparse.ArgumentParser(
            description='Camera Test',
            allow_abbrev=False)
    # Options
    parser.add_argument('-camera', type=int, nargs=1, default=[0], help='Camera number - default 0')
    parser.add_argument('-pires', type=str, nargs=1, default=[''], help='pires commands for libcamera-vid')
    parser.add_argument('-pistream', type=str, nargs=1, default=['tcp://0.0.0.0:5000'], help='Output stream. Default = tcp://0.0.0.0:5000') 
    parser.add_argument('-rotate', type=int, nargs=1,default=[0], help='Can be 0,90,180,270 Default 0')
    parser.add_argument('-debug', action='store_true', help='If omitted - limit debug messages ')

    args = vars(parser.parse_args())

    global camera, pires, rotateimage, debug, pistream
    camera = abs(args['camera'][0])
    pires = args['pires'][0]
    pistream = args['pistream'][0]
    rotateimage = args['rotate'][0]
    if rotateimage not in (0,90,180,270):
        rotateimage = 0
    if args['debug']:
        debug = ''
    else:
        debug = ' 2>/dev/null'
    
    #Check if libcamera-vid is already in-use
    cmd = ['pgrep', '-f', 'libcamera-vid']
    try:
        # exit code is zero if found
        result = subprocess.check_call(cmd)
        print(result)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('libcamera-vid is already in use.')
        print('Check with ps - ef | grep libcamera-vid')
        print('Exiting')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        pass
        
                
class VideoStream:
    # initialize with safe defaults
    def __init__(self, src=0, res=[800,600,'MJPG'], name="VideoStream"):
        # initialize the video camera stream and read the first frame
        self.stream = cv2.VideoCapture(src)
        if isinstance(src, int):  #Bypass is stream input
            try:
                self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, res[0])
                self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, res[1])
                format = res[2]
                fourcc = cv2.VideoWriter_fourcc(*format)
                self.stream.set(cv2.CAP_PROP_FOURCC, fourcc)
            except Exeption as e:
                print('opencv error')
                print(e)
        self.grabbed, self.frame = self.stream.read()

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
            self.grabbed, self.frame = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.grabbed, self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

def startPicam(cam, res):
    libcamera = 'libcamera-vid '        
    cmdtxt = []
    cmdtxt.append(libcamera + '-t 0')
    cmdtxt.append(' --nopreview --inline  --listen ')
    cmdtxt.append(res)   
    cmdtxt.append(' --camera ' + str(cam))
    cmdtxt.append(' -o ' + pistream)
    if debug != '':
        cmdtxt.append(debug)
    cmd = ''.join(cmdtxt)

    print('\nStarting camera with this command\n')    
    print(cmd)
    try:
        subprocess.Popen(cmd, shell=True, start_new_session=True)  # run the program
    except Exception as e:
        print('Problem starting ' + libcamera)
        print(e)

def camdisplay(cam, res):
    windowname = 'Camera ' + str(cam) + ' ' + res
    framerate = 10
    newwidth = 640  # Display pires width

    while True:
        time.sleep(1/framerate) # Don't ask for frames any quicker than needed
        try:
            ret, frame = stream.read()
        except Exception as e:
            print('There was an error reading from the camera')
            print(e)
            continue
        
        if ret is False or ret is None:
            continue
        else:    
            frame = imutils.resize(frame, width=newwidth, inter=cv2.INTER_LINEAR)    
            if rotateimage != 0:
                frame = imutils.rotate(frame, rotateimage)
            cv2.imshow(windowname, frame)
        cv2.waitKey(1)
        if shutdown:
            cv2.destroyAllWindows()
            break
  
    cv2.destroyAllWindows()
    return

## Start of program
if __name__ == "__main__":
    
    init()
    startPicam(camera, pires) #Just needs to be started no thread needed
    delay = 10
    print('\nWait ' + str(delay) + ' sec for libcamera-vid to start')
    time.sleep(delay)
    cam = pistream
    stream = VideoStream(cam)
    stream.start()
    print('\nStop by pressing Ctrl+C')
    try:
        shutdown = False
        camdisplay(camera, pires)
    except KeyboardInterrupt:
        shutdown = True

    cv2.destroyAllWindows()
    stream.stop()
