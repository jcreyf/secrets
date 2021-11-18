#!/bin/bash

# Copy the needed files from project folders:
cp ../ciphers.py main.py
cp ../ciphers.kv .
cp ../../secrets.py .

# Add comment to app:
sed -i '1 i\#' main.py
sed -i '1 i\# THIS FILE IS REQUIRED FOR BUILDOZER TO GENERATE THE ANDROID APP' main.py
sed -i '1 i\# THIS FILE IS AN EXACT COPY OF secrets.py!!!!' main.py
sed -i '1 i\#' main.py

# Todo: add a flag to "clean" (delete .buildozer and venv and bin directories before starting

buildozer android debug deploy run
if [ $? -eq 0 ] ; then
  echo "Build successful"
  ls -la ./bin/
#  scp ./bin/secrets*.apk 192.168.1.250:/tmp/
fi

#
# /home/jcreyf/.buildozer/android/platform/android-sdk/platform-tools/adb kill-server
# /home/jcreyf/.buildozer/android/platform/android-sdk/platform-tools/adb start-server
# /home/jcreyf/.buildozer/android/platform/android-sdk/platform-tools/adb devices
# /home/jcreyf/.buildozer/android/platform/android-sdk/platform-tools/adb usb
#

# /> lsusb
#   Bus 001 Device 016: ID 22b8:2e82 Motorola PCS XT1541 [Moto G 3rd Gen]
#
# Created udev file:
#   /lib/udev/rules.d/70-android-tools-adb.rules
#    #  SUBSYSTEM=="usb", ATTR{idVendor}=="22b8", ATTR{idProduct}=="2e82", MODE="0666", OWNER="jcreyf", TAG+="uaccess"
#      SUBSYSTEM=="usb", ATTR{idVendor}=="22b8", ATTR{idProduct}=="2e82", MODE="0666", OWNER="root", GROUP="androidadb", SYMLINK+="android%n"
#
# /> sudo groupadd androidadb
# /> sudo usermod -a -G androidadb jcreyf
#
# /> lsusb -v -d 22b8:2e82
#      iManufacturer           1 motorola
#      iProduct                2 moto z3
#
# /> lsusb -v -d 22b8:2e82 | grep -B 3 -i iInterface
#      bInterfaceClass       255 Vendor Specific Class
#      bInterfaceSubClass    255 Vendor Specific Subclass
#      bInterfaceProtocol      0
#      iInterface              5 MTP
#
# (this is apparently no longer needed in newer ADB versions):
# /> cat ~/.android/adb_usb.ini
#      0x22B8
#      0x2E82
#
