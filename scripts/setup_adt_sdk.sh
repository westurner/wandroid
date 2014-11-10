#!/bin/bash -x
# Download Android ADT SDK
# -------------------------
# https://developer.android.com/sdk/index.html

version="20140702"
prefix="${HOME}/.local/android"  # /opt/android"

UNAME=$(uname)
ARCH=$(uname -m)

if [ ${UNAME} == "Darwin" ]; then
    platformstr="mac"
    chownstr=$USER
    md5cmd="md5"
    browser="open"
elif [ ${UNAME} == "Linux" ]; then
    platformstr="linux"
    chownstr=$USER:$USER
    md5cmd="md5sum"
    browser="x-www-browser"
else
    echo "Unsupported platform: ${UNAME}"
    exit 1
fi

vername="adt-bundle-${platformstr}-${ARCH}-${version}"
archivename="${vername}.zip"
archiveurl="http://dl.google.com/android/adt/${archivename}"
destpath="${prefix}/${vername}"
adtprefix=${prefix}/adt

sudo mkdir -p ${prefix}
sudo chown ${chownstr} ${prefix}
(cd ${prefix} && \
    curl -fSL -C - "${archiveurl}" -o "${archivename}" && \
    ${md5cmd} "${archivename}" && \
    unzip -q ${archivename} -d ${prefix}/)

ln -s ${destpath}/ ${adtprefix}

echo ${browser} https://developer.android.com/sdk/installing/adding-packages.html &

${adtprefix}/sdk/tools/android update sdk &

