## Resolution Testing
Two test scripts written in python.
libcamera-test.py - only tests embedded cameras. Can test both still and video output.
opencv-test.py - tests embedded and USB cameras. Only tests video output.

- [1] These scripts attempt to display common / available resolutions.<br>
- [2] Not all combinations will produce the desired display.<br>
- [3] Supported combinations may be different between libcamera and openCV.<br>
- [4] Camera numbers may be different between libcamera and openCV.


### libcamera-test.py
Can be used on Bullseye or later releases with libcamera enabled.
Is run like this:
```
python3 ./libcamera-test.py [options]
```
Options are:
-rotate  rotates the image 180 deg
-still   uses libcamera-still (default is libcamera-vid)
-debug   outputs debug messages from libcamera
-time    length of time for display (default is 15 sec)

### opencv-test.py
Can be used on Buster (and earlier) and Bullseye.

If used on Buster - should be run like this:

```
python3 ./opencv-test.py [options]

```

If used on Bullseye must be run like this:
```
libcamerify python3 ./opencv-test.py [options]
```

Options are:
-rotate  rotates the image 180 deg
-debug   outputs debug messages from libcamera
-time    length of time for display (default is 15 sec)

