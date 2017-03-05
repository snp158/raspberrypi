#!/bin/bash
 
#HOST=murino.ddns.net
HOST=192.168.2.1
PPTPUSER=zaharovo
PPTPPASS=Pandora2016$
 
DATE=`date`
PINGRES=`ping -c 2 $HOST`
PLOSS=`echo $PINGRES : | grep -oP '\d+(?=% packet loss)'`
echo "$DATE : Loss Result : $PLOSS"
 
if [ "100" -eq "$PLOSS" ];
then
    echo "$DATE : Starting : $HOST"
    /usr/sbin/pptp pty file /etc/ppp/options.pptp user $PPTPUSER password $PPTPPASS
    echo "$DATE : Now running : $HOST"
else
    echo "$DATE : Already running : $HOST"
fi

