# MCUmgr subsystem for testing purposes

### Table of Contents
1. [Zephyr application - home page](../README.md)
2. [Add new board to project](Add_new_board_to_project.md)
3. [Artifactory storage server](Artifactory_storage_server.md)
4. [GitHub workflow_dispatch panel](Github_workflow_dispatch_panel.md)
5. [HW resources for tests](HW_resources_for_tests.md)
6. [Kconfig tester guide](Kconfig_tester_guide.md)
7. [Raspi runner installation](Raspi_runner_installation.md)
8. [Shell tests with native_sim](Shell_tests_with_native_sim.md)
9. [Tests list](Tests_list.md)
10. [Tests user guide](Tests_user_guide.md)
11. MCUmgr subsystem for testing purposes [this page]
---

The MCUmgr management subsystem allows remote management of Zephyr-enabled devices.  There are various tools and libraries 
available which enable usage of MCUmgr functionality - the `mcumgr` CLI tool is used in this repository for tests with Bluetooth stack.

- For more details about mcumbr-CLI tool see [mcumgr Command-line tool](https://docs.nordicsemi.com/bundle/ncs-3.0.2/page/nrf/app_dev/bootloaders_dfu/dfu_tools_mcumgr_cli.html) guide.
- mcumgr tool repository can be found here: [mcumgr GitHub repo](https://github.com/apache/mynewt-mcumgr).
- MCUmgr subsystem is described in official Zephyr [MCUmgr documentation](https://docs.zephyrproject.org/latest/services/device_mgmt/mcumgr.html).


<br/>

## Installation of mcumgr CLI tool

The tool is written in the Go programming language. Once Go is installed and set up on your system, you can install the mcumgr CLI tool.

```
sudo apt-get update && sudo apt install golang-go 
go install github.com/apache/mynewt-mcumgr-cli/mcumgr@latest

# mcumgr is installed into $USER/go/bin/mcumgr by default

# Run the mcumgr command:
cd ~/go/bin$
sudo ./mcumgr
```

<br/>

## Usage of mcumbr CLI tool 

`mcumgr` provides the tools for:<br/>
- image management, 
- file system management, 
- OS management.

The argument `--conntype` determines what interface is used for communication with the device (ble, serial etc.). The argument `--connstring` is used to specify the connection details of the device. All below examples are for "Bluetooth" interface used for communication with target device.

For handling with application <strong>image</strong> on target BT device the following commands are mostly used:

### Get image list

Get image list from target BT device over Bluetooth:<br/>
`$USER/go/bin/mcumgr --conntype ble --connstring peer_name='BLE_Name' image list`

The image is "active" and "confirmed", which means it will be executed again upon next reset.

<br/>

```
(.venv) peter@rpi5:~/zephyrproject/customer-application$ sudo ~/go/bin/mcumgr --conntype ble --connstring peer_name="BLE_Name" image list
Images:
    image=0 slot=0
        version: 0.0.0
        bootable: true
        flags: active confirmed	
        hash: fa44c7da72d97c2c8b56bc35723d552be80348697017c81628d355bac5ea256d
```
<br/>

### Upload new image to the device

Flash new image to target BT device (must be build before uploading! Below example uses default signed-image built in build/ folder):<br/>
`$USER/go/bin/mcumgr --conntype ble --connstring peer_name="BLE_Name" image upload build/smp_svr/zephyr/zephyr.signed.bin`

<br/>

### Verify a successfull upload of new image

Get image list from target BT device over Bluetooth. New image is listed besides the current firmware (flags = active running)<br/>
`$USER/go/bin/mcumgr --conntype ble --connstring peer_name='BLE_Name' image list`

<br/>

```
(.venv) peter@rpi5:~/zephyrproject/customer-application$ sudo ~/go/bin/mcumgr --conntype ble --connstring peer_name="BLE_Name" image list
Images:
    image=0 slot=0
        version: 0.0.0
        bootable: true
        flags: active confirmed	
        hash: fa44c7da72d97c2c8b56bc35723d552be80348697017c81628d355bac5ea256d
    image=0 slot=1
		version: 0.0.0
		bootable: true
		flags: 					---> New image!
		hash: 37dbff844a55ac7b55d3f830e5e3d7f6c6aec5b4e5cb5b332bc855ace01aad64
```

<br/>

### Get ready the image for DFU

Update the state of new-test image to "pending". Apply the image-hash string found by previous "image list" mcumgr commands!<br/>
`$USER/go/bin/mcumgr --conntype ble --connstring peer_name="BLE_Name" image test 37dbff844a55ac7b55d3f830e5e3d7f6c6aec5b4e5cb5b332bc855ace01aad64`

The image gets status "pending", which means it will be executed again upon next reset. This command initiates a test upgrade, indicating that after the next reboot, the bootloader will execute the upgrade and switch to the new image marked as "pending". 

<br/>

```
(.venv) peter@rpi5:~/zephyrproject/customer-application$ sudo ~/go/bin/mcumgr --conntype ble --connstring peer_name="BLE_Name" image list
Images:
    image=0 slot=0
        version: 0.0.0
        bootable: true
        flags: active confirmed	
        hash: fa44c7da72d97c2c8b56bc35723d552be80348697017c81628d355bac5ea256d
    image=0 slot=1
        version: 0.0.0
        bootable: true
        flags: pending		   ---> Change to be ready for update!
        hash: 37dbff844a55ac7b55d3f830e5e3d7f6c6aec5b4e5cb5b332bc855ace01aad64
```

<br/>  

### Reset the target device to perform DFU operation

Perform a soft reset of a device:<br/>
`$USER/go/bin/mcumgr --conntype ble --connstring peer_name="BLE_Name" reset`

The FW image with previous status "pending" is applied after soft reset. The "image list" command executed after soft reset confirms a successful DFU operation:

<br/>

```
(.venv) peter@rpi5:~/zephyrproject/customer-application$ sudo ~/go/bin/mcumgr --conntype ble --connstring peer_name="BLE_Name" image list
Images:
    image=0 slot=0
        version: 0.0.0
        bootable: true
        flags: active confirmed		---> New FW is active!
        hash: 37dbff844a55ac7b55d3f830e5e3d7f6c6aec5b4e5cb5b332bc855ace01aad64
```

<br/> 

## Kconfig versus mcumgr tool
The Kconfig file plays an important role in setup for `mcumgr` tool. Check all mandatory Kconfig symbols are present in sample.yaml or testcase.yaml files to get mcumgr-tool working properly!