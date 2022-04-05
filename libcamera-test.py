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
    parser.add_argument('-still', action='store_true', help='If omitted = Use video')
    parser.add_argument('-debug', action='store_true', help='If omitted = Limit debug messages ')
    parser.add_argument('-time', type=int, nargs=1, default=[15], help='Image display time - default 15 sec')
    args = vars(parser.parse_args())

    global rotateimage, still, debug, display

    rotateimage = args['rotate']
    still = args['still']
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


def findCameras():
    return raspiInfo.get_cameras()

def getCameraname(cam):
    return raspiInfo.get_name(cam)

def getResolutions(cam):
    return raspiInfo.get_resolutions(cam)


def startPicam(cam, res):
    # Current settings are inconsistent. The lookup is a workaround
    timeout = str(display*1000) #timeout in ms
    if still:
        libcamera = 'libcamera-still '
    else:
        libcamera = 'libcamera-vid '
        
    cmdtxt = []
    cmdtxt.append(libcamera + '-t ' + timeout)
    cmdtxt.append(res)
    cmdtxt.append(' --info-text "' + libcamera + res + '"')
    if rotateimage:
        cmdtxt.append(' --vflip --hflip')   
    cmdtxt.append(' --camera ' + str(cam))
    if debug != '':
        cmdtxt.append(debug)
    cmd = ''.join(cmdtxt)

    print('\nStarting camera with this command\n')
    print('Will display for ' + str(display) + ' seconds\n')
    
    print(cmd)
    time.sleep(5)
    try:
        #newproc = subprocess.Popen(cmd, shell=True, start_new_session=True)  # run the program
        newproc = subprocess.run(cmd, shell=True)  # run the program
    except Exception as e:
        print('Problem starting ' + libcamera)
        print(e)

def testCamera(cam):
    resolution_str, resolutions = getResolutions(int(cam))
    if resolution_str != '':
        print('\nThe following resolutions are POSSIBLE from camera:  ' + str(cam) + '\n' + resolution_str)
    else:
        print('\n The camera did not provide any resolution information')
    #  Create combinations
    modes = []
    modes.append('')  # No Mode
    for res in resolutions:
        m = res[0] + ':' + res[1]
        modes.append(' --mode ' + m)

    resmode = []
    for res in resolutions:
        wh = ' --width ' + res[0] + ' --height ' + res[1]
        for mode in modes:
            r = wh + mode
            resmode.append(r)

    for res in resmode:
        try:
            startPicam(int(cam), res)
        except KeyboardInterrupt:
            sys.exit(0)    
## Start of program        
if __name__ == "__main__":
    
    init()
    raspiInfo = picams()
        
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
