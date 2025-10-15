# Raspberry Pi5: self-hosted GitHub runner

### Table of Contents
1. [Zephyr application - home page](../README.md)
2. [Add new board to project](Add_new_board_to_project.md)
3. [Artifactory storage server](Artifactory_storage_server.md)
4. [GitHub workflow_dispatch panel](Github_workflow_dispatch_panel.md)
5. [HW resources for tests](HW_resources_for_tests.md)
6. [Kconfig tester guide](Kconfig_tester_guide.md)
7. Raspi runner installation [this page]
8. [Shell tests with native_sim](Shell_tests_with_native_sim.md)
9. [Tests list](Tests_list.md)
10. [Tests user guide](Tests_user_guide.md)
---

Runners are the machines that execute jobs in a GitHub Actions workflow. The standalone GitHub self-hosted runner on Raspberry Pi5 (Raspi5) is used as default in this project for CI/CD workflows.

## Installing self-hosted GitHub runner on Raspi5

For basic guideline how to start the installation see the official GitHub page:  
[https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners)  

**PREREQUISITES:**

_Ubuntu 24.04 LTS desktop OS is installed on Raspberry Pi5._  

**To install the GitHub self-hosted runner on Raspberry Pi5, follow these steps:**

1\. On your host machine, open a terminal or command prompt. Run the commands provided by GitHub to download the runner package. GitHub runner is installed in the folder /home/\<user>/actions-runner/:

```
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.305.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.305.0/actions-runner-linux-x64-2.305.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.305.0.tar.gz
```

2\. When download is complete, configure the runner with your username, repo details and GitHub token provided in GitHub repository settings (where you are setting up the runner):

```
./config.sh --url https://github.com/your-username/your-repo --token YOUR_RUNNER_TOKEN
```

3\. Start the runner (without 'sudo' in command!):

```
./run.sh
```

4\. As most Raspberry Pis are running unattended you may want to start the runner service on your Raspi automatically as soon as the device boots up. For this, switch into the extracted folder from the initial setup and run the service install script:

```
cd /home/\<user>/actions-runner/  
sudo ./svc.sh install
```

5\. After installation you need to start the service once:

```
sudo ./svc.sh start
```

6\. The service can be controlled by following commands later if required:

```
sudo ./svc.sh status            --> check the service status
sudo ./svc.sh stop              --> stop the service
sudo ./svc.sh uninstall         --> uninstall the service 
```

7\. Once your runner is configured and running, you can specify it in your GitHub Actions workflow - see an example:

```
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: self-hosted
    steps:
    - uses: actions/checkout@v2
    - name: Run a one-line script
      run: echo "Hello, world!" 
```

  
  
## Additional utilities and workarounds

1\. To check the GutHub runner service process, you can use the following command (example for user 'pantoska-tieto' and repository name 'antoskape-project'):

```
peter@rpi5:~$ ls -la /etc/systemd/system/|grep runner
-rw-rw-r--  1 root root  309 Aug 11 10:39 actions.runner.pantoska-tieto-antoskape-project.rpi5.service
```

2\. If having an issues with GitHub service, check the service config file for correct settings (example for user 'pantoska-tieto' and repository name 'antoskape-project'):

```
peter@rpi5:~$ sudo nano /etc/systemd/system/actions.runner.pantoska-tieto-antoskape-project.rpi5.service
GNU nano 7.2  /etc/systemd/system/actions.runner.pantoska-tieto-antoskape-project.rpi5.service
Description=GitHub Actions Runner (pantoska-tieto-antoskape-project.rpi5)
After=network.target

[Service]
ExecStart=/home/peter/actions-runner/runsvc.sh
User=peter                                                      
WorkingDirectory=/home/peter/actions-runner
KillMode=process
KillSignal=SIGTERM
TimeoutStopSec=5min

[Install]
WantedBy=multi-user.target
```

3\. If you encounter an issue to open serial port when running hardware tests on real device through the GitHub CI/CD actions, check that your GitHub username has the necessary permissions to access the serial port - it belongs to 'dialout' group (serial device's group). You can add your user to the 'dialout' group by running the following command:

```
adduser <user> dialout
sudo usermod -aG dialout <user>
```

Once you have added your user to the 'dialout' group, you need to log out and log back in for the group changes to take effect. After that, you should be able to open the serial port without any issues. You can use the following command to verify the group membership:

```
getent group dialout
```

or to remove from dialout group, use:

```
sudo deluser <user> dialout
```