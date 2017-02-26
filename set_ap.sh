#!/bin/bash
clear

#  ARG 1 sets Rpi to be WiFi access host
#  ARG 0 return to original set

echo AAAA

if [ "$1" = 1 ]
then
	echo  "WiFi HotSpot is being created"
        sudo cp /etc/network/interfaces.hostapd /etc/network/interfaces
        sudo cp /etc/sysctl.conf.hostapd /etc/sysctl.conf
	sudo cp /etc/dhcpcd.conf.hostapd /etc/dhcpcd.conf
	sudo cp /etc/default/hostapd.zz.hostapd /etc/default/hostapd
	sudo service hostapd start
        sudo service dnsmasq start
        sudo ifdown wlan0
	sudo ifup wlan0
else
        echo  "WiFi HotSpot is being replaced with orig WiFi"
        sudo cp /etc/network/interfaces.orig /etc/network/interfaces
        sudo cp /etc/sysctl.conf.orig /etc/sysctl.conf
        sudo cp /etc/dhcpcd.conf.orig /etc/dhcpcd.conf
        sudo cp /etc/default/hostapd.orig /etc/default/hostapd
        sudo service hostapd stop
        sudo service dnsmasq stop
        sudo ifdown wlan0
        sudo ifup wlan0
fi
