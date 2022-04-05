## Resolution Testing
This note describes two test scripts written in python.

### libcamera-test.py
Tests embedded cameras. Can test both still and video output.<br><br>

### opencv-test.py
Tests embedded and USB cameras. Only tests video output.

### Scope
- [1] These scripts attempt to display common / available resolutions.<br>
- [2] Not all combinations will produce the desired display due to differences in camera characteristics.<br>
- [3] Supported combinations may behave differently between libcamera and openCV.<br>
- [4] Camera numbers may be different in libcamera and openCV.
- [5] Multiple logical cameras can be found for each physical camera

### libcamera-test.py
Can be used on Bullseye or later releases with libcamera enabled.
Download from here:
https://github.com/stuartofmt/Pi-Notes/blob/master/libcamera-test.py

Is run like this:
```
python3 ./libcamera-test.py [options]
```
Options are:
- -rotate  rotates the image 180 deg
- -still   uses libcamera-still (default is libcamera-vid)
- -debug   outputs debug messages from libcamera
- -time    length of time for display (default is 15 sec)

### opencv-test.py
Can be used on Buster (and earlier) and Bullseye.
Download from here:
https://github.com/stuartofmt/Pi-Notes/blob/master/opencv-test.py

If used on Buster - should be run like this:

```
python3 ./opencv-test.py [options] 2>/dev/null

```

If used on Bullseye must be run with libcamerify:
```
libcamerify python3 ./opencv-test.py [options] 2>/dev/null
```

Options are:
- -rotate  rotates the image 180 deg
- -time    length of time for display (default is 15 sec)

Note: There is no debug mode.  If opencv responses are desired then omit "2>/dev/null"
