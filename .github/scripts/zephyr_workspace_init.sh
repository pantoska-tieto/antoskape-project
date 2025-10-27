
#!/bin/bash
set -e
export HOME=/tmp
cd /workspace/customer-application
git config --global --add safe.directory "/workspace/zephyr"
git config --global --add safe.directory "/workspace/modules/lib/uoscore-uedhoc"
git config --global --add safe.directory "/workspace/modules/lib/zcbor"
echo 'Initializing Zephyr environment...'
pwd
echo 'Current github workspace:'
ls -la
echo 'Parent github folder'
ls -la ..
rm -rf ../.west
west init -l .
west update -o=--depth=1 -n
west blobs fetch hal_espressif"