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

# Get the app's version info and write to the buildozer.spec file:
version=$(grep " __version__ " secrets.py | cut -d'"' -f2 | sed 's/ //g')
sed -i "s/^version = .*/version = ${version}/" buildozer.spec

# Todo: add a flag to "clean" (delete .buildozer and venv and bin directories before starting

# Select the correct Anaconda environment for this Python project:
conda activate secrets

# Build, deploy over USB and launch the app on the phone:
buildozer android debug deploy run

# Build, deploy over USB; launch the app on the phone and start capturing logs on the laptop:
#buildozer android debug deploy run logcat
if [ $? -eq 0 ] ; then
  echo "Build successful"
  ls -la ./bin/
  scp ./bin/secrets*.apk 192.168.1.250:/tmp/
  # Wait for a few seconds before trying to tail the apps's log.
  # Give the phone some time to launch the app:
  sleep 3s
  # Tail the app's log:
  adb logcat --pid=$(adb shell ps -e | grep jocreyf.com.secrets | tr -s [:space:] ' ' | cut -d' ' -f2)
fi

# Useful adb commands to debug potential issues:

# Get the PID of your app on the phone:
#  /> adb shell ps -e | grep jocreyf.com.secrets | tr -s [:space:] ' '
#  u0_a275 8915 1039 1113700 72416 0 0 S jocreyf.com.secrets
#
#  /> adb shell ps -e | grep jocreyf.com.secrets | tr -s [:space:] ' ' | cut -d' ' -f2
#  8915
#
#  /> adb logcat --pid=$(adb shell ps -e | grep jocreyf.com.secrets | tr -s [:space:] ' ' | cut -d' ' -f2)
