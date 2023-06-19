#!/usr/bin/python3
import time
import os

CMD_MOUNT = "modprobe g_mass_storage file=/piusb.bin stall=0 ro=1"
CMD_UNMOUNT = "modprobe -r g_mass_storage"

# Mount the filesystem as read-only for USB gadget mode
os.system(CMD_MOUNT)

# You could add whatever else you need here

