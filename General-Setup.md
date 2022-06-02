## General Setup


These settings work well BUT may not be appropriate for all Raspberry Pi variations of CPU, RAM etc.

### Update raspi-config.

```
sudo raspi-config
    Update
```

### Expand file system
To make use of the entire micro sd 

```
sudo raspi-config
    Advanced Options
        Expand Filesystem
```

### Set GPU memory
Many libraries like to make use of GPU - so give it enough to work with.

For P1 3B+ --> Set the GPU memory to 128

```
sudo raspi-config
    Performance Options
        GPU Memory       
```

It is best to reboot at this point.


###  Swap File
Best to do this after the above and after a reboot.

Depending on model of Raspberry Pi the default amount of swap space may (or not) be sufficient.
In general 4GB is a sensible minimum if using desktop apps such as chrome and doing video manipulation (e.g. ffmpeg).

First check to see what is allocated.

```
free -m

```
if less than 4096 - make it larger

```

sudo dphys-swapfile swapoff

sudo nano /etc/dphys-swapfile
     change CONF_SWAPSIZE=4096 and CONF_MAXSWAP=4096

sudo dphys-swapfile setup

sudo dphys-swapfile swapon

sudo reboot
```
