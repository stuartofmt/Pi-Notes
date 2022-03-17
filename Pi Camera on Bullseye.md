## Pi Camera on Bullseye


## Enable the Pi Camera

If using the new libcamera libraries (recommended) - he camera should already be enabled by default.

If using the old legacy libraries - the camera needs to be enabled.

```
sudo raspi-config
    Interface Option
        Camera       
```

##Testing the Camera

if using libcamera libraries

```
libcamera_hello       
```

if using legacy libraries

```
libcamera_hello       
```