#!/bin/bash

# Target board variable from GitHub dispatch event
TARGET="$1"

# Output file for udev rules
OUTPUT_FILE="udev_mapping.txt"
> "$OUTPUT_FILE"

# Determine vendor and port prefix
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

serial_counter=0

# Loop through all matching serial ports
for DEV in ${PORT}*; do
    [ -e "$DEV" ] || continue
    echo "Processing serial port $DEV"

    # For nRF boards, skip ttyACM0 (network core), only use ttyACM1
    if [[ "$VENDOR" == "nrf" && "$DEV" == "/dev/ttyACM0" ]]; then
        echo "Skipping $DEV (network core)"
        continue
    fi

    # Get udev info
    INFO=$(udevadm info -a -n "$DEV")

    # Extract idVendor, idProduct, and serial
    ID_VENDOR=$(echo "$INFO" | grep -m 1 'ATTRS{idVendor}' | awk -F '=="' '{print $2}' | tr -d '"')
    ID_PRODUCT=$(echo "$INFO" | grep -m 1 'ATTRS{idProduct}' | awk -F '=="' '{print $2}' | tr -d '"')
    SERIAL=$(echo "$INFO" | grep -m 1 'ATTRS{serial}' | awk -F '=="' '{print $2}' | tr -d '"')

    # Write udev rule
    echo "SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"$ID_VENDOR\", ATTRS{idProduct}==\"$ID_PRODUCT\", ATTRS{serial}==\"$SERIAL\", SYMLINK+=\"${VENDOR}_${serial_counter}\"" | sudo tee -a "$OUTPUT_FILE" > /dev/null

    ((serial_counter++))
    sleep 2
done

# Apply rules
if [[ $serial_counter -gt 0 ]]; then
    # Copy local file to new udev rule
    sudo cp "$OUTPUT_FILE" /etc/udev/rules.d/99-$VENDOR.rules
    echo "File with udevadm rules:"
    cat /etc/udev/rules.d/99-$VENDOR.rules
    echo "udevadm: reload-rules..."
    sudo udevadm control --reload-rules || echo "Error for udevadm reload-rules."
    sudo udevadm trigger || echo "Error for udevadm reload-rules."
    echo "Symlinks created:"
    ls -la /dev/ | grep -E "${VENDOR}|tty(USB|ACM)"
else
    echo "No matching devices found for $TARGET"
fi

echo "Mapping udev finished and rules saved to $OUTPUT_FILE"
