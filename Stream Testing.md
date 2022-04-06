## Stream Testing
This note describes a test script  written in python.
The purpose is to validate streaming of libcamera-vid.


### stream-test.py
Tests embedded cameras using libcamera-vid (i.e. Bullseye or later)<br><br>
Can be used on Bullseye or later releases with libcamera enabled.

### Scope
- [1] Tests one libcamera-vid combination for correct streaming.<br>
- [2] Use libcamera-test.py to determine a suitable resolution.  Can be found here:

https://github.com/stuartofmt/Pi-Notes/blob/master/Resolution%20Testing.md


Download stream-test.py from here:

https://github.com/stuartofmt/Pi-Notes/blob/master/stream-test.py

Is run like this:
```
python3 ./stream-test.py [options]
```
Options are:
- -camera  the number of the camera to be tested. Default is 0
- -pires  Mandatory. the resolution to be tested, specify --width and --height and / or --mode
- -pistream  the streaming method.  Default is tcp://0.0.0.0:5000
- -rotate  rotates the image 0, 90, 180 or 270 deg

The form of the command to start the streaming is
```
libcamera-vid -t 0  --nopreview --inline  --listen <-pires> --camera <-camera>  -o <-pistream>
```
-pires should work with any combination of commands supported by the camera.

Examples

Basic
```
python3 ./stream-test.py -pires "--width 1640 --height 1232"

```
Using a different resolution and camera
```
python3 ./stream-test.py -pires "--width 1920 --height 1080 --mode 3280:2464" -camera 1
```

with rotation
```
python3 ./stream-test.py -pires "--width 1640 --height 1232" -rotate 180
```

Same as above but used port 5050
```
python3 ./stream-test.py -pires "--width 1640 --height 1232" -rotate 180 -pistream "tcp://0.0.0.0:5050"
```


