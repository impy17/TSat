#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

if [ ! -e /etc/service/tsat/run ]
then
    echo "Installing python script to run on boot"

    mkdir -p /etc/service/tsat

    echo '#!/bin/bash' > /etc/service/tsat/run
    echo 'exec /usr/bin/python /home/pi/TSat/tiny_sat.py' >> /etc/service/tsat/run

    chmod u+x /etc/service/tsat/run

else
    echo "Already installed"
fi

