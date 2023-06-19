# NunaAirQual

## Initial USB Setup Details

Process taken from https://magpi.raspberrypi.com/articles/pi-zero-w-smart-usb-flash-drive and https://magpi.raspberrypi.com/articles/pi-zero-w-smart-usb-flash-drive

### 1. Enable the DCW2 USB Driver

Open config.txt file: `sudo nano /boot/config.txt`
Add this text to the end of the file: `dtoverlay=dwc2`
Open modules: `sudo nano /etc/modules`
Add this text to the end of the file: `dwc2`

> JJS notes:
> I couldn't get into the Pi to do this (durr...), so had to add `modules-load=dwc2,g_ether` after `rootwait` in `cmdline.txt`.

### 2. Swap USB port

Power off the Pi and then plug into your computer using a USB cable connected to the middle micro USB port.

### 3. Create storage file

Create an empty 2GB binary file `sudo dd bs=1M if=/dev/zero of=/piusb.bin count=2048`
Format the file as a FAT32 file system. `sudo mkdosfs /piusb.bin -F 32 -I`

### 4. Mount the file

Create a folder on which we can mount the file system: `sudo mkdir /mnt/usb_share`
Add this to fstab `sudo nano /etc/fstab` Append the line below to the end of the file: `/piusb.bin /mnt/usb_share vfat users,umask=000 0 2`
Now mount the folder `sudo mount -a`

### 5. Start Mass Storage Device mode

Mount the mass storage device `sudo modprobe g_mass_storage file=/piusb.bin stall=0 ro=1`
If the Pi is connected to your computer using the second, more central usb port it should now show up as a external usb drive.
You can unmount using `sudo modprobe -r g_mass_storage`

### 6. Configure to start USB device at boot

Open the bashrc file `sudo nano /home/pi/.bashrc`
Go to the last line of the script and add: `sudo modprobe g_mass_storage file=/usb-drive.img stall=0 removable=1` (JJS note: *presumably piusb.bin*)
Restart the RPi: `sudo reboot`

### 7. Enable AutoLogin

I'm not sure if this is strictly needed (JJS: *it is, as your modprobe only runs on login. See below for alternative*)
Run `sudo raspi-config`.
Then configure - Boot Options -> Desktop / CLI -> Console Autologin

### 6a. JJS: alternate autostart approach

1. Copy the `autorun_example.py` script to `~/NUNA/autorun_example.py`.
2. Edit `nuna_air_qual.service` with your username (two places), then copy it to `/etc/systemd/system/`.
3. Test the service with `sudo systemctl start nuna_air_qual.service`

You may also need to do `sudo systemctl daemon-reload`. Assuming things seem to work, `sudo systemctl start nuna_air_qual.service` is your friend.

Note that I'm note entirely sure if this is going to work properly as-is, in that it might exit the script (it's only running the modprobe command), then immediately relaunch it. That problem goes away once you have an actual loop in the autorun script.

My [DataBot code](https://github.com/jjsanderson/DataBot/blob/main/databot.py) isn't great, but it seems entirely solid on a basic Pi Zero W, with no memory leaks I've noticed. I think the longest I've left it running is about a year. The RepeatedTimer class there is very straightforward and works nicely for simulating background update threads and keeping the main loop short. That said, I'm only firing it every 30 mins or so; if you're looking to capture data much more rapidly it would need testing more rigorously.
