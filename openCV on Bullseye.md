openCV typically fails on RP when the following command is used.

```
sudo apt install opencv-contrib-python
```


The simple command above can fail. Below is a sequence of commands that should work
(Verified on Pi 3b+ with Debian Bullseye):
They are taken from this article:  https://raspberrypi-guide.github.io/programming/install-opencv

Install Prerequisites

Tried this:
```
sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103  libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 python3-dev -y
```


Got errors on libqtgui4 libqtwebkit4 libqt4-test
Rerun without

```
sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103  python3-pyqt5 python3-dev -y
```

Try simple install. NOTE use of pip3.  This build can take a long time (hours) and may fail.

```
pip3 install opencv-contrib-python
```

If it fails - try this.

```
pip install opencv-contrib-python==4.1.0.25
```

or

```
sudo apt install python-opencv
```
