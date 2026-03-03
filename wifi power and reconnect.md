# Set wifi sleep power to disable


disable at each boot with cron
```
$ sudo crontab -e

# which opens the root crontab in your chosen editor...
# add the following line at the bottom of the root crontab:

@reboot /usr/sbin/iw wlan0 set power_save off > /home/<user>/power_save_log.txt 2>&1

# be sure to substitute a valid folder name for '<user>' in the line above
```

#change connection retry amount

And turn on permanent connection retries, in the xyz.nmconnection file (whwre xyz is the connection being used),
located at /etc/NetworkManager/system-connections like:

```
[connection]
id=MyWiFi
uuid=<connection uid>
type=wifi
interface-name=wlan0
# This value is probably missing if configured with raspi-config
# By default is -1 that means, to use NM default value. In Debian is likely to be 3 or 4 tries.
# Here zero means retry forever. MAY (unsure ??) prevent connecion fallback to lower priority connection
autoconnect-retries=0

[wifi]
mode=infrastructure
ssid=MyWiFi

[wifi-security]
auth-alg=open
key-mgmt=wpa-psk
psk=superpassword

[ipv4]
method=auto

[ipv6]
addr-gen-mode=default
method=auto

[proxy]
```
