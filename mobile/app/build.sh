#!/bin/bash

# Copy the .py file from project folder:
cp ../ciphers.py main.py
cp ../ciphers.kv main.kv

# Add comment to app:
#sed -i '1 i\#' main.py
#sed -i '1 i\# THIS FILE IS REQUIRED FOR BUILDOZER TO GENERATE THE ANDROID APP' main.py
#sed -i '1 i\# THIS FILE IS AN EXACT COPY OF ledstrips.py!!!!' main.py
#sed -i '1 i\#' main.py

# Todo: add a flag to "clean" (delete .buildozer and venv and bin directories before starting

buildozer android debug deploy run
if [ $? -eq 0 ] ; then
  echo "Build successful"
  ls -la ./bin/
  scp ./bin/secrets*.apk 192.168.1.250:/tmp/
fi
