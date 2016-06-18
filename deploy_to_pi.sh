#!/bin/bash

{

rsync --exclude=".*/" --delete-excluded -avz ~/camcamcam/ tommy@magicmike.local:~/camcamcam/

if [ "$1" == '--install' ]; then
    ssh tommy@magicmike.local "
        sudo apt-get install python-dev
        sudo apt-get install python-pip
        sudo pip install flask
    "
fi

}
