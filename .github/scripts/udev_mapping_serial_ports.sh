#!/bin/bash

# Target board variable from GitHub dispatch event
TARGET="$1"

# Content of udev-rules file
OUTPUT_FILE="udev_mapping.txt"
> "$OUTPUT_FILE"

if [[ "$TARGET" == esp32* ]]; then
    VENDOR="esp32"
    PORT="/dev/ttyUSB"
elif [[ "$TARGET" == nrf* ]]; then
    VENDOR="nrf"
    PORT="/dev/ttyACM"
elif [[ "$TARGET" == native_sim* || "$TARGET" == qemu* ]]; then
    echo "Skipped searching for udevadm target for simulation: $TARGET"
    exit 0
else
    echo "No vendor found for: $TARGET"
    exit 1
fi

# Internal counter for multiple ports symlinks
serial_counter=0

# Loop through all ttyUSB devices
for DEV in ${PORT}*; do
    # Filter existing ports
    [ -e "$DEV" ] || continue
    echo "Processing serial port $DEV"

    # Get udev info
    INFO=$(udevadm info -a -n "$DEV")

    # Extract first occurrence of idVendor, idProduct (and serial)
    ID_VENDOR=$(echo "$INFO" | grep -m 1 'ATTRS{idVendor}' | awk -F '=="' '{print $2}' | tr -d '"')
    ID_PRODUCT=$(echo "$INFO" | grep -m 1 'ATTRS{idProduct}' | awk -F '=="' '{print $2}' | tr -d '"')
    SERIAL=$(echo "$INFO" | grep -m 1 'ATTRS{serial}' | awk -F '=="' '{print $2}' | tr -d '"')

    # echo "SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"$ID_VENDOR\", ATTRS{idProduct}==\"$ID_PRODUCT\", SYMLINK+=\"${VENDOR}_${serial_counter}\"" | sudo tee -a "$OUTPUT_FILE" > /dev/null
    echo "SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"$ID_VENDOR\", ATTRS{idProduct}==\"$ID_PRODUCT\", ATTRS{serial}==\"$SERIAL\", SYMLINK+=\"${VENDOR}_${serial_counter}\"" | sudo tee -a "$OUTPUT_FILE" > /dev/null

    # Copy local file to new udev rule
    sudo cp $OUTPUT_FILE /etc/udev/rules.d/99-$VENDOR.rules
    echo "Verify permissions for udev-rules file..."
    cat /etc/udev/rules.d/99-$VENDOR.rules
    # Reload udev rules
    echo "udevadm: reload-rules..."
    sudo udevadm control --reload-rules || echo "Error for udevadm reload-rules."
	sudo udevadm trigger || echo "Error for udevadm reload-rules."
    echo "Show symlinks for serial ports..."
    ls -la /dev/ | grep USB
    # Increment for further serial port
    ((serial_counter++))
    sleep 2
done

echo "Mapping udev finished and Device udev-rules saved to $OUTPUT_FILE"