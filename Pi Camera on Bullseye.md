## Pi Camera on Bullseye

Bullseye uses the newer libcamera libraries.

## Enable the Pi Camera

If using the new libcamera libraries (recommended) - the camera should already be enabled by default.

If using the old legacy libraries (not recommended) - the camera needs to be enabled<br>

The legacy camera stack cannot be re-enabled on a 64-bit Raspberry Pi OS release.

```
sudo raspi-config
    Interface Option
        Legacy Camera --> enable
    Advanced Options     
        Glamor --> enable
sudo reboot              
```

## On Raspberry Pi 3 and earlier

If running Bullseye you need to enable Glamor

```
sudo raspi-config
    Advanced Options     
        Glamor --> enable
sudo reboot              
```

## Testing the Camera

if using the recommended libcamera libraries.

```
libcamera_hello       
```

if using legacy libraries

```
raspistill -v -o test.jpg       
```



