

openCV typically fails on Raspberry Pi when the following command is used.

```
sudo apt install opencv-contrib-python
```


Due to some dependencies not included in some OS versions on the Raspberry Pi - the simple command above can fail. Below is a sequence of commands that should work
(Verified on Pi 3b+ with Debian Buster):
They are taken from this article:  https://pyshine.com/How-to-install-OpenCV-in-Rasspberry-Pi/

```
sudo apt-get install libhdf5-dev libhdf5-serial-dev

sudo apt-get install python3-h5py

sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5

sudo apt-get install libatlas-base-dev

sudo apt-get install libjasper-dev

sudo apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test

sudo pip3 install opencv-contrib-python==3.4.4.19
```

