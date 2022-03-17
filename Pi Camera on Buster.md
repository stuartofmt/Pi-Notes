## Pi Camera on Buster

Buster and previous releases use what is now referred to as the legacy libraries.

## Enable the Pi Camera

```
sudo raspi-config
    Interface Option
        Camera       
```

## Testing the Camera

```
raspistill -v -o test.jpg       
```