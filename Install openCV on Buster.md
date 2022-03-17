## openCV on Buster


### Caution
openCV often fails to install correctly when the following command is used.

```
sudo apt install opencv-contrib-python
```

Below is a sequence of commands that should work.
Verified on Pi 3b+ with Debian Buster.

### Installation options

#### Option 1 - Recommended
Use the same procedure for installing a lite version described here:

https://github.com/stuartofmt/Pi-Notes/blob/master/openCV%20on%20Bullseye.md

#### Option 2
Use the following process for a much older version - taken from this article:

https://pyshine.com/How-to-install-OpenCV-in-Rasspberry-Pi/


```
sudo apt-get install libhdf5-dev libhdf5-serial-dev

sudo apt-get install python3-h5py

sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5

sudo apt-get install libatlas-base-dev

sudo apt-get install libjasper-dev

sudo apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test

sudo pip3 install opencv-contrib-python==3.4.4.19
```

### Test the install

```
python3
>>> import cv2
>>> cv2.__version__
>>> exit()
```
If there is no error then cv2 is ready to go.