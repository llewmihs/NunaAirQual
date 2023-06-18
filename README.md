# NunaAirQual
## Initial USB Setup Details
Process taken from https://magpi.raspberrypi.com/articles/pi-zero-w-smart-usb-flash-drive and https://magpi.raspberrypi.com/articles/pi-zero-w-smart-usb-flash-drive
### 1. Enable the DCW2 USB Driver
Open config.txt file: `sudo nano /boot/config.txt`  
Add this text to the end of the file: `dtoverlay=dwc2`  
Open modules: `sudo nano /etc/modules`  
Add this text to the end of the file: `dwc2`   
### 2. Swap USB port
Poweroff the Pi and then plug into your computer using a USB cable connected to the middle micro USB port.  
### 3. Create storage file
Create an empty 2GB binary file `sudo dd bs=1M if=/dev/zero of=/piusb.bin count=2048`  
Format the file as a FAT32 file system. `sudo mkdosfs /piusb.bin -F 32 -I` 
### 4. Mount the file
Create a folder on which we can mount the file system: `sudo mkdir /mnt/usb_share`  
Add this to fstab `sudo nano /etc/fstab` Append the line below to the end of the file: `/piusb.bin /mnt/usb_share vfat users,umask=000 0 2`  
Now mount the folder `sudo mount -a`
### 5. Start Mass Sotrage Device mode
Mount the mass storage device `sudo modprobe g_mass_storage file=/piusb.bin stall=0 ro=1`  
If the Pi is connected to your computer using the second, more cetral usb port it should now show up as a external usb drive. 
You can unmount using `sudo modprobe -r g_mass_storage`  
### 6. Configure to start USB device at boot
Open the bashrc file `sudo nano /home/pi/.bashrc`  
Go to the last line of the script and add: `sudo modprobe g_mass_storage file=/usb-drive.img stall=0 removable=1`  
Restart the RPi: `sudo reboot` 
### 7. Enable AutoLogin
I'm not sure if this is strictly needed...  
Run `sudo raspi-config`. 
Then configure - Boot Options -> Desktop / CLI -> Console Autologin
