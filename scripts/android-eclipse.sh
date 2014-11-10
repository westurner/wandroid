#!/bin/bash -x

echo "ANDROID_WORKSPACEPATH=${ANDROID_WORKSPACEPATH}"

UNAME=$(uname)
if [ ${UNAME} == "Darwin" ]; then
    open ${ANDROID_ADTPATH}/eclipse/Eclipse.app &
elif [ ${UNAME} == "Linux" ]; then
    ${ANDROID_ADTPATH}/eclipse/eclipse.sh &  # TODO
fi
