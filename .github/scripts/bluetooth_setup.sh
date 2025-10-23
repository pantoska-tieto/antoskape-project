#!/bin/bash

# This script is used for Bluetooth initiation on GitHub container level for BT tests.
# Current status on 23.10.2025:  BT HCI access is not working and causing error 
# for "mcumgr" commands:
# can't init hci: can't create socket: address family not supported by protocol

echo "Checking dbus-daemon status..."
if ! dbus-send --system --type=method_call --dest=org.freedesktop.DBus \
    /org/freedesktop/DBus org.freedesktop.DBus.ListNames &> /dev/null; then
    echo "dbus-daemon not responding, attempting restart"
    sudo pkill dbus-daemon || true
    sleep 1
    sudo rm -f /run/dbus/pid || echo "Could not remove /run/dbus/pid, might be locked"
    sudo dbus-daemon --system --fork
fi

echo "Waiting for dbus-daemon to become responsive..."
for i in {1..5}; do
    if dbus-send --system --type=method_call --dest=org.freedesktop.DBus \
        /org/freedesktop/DBus org.freedesktop.DBus.ListNames &> /dev/null; then
        echo "dbus-daemon is now responsive"
        break
    fi
    echo "DBus not ready yet, retrying in 1s..."
    sleep 1
done

# BT daemon initiation - on Host already, not needed in container!
# sudo bluetoothd & 

echo "Checking if bluetoothd is running..."
ps aux | grep bluetoothd

# Check for access to BT stack folders -> PASS
# echo "Confirm container has access to /sys/class/bluetooth/hci0..."
# ls /sys/class/bluetooth/
# ls /sys/class/bluetooth/hci0

# Check for access to BT stack folders -> PASS
# echo "Confirm container has access to /dev and /run/dbus..."t
# ls /dev
# ls /run/dbus/system_bus_socket

# Check for status of BT D-Bus -> PASS
# systemctl is not usable inside the container
# echo "systemctl status dbus..."
# sudo systemctl status dbus

# Check for BT daemon status
echo "bluetoothctl show..."
sudo bluetoothctl show

# Check for Linux BlueZ status
echo "Check bluetoothds..."
busctl tree org.bluez

# Show HCI status - not working and causing error:
# can't init hci: can't create socket: address family not supported by protocol
# No access to Host BT HCI stack!
# echo "Starting hciconfig command..."
# sudo hciconfig
echo "Mapping udev finished and Device udev-rules saved to $OUTPUT_FILE"