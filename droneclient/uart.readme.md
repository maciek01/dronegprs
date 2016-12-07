
#setting up RPi3 UART


  sudo vi /boot/config.txt

Add to the end of the file

  dtoverlay=pi3-disable-bt

We also need to run to stop BT modem trying to use UART

  sudo systemctl disable hciuart

(See RasPi device tree commit for pi3-disable-bt and raspi forum thread discussion)
Reboot and test serial coms with:

  sudo minicom -D /dev/ttyAMA0 -b38400




Next

  sudo vi /boot/cmdline.txt

If you see:

  console=/dev/ttyS0,115200 

Or:

  console=/dev/serial0,115200 

Or anything involving console= that isn't console=tty1, remove it. Make sure not to accidentally add a line break to that file, it should remain all one line with spaces between the options, but no spaces around any =.

The other aspect is the login started by the init system. On Raspbian jessie, check:

ls /etc/systemd/system/getty.target.wants
If you see that serial device node (ttyS0) mentioned, disable this service:

  systemctl disable serial-getty@ttyS0.service

