#!/usr/bin/env bash
TARGET=${1:-"dev"}
NAME=${1:-"dev"}
HOSTNAME=$(hostname)

if [[ $TARGET == '*' ]]; then
	read -p "Are you sure you want to deploy to ALL hosts?" 
	NAME="all"
fi

echo "sending OTA to $TARGET"
pio run && cp .pio/build/ota/firmware.bin "builds/firmware-$NAME.bin" && mosquitto_pub -h 192.168.1.101 -t "/ota/$TARGET" -m "http://192.168.1.101/ota/$HOSTNAME/firmware-$NAME.bin"
