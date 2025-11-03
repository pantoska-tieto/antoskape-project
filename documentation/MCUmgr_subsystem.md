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
12. [Simulation/emulation principles in testing](Simulation_emulation_principles.md)
---

The Simple Management Protocol (SMP) provided by MCUmgr allows remote management of Zephyr-enabled devices. The following management operations can be done with this subsystem:<br/>

- Image management
- File System management
- OS management
- Settings (config) management
- Shell management
- Statistic management
- Zephyr management

over the following transports:

- Bluetooth Low Energy (LE)
- Serial (UART)
- UDP over IP

There are various tools and libraries available which enable usage of MCUmgr functionality - the `mcumgr` CLI tool is used in this repository for tests with Bluetooth stack.

- For more details about mcumbr-CLI tool see [mcumgr Command-line tool](https://docs.nordicsemi.com/bundle/ncs-3.0.2/page/nrf/app_dev/bootloaders_dfu/dfu_tools_mcumgr_cli.html) guide.
- mcumgr tool repository can be found here: [mcumgr GitHub repo](https://github.com/apache/mynewt-mcumgr).
- MCUmgr subsystem is described in official Zephyr [MCUmgr documentation](https://docs.zephyrproject.org/latest/services/device_mgmt/mcumgr.html).


<br/>

## Installation of mcumgr CLI tool

The tool is written in the Go programming language. Once Go is installed and set up on your system, you can install the mcumgr CLI tool.

```c
sudo apt-get update && sudo apt install golang-go 
go install github.com/apache/mynewt-mcumgr-cli/mcumgr@latest

# mcumgr is installed into $USER/go/bin/mcumgr by default

# Run the mcumgr command:
cd ~/go/bin$
sudo ./mcumgr
```

<br/>

## Usage of mcumbr CLI tool 

The argument `--conntype` determines what interface/transport is used for communication with the device (ble, serial etc.). The argument `--connstring` is used to specify the connection details of the device. All below examples are for "Bluetooth" interface used for communication with target device.

For handling with application <strong>image</strong> on target BT device the following commands are mostly used:

### Get image list

Get image list from target BT device over Bluetooth:<br/>
`$USER/go/bin/mcumgr --conntype ble --connstring peer_name='BLE_Name' image list`

The image is "active" and "confirmed", which means it will be executed again upon next reset.

<br/>

```c
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

```c
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

```c
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

```c
(.venv) peter@rpi5:~/zephyrproject/customer-application$ sudo ~/go/bin/mcumgr --conntype ble --connstring peer_name="BLE_Name" image list
Images:
    image=0 slot=0
        version: 0.0.0
        bootable: true
        flags: active confirmed		---> New FW is active!
        hash: 37dbff844a55ac7b55d3f830e5e3d7f6c6aec5b4e5cb5b332bc855ace01aad64
```

<br/>

## GitHub container and step-context (MCUmgr restrictions for BLE transport)
When using `mcumgr` tool in general GitHub workflow where the docker container is created within container: section (container-context) the usage of mcumgr commands fail with the following error for device `hci0`:

```c
[hci0]: can't init hci: can't create socket: address family not supported by protocol
```
<br/>

HCI sockets are not exposed as "/dev/devicesmeans" that menas `/dev/hci0` does not exist as a device file — they are accessed via <strong>AF_BLUETOOTH</strong> sockets in the <strong>kernel</strong>! Docker container cannot access this BT kernel socket through doecker-run arguments (--volume or -v flag/option), it needs an access to Host runner newtork (`--network` option) to get kernel-sockets available for access. As noted in official Github workflow documentation, the `--network` option is not supported in `jobs.<job_id>.container.options` what is crucial for resolving above issue - see [Setting container resource options](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/run-jobs-in-a-container). 


<br/>

Container-context in workflow .yml file:

```c
build:
    name: Build Zephyr workspace
    needs: [process-image, process-runner]
    runs-on: ${{ needs.process-runner.outputs.label }}
    outputs:
      testing: ${{ env.RUN_TESTS }}
      board_target: ${{ env.BOARD_TARGET }}
    defaults:
      run:
        working-directory: customer-application
    container:                                              ---> Section to define source image and container attributes!
      image: ${{ needs.process-image.outputs.image }}
      options: >
        --device=/dev/ttyUSB0 
        --privileged  
        -v /var/run/dbus:/var/run/dbus 
        -v /run/dbus:/run/dbus 
        -v /dev:/dev
        -e DBUS_SESSION_BUS_ADDRESS=unix:path=/run/dbus/system_bus_socket
    env:
      CMAKE_PREFIX_PATH: /opt/toolchains
```
<br/>

PROS:
- All operations in workflow steps are performed in docker container automatically without a need to run docker-commands.
- Simpe maintenance of steps-code because of automated integration Docker container - GitHub runner instance.

CONS:
- Restricted access to Host runner network through `--network` option. GitHub runner applies only a whitelisted set of options (like --volume, --env, --cpus, --memory) and explicitly disallows dangerous flags.
- Create container & install zephyr workspace steps are not persistent and must be triggered in each GitHub workflow file repeatedly (time and resource consuming).
- Docker container lifecycle is controlled by runner and container is removed at the end of job/workflow file.
- Container name during the workflow run is unpredictable (hashed by default). The manual manipulation with such container cannot be performed without a more complex scripting. 

<br/>

Because for BLE tests with mcumgr tool the access to AF_BLUETOOTH socket family is crucial condition (required for tools like bluetoothd, bluetoothctl, and BLE communication), the low level container run within GitHub workflow is necessary (direct access to Host runner network through `--network` option) - the step-context approach:

<br/>

Step-context in workflow .yml file:

```c
steps:					
    # Run docker container								
    - name: Run Zephyr Docker container
    shell: bash
    run: |
        docker run -d --name zephyr-env \
            --user $(id -u):$(id -g) \
            --device=/dev/ttyUSB0 \
            --cgroupns=host \
            --privileged \
            --network host \                            ---> Direct access to Host network!
            -v /var/run/dbus:/var/run/dbus \
            -v /run/dbus:/run/dbus \
            -v /dev:/dev \
            -v /etc/udev/rules.d:/etc/udev/rules.d \
            -v /sys/class/bluetooth:/sys/class/bluetooth \
            -e DBUS_SESSION_BUS_ADDRESS=unix:path=/run/dbus/system_bus_socket \
            -e CMAKE_PREFIX_PATH=/opt/toolchains \
            -w /workspace/customer-application \
            ${{ needs.process-image.outputs.image }} \
            sleep infinity
```
<br/>

In contrast to container-context the step-context requires to call "docker exec \<container-name\>" command in each ongoing steps of the workflow to invoke required commands/actions. See example:

```c
# Install Python packages
- name: Install Python extra packages
shell: bash
run: |
    docker exec -u root zephyr-env \
    bash -c "pip install -r requirements-extras.txt"
```
<br/>

PROS:
- Full access to Host network and all resources through docker `--network` option.
- Wider maintenance options to control docker container, which is running out of GitHub runner control layer.
- Docker container can be triggered with flag `sleep infinity` and thus available for all GitHub workflow files/jobs - persistent docker container lifecycle.

CONS:
- All operations in workflow steps require explicit access to docker container with docker-commands.
- More developer errors prone and more complex debugging for workflow steps code.
- Docker lifecycle is not controlled automatically by GitHub network and must be manually managed in the code (stop & remove container).

<br/>

## Kconfig versus mcumgr tool
The Kconfig file plays an important role in setup for `mcumgr` tool. Check all mandatory Kconfig symbols are present in sample.yaml or testcase.yaml files to get mcumgr-tool working properly!