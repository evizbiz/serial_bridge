Serial Bridge
=============

This program provides a bridge between two serial devices connected
by USB to serial cables.  These are used, for example, in Lakeshore
temperature controllers.

The intent is to run the program on a small computer such as a
raspberry pi or a beagle bone.  As a man in the middle, the bridge
can act as a translator, converting one serial protocol into another,
or tying different serial devices together.

This version is set up specifically for talking to a Lakeshore 336
temperature controller.

Installation
------------

Clone the github repository onto your raspberry pi::

    cd ~
    git clone https://github.com/scattering/serial_bridge.git

Add a pointer to the ls336 program to */etc/rc.local*::

    sudo nano /etc/rc.local

Just before the *exit 0* line, add the following::

    python /home/pi/serial_bridge/ls336.py

Copy the rules file to */etc/udev/rules.d*::

    sudo cp serial_bridge/10-ftdi.rules /etc/udev/rules.d
    sudo chmod 644 /etc/udev/rules.d/10-ftdi.rules

When you restart the raspberry pi, it will automatically start
the bridge communication, even if there is no keyboard or screen
attached.

If you do not have a network connection, copy the current version
of the repository onto a usb drive:: 

    https://github.com/scattering/serial_bridge/archive/master.zip

and expand it on the raspberry pi.  This will create a directory
such as */home/pi/Desktop/serial_bridge-master* on your pi.  Either
adjust all the commands above to use this new directory in place of
*serial_bridge*, or move the directory to */home/pi* and rename it
to *serial_bridge*.

Configuration
-------------

The Rasbian operating system already contains drivers for the common
cp210x usb to serial connector, so no drivers need to be installed.

When a USB serial device is plugged in, it creates a /dev/ttyUSB*
device, where * is some small integer.  Unplug the device and plug
it back in, and the number may be different.  Plug two devices in
in a different order, and the they may have different numbers.  This
makes it difficult to work consistently on a headless box with no
user interface.

The solution to this problem is to set up a udev rule to create a
serial device named for the device which is plugged in.  In order
to do so, you first need to plug in your devices and run the 
following::

	usb-devices | grep "^[PS]\|^$"

This will produce output such as the following::

	P:  Vendor=1d6b ProdID=0002 Rev=03.12
	S:  Manufacturer=Linux 3.12.22+ dwc_otg_hcd
	S:  Product=DWC OTG Controller
	S:  SerialNumber=bcm2708_usb

	P:  Vendor=0424 ProdID=9514 Rev=02.00

	P:  Vendor=0424 ProdID=ec00 Rev=02.00

	P:  Vendor=067b ProdID=2303 Rev=03.00
	S:  Manufacturer=Prolific Technology Inc.
	S:  Product=USB-Serial Controller

	P:  Vendor=1fb9 ProdID=0301 Rev=01.00
	S:  Manufacturer=Silicon Labs
	S:  Product=Model 336 Temperature Controller
	S:  SerialNumber=336AB50

In our case, we were looking for the Model 336 Temperature Controller
and the USB-Serial Controller.  Using these values we can create
a rules file */etc/udev/rules.d/10-ftdi.rules*::

	SUBSYSTEMS=="usb", KERNEL=="ttyUSB*", ATTRS{idVendor}=="1fb9", ATTRS{idProduct}=="0301", NAME="ttyLakeshore336"
	SUBSYSTEMS=="usb", KERNEL=="ttyUSB*", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", NAME="ttyOutputRS232"

Set the proper permissions on the file::

	sudo chmod 644 /etc/udev/rules.d/10-ftdi.rules 

Next time the LS 336 is plugged in, a new */dev/ttyLakeshore336* link
will be created.

If you have multiple devices of the same type that can be connected at 
the same time, you will want to distinguish them by serial number.  For 
this particular Lakeshore 336, you would change the symlink to
string *ATTRS{serial}=="336AB50"* to the rule.

Changes to the configuration should be pushed back to the repository.
The following command shows details of what has been changed::

    git diff

The following command commits the changes to the repository::

    git commit -a -m "description of change"
    git push

Please use a meaningful description so that your future self remembers
why the change was done.

