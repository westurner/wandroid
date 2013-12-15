#!/bin/sh
# Download Android ADT SDK
# -------------------------
# https://developer.android.com/sdk/index.html

version="20131030"
vername="adt-bundle-linux-x86-$version"
#vername="adt-bundle-linux-x86_64-$version"
archive="$version.zip"
android="/opt/android"

sudo mkdir -p $android
sudo chown $USER:$USER $android
cd $android

curl -fSL 'http://dl.google.com/android/adt/$archive' -O
unzip $archive -d
ln -s $android/$vername $android/adt

