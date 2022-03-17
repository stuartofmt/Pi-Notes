## openCV on Bullseye

See this site for a full discussion:
https://qengineering.eu/install-opencv-4.5-on-raspberry-pi-4.html


### Caution

openCV can fail to install correctly when the following command is used.

```
sudo apt install opencv-contrib-python
```


### Install openCV

The link below is a sequence of commands that should work
Verified on Pi 3b+ with Debian Bullseye.  It installs a light version of openCV.

https://qengineering.eu/install-opencv-lite-on-raspberry-pi.html

### Test the install

```
python3
>>> import cv2
>>> cv2.__version__
>>> exit()
```
If there is no error then cv2 is ready to go.

### What to do if CV2 cannot be found

If the module cannot be found - then a path needs to be added.

To find the path use:
```
sudo find / -name cv2
```

Next find the user site packages path for python

```
python3
>>> import site
>>> site.getusersitepackages()
```
For example:  This might return:
/home/pi/.local/lib/python3.9/site-packages

In this directory create a file called usercustomize.py with the following commands.
Note the position of the single quotes and the comma.
```
# usercustomize.py
import sys
sys.path.extend(['PATH-TO-CV2',])
```

Retest to see if CV2 is found.



