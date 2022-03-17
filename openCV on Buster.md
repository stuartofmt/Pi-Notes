## openCV on Buster

See this site for a full discussion:

https://qengineering.eu/install-opencv-4.5-on-raspberry-pi-4.html


### Caution
openCV often fails to install correctly on Raspberry Pi when the following command is used.

```
sudo apt install opencv-contrib-python
```

Below is a sequence of commands that should work.
Verified on Pi 3b+ with Debian Buster.


They are taken from this article:

https://pyshine.com/How-to-install-OpenCV-in-Rasspberry-Pi/

### Install Prerequisites

```
sudo apt-get install libhdf5-dev libhdf5-serial-dev

sudo apt-get install python3-h5py

sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5

sudo apt-get install libatlas-base-dev

sudo apt-get install libjasper-dev

sudo apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test

```

### Install openCV
NOTE the use of pip3.

This build can take a long time (3+ hours)

```
sudo pip3 install opencv-contrib-python==3.4.4.19
```