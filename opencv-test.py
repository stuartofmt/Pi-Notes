# camera-test.py

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
    parser.add_argument('-debug', action='store_true', help='If omitted = Limit debug messages ')
    parser.add_argument('-time', type=int, nargs=1, default=[15], help='Image display time - default 15 sec')
    args = vars(parser.parse_args())

    global rotateimage, debug, display

    rotateimage = args['rotate']
    if args['debug']:
        debug = ''
    else:
        debug = ' 2>/dev/null'
    display = abs(args['time'][0])

class picams():
    
    def __init__(self):

        cmd = 'libcamera-vid --list-cameras'
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
            if str(res.stderr) != '':
                result = str(res.stderr)
        except Exception as e:
            result = ''
            print(e)
        
        cameraInfo=result.partition('Available cameras')[2]
        # find the cameraids - form is one or two digits followed by :
        cameraids = re.findall('(\s\d\s:|\s\d{2}:)', cameraInfo)
        
        # get the camera numbers
        self.cameras = []
        for camera in cameraids:
            newid = re.search('\d{1,2}', camera)
            if newid is not None:
                self.cameras.append(newid.group())
        # get the data between / after the camerais
        cameradata = re.split('\s\d\s:|\s\d{2}:', cameraInfo) 
        del cameradata[0]  # need to ignore the first result
        
        # parse out the name and resolutions for each camera
        name = []
        reses = []
        for camera in cameradata:
            index = cameradata.index(camera)
            camname = re.search('imx\d{3}',camera)
            print(camname)
            if camname is not None:  # Ignore other types
                name.append(camname.group())
                reses.append(re.findall('([0-9]{3,4})x([0-9]{3,4})', camera))
            else:
                del self.cameras[index]
        # get rid of unwanted resolutions
        self.resolutions = {}
        for cam in self.cameras:
            self.resolutions[cam] = {}
            resolut = []
            for res in reses[int(cam)]:
                res = list(res) # Convert to list
                if res in resolut or int(res[0]) < 320 or int(res[1]) < 240:
                    pass
                else:
                    resolut.append(res)
            sortedresolut = sorted(resolut, key=lambda x:int(x[0]))
            self.resolutions[cam] = sortedresolut               
        # Build the camera info
        self.available_cameras= {}
        for camera in self.cameras:
            self.available_cameras[camera] = {}
            self.available_cameras[camera]['name'] = name[int(camera)]
            
    def get_cameras(self):
        return self.cameras
    
    def get_name(self,cam):
        return self.available_cameras[str(cam)]['name']
    
    def get_resolutions(self, cam):
        resolutions = self.resolutions[str(cam)]
        resolutions_str = str(resolutions).strip('[]')
        return resolutions_str, resolutions    


class VideoStream:
    # initialize with safe defaults
    def __init__(self, src=0, res=[800,600,'BGR3'], frate=15, name="VideoStream"):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        if isinstance(src, int):  #  Assume cv2 can manipulate
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, res[0])
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, res[1])
            format = res[2]
            fourcc = cv2.VideoWriter_fourcc(*format)
            self.stream.set(cv2.CAP_PROP_FOURCC, fourcc)
            self.stream.set(cv2.CAP_PROP_FPS, frate)
            #self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Just to keep things tidy and small
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
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
            # if the thread indicator variable is set, stop the thread
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
    if raspi:
        return raspiInfo.get_cameras()
    return findopencvCameras()

def findopencvCameras():
    available_cameras = []
    for index in range(0, 20):
        stream = cv2.VideoCapture(index)
        if stream.isOpened():
            available_cameras.append(str(index))   # using string for convenience
        stream.release()
    return available_cameras

def getCameraname(cam):
    if raspi:
        return raspiInfo.get_name(cam)
    return ''



def getResolutions(cam):
    if raspi:
        return raspiInfo.get_resolutions(cam)
    return getopencvResolutions()

def getopencvResolutions():
    resolution = []                  # Note: needs to be ordered in size to support later comparisons
    resolution.append([2048, 1080])  # Default
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
    print('\n Scanning for resolutions and formats -- this can take some time ...')

    #stream = cv2.VideoCapture(int(cam))

    for res in resolution:
        width = res[0]
        height = res[1]
        for form in allowed_formats:
            stream = cv2.VideoCapture(int(camera)) # Make sure we have a new clean connection
            if not stream.isOpened:
                print('Could not open camera: ' + str(camera))
                stream.release()
                break
            stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            fourcc = cv2.VideoWriter_fourcc(*form)
            stream.set(cv2.CAP_PROP_FOURCC, fourcc)
            # Now try to read back
            camwidth = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
            camheight = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cc = stream.get(cv2.CAP_PROP_FOURCC)
            camformat = "".join([chr((int(cc) >> 8 * i) & 0xFF) for i in range(4)])
            reported_resolution = [camwidth, camheight, camformat]
            if reported_resolution not in available_res and camformat in allowed_formats:
                available_res.append(reported_resolution)
                available_resolutions_str.append(str(camwidth) + 'x' + str(camheight) + '(' + camformat + ')  ')
            stream.release()
            
    available_resolutions = sorted(available_res, key=lambda x:int(x[0]))        
    resolutions_str = ''.join(available_resolutions_str)
    return resolutions_str, available_resolutions 

def startPicam(cam, res):
    # Current settings are inconsistent. The lookup is a workaround
    commands = {}
    commands['640']= 'libcamera-vid -t 0 --width 640 --height 480 --mode 1640:1232'
    commands['1640'] = 'libcamera-vid -t 0 --width 1640 --height 1232'
    commands['1920'] = 'libcamera-vid -t 0 --width 1920 --height 1080 --mode 3280:2464'
    commands['3280'] = 'libcamera-vid -t 0 --mode 3280:2464'
    w = str(res[0])
    h = str(res[1])
    cmdtxt = []
    cmdtxt.append(commands[str(res[0])])
    cmdtxt.append(' --nopreview --inline  --listen')
    """
    cmdtxt.append(' --width ' + w) 
    cmdtxt.append(' --height ' + h)
    #cmdtxt.append(' --mode 1640:1232')
    cmdtxt.append(' --mode ' + w + ':' + h)
    """
    if rotateimage:
        cmdtxt.append(' --vflip --hflip')   
    cmdtxt.append(' --camera ' + str(cam))
    cmdtxt.append(' -o tcp://0.0.0.0:5000')
    if debug != '':
        cmdtxt.append(debug)
    cmd = ''.join(cmdtxt)

    print('\nStarting camera with this command')
    print(cmd)
    try:
        newproc = subprocess.Popen(cmd, shell=True, start_new_session=True)  # run the program
        time.sleep(2) # Give it some time to startup
    except Exception as e:
        print('Problem starting libcamera-vid')
        print(e)

def display(cam, res):
    
    displaytime = 15 #seconds
    print('\n\n ===============  Camera ' + str(cam) + '  ===================== \n\n')
    print('Will attempt to display the following resolution for ' + str(displaytime) + ' seconds\n')
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
    framerate = 15 # keep it low for testing
    if raspi:
        startPicam(cam, res)
        cam = 'tcp://0.0.0.0:5000'
        windowname = 'Camera ' + str(cam) + ' ' + str(res[0]) + ' x ' + str(res[1])
    else:
        windowname = 'Camera ' + str(cam) + ' ' + str(res[0]) + ' x ' + str(res[1]) + ' format ' + str(res[2])

    stream = VideoStream(cam, res, framerate)
    stream.start()
    
    #cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)
    newwidth = 640  # Display resolution width
    reads = 0
    errors = 0
    timeout = 0
    starttime = time.time()
    while  time.time() - starttime < displaytime:
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
                print('Waiting')
            print('.', end='', flush=True)
            timeout = timeout + 1
            if timeout > framerate*(displaytime-1):  # Mostly no frames  
                print('\nConnection timed out')
                break
            continue
        else:
            timeout = 0  # reset if it starts displaying     
            resized = imutils.resize(frame, width=newwidth, inter=cv2.INTER_LINEAR)    
            #resized = frame
            cv2.imshow(windowname, resized)
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
        display(int(cam), res)

## Start of program
        
init()

if __name__ == "__main__":
        
            
    keypress = 'n'
    while keypress not in ['p', 'a', 'q']:
        print('What type of camera? Make a selection and press enter\n')
        print('(p) - Raspberry Pi using libcamera')
        print('(a) - All cameras. Pi and USB using opencv')
        print('(q) - quit')
        keypress = input()
    raspi = False    
    if keypress == 'p':
        raspi = True
        raspiInfo = picams()
    elif keypress == 'q':
        sys.exit(0)
    elif keypress == 'a':
            print('\nNote:\n')
            print('opencv may fully support Pi Cameras with libcamera yet')
            print('Camera numbers may also be different than with libcamaera')
            print('Try running "libcamerify python3 ./<this program> 2>/dev/null"')
            
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