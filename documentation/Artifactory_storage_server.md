# Artifactory storage server

### Table of Contents
1. [Zephyr application - home page](../README.md)
2. [Add new board to project](Add_new_board_to_project.md)
3. Artifactory storage server[this page]
4. [GitHub workflow_dispatch panel](Github_workflow_dispatch_panel.md)
5. [HW resources for tests](HW_resources_for_tests.md)
6. [Kconfig tester guide](Kconfig_tester_guide.md)
7. [Raspi runner installation](Raspi_runner_installation.md)
8. [Shell tests with native_sim](Shell_tests_with_native_sim.md)
9. [Tests list](Tests_list.md)
10. [Tests user guide](Tests_user_guide.md)
11. [MCUmgr subsystem for testing purposes](MCUmgr_subsystem_for_testing_purpose.md)
12. [Simulation/emulation principles in testing](Simulation_emulation_principles.md)
---

For storing the binaries and other artifacts, the project uses Artifactory storage server. Artifactory is a repository manager that allows you to store and manage your artifacts in a centralized location. The project uses Fre version of <strong>JFrog Artifactory (Freemium)</strong> - self-hosted version. The Artifactory server is configured to store the binaries and other artifacts in a centralized location, which makes it easy to manage and access the artifacts from anywhere in the organization. Actually the test results records are stored in Artifactory server - `metadata.json` file with incremental test results generated each time when Testing GitHub workflow is executed. At this development phase no other binaries are archived in Artifacory but the system is prepared for smooth integration of other artifacts to be stored in Artifacts in future. The only restriction is 2GB of storage space per repository. If you need to store more than 2GB of artifacts data, you can use Artifactory Pro or other paid storage solutions. For more details see [JFROG ARTIFACTORY OPEN SOURCE ](https://jfrog.com/community/download-artifactory-oss/) page.

<strong>JFrog Container Registry (Freemium)</strong> Artifactory is available as <strong>self-hosted</strong> storage manager and can be installed in various operating systems (Debian, Ubuntu, Windows) together with PostgreSQL database (recommended). In case of this project the JFrog Container Registry was installed in <strong>VMware® Workstation 17 Pro virtual machine (preinstalled with Ubuntu 24.04 LTS)</strong> on Windows 11 laptop.

<br/>

## Installing Artifactory on VMWare  

For basic guideline how to install Artifactory on various operating systems follow the official JFrog documentation:  
[https://jfrog.com/help/r/jfrog-installation-setup-documentation/installing-artifactory](https://jfrog.com/help/r/jfrog-installation-setup-documentation/installing-artifactory)<br/>
<br/>

**PREREQUISITES:**

JFrog Platform requires filestore and database services:

- The filestore where binaries are physically stored.

- The database that maps a file’s checksum to its physical storage, and many operations on files within repositories are implemented as transactions in the database. Recommended database system for single self-hosted system use cases is PostgreSQL.

<br/>

1\. Install PostgreSQL database on your host machine if not available yet. You can install PostgreSQL using the following commands on Ubuntu 24.04 LTS:
<br/>


```c
sudo apt update
sudo apt install postgresql

sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgres

# Check the functional PostgreSQL DB if listening on port 5432
sudo netstat -tuln | grep 5432
tcp        0      0 127.0.0.1:5432          0.0.0.0:*               LISTEN

```

<br/>

2.\ Download the JFrog Container Registry (Freemium) installation .tar.gz package from the [JFrog website](https://jfrog.com/container-registry/) - go to the page bottom and click on <strong>SELF-HOSTED</strong> (FREE DOWNLOAD) button - and extract it to a directory of your choice. The recommended target installation folder is:

```c
/usr/local/jfrog/artifactory/
```

<br/>


3.\ Setup the environment variables for Artifactory installation:<br/>

```c
export JFROG_HOME=/usr/local/jfrog
```

<br/>

4.\ Start installation process by running the following commands in the Artifactory installation directory:

```c
cd $JFROG_HOME/artifactory/app/bin
./installService.sh
```

<br/>

5.\ Set up Artifactory Database. Artifactory requires an external database for production. JFrog highly recommends using <strong>PostgreSQL</strong> for all products in the JFrog Platform, although Artifactory supports additional databases. Edit the configuration file `$JFROG_HOME/artifactory/var/etc/system.yaml` to point Artifactory to your external database. For minimal setup in VMWare machine the following parameters should be set:

<br/>

```c
## @formatter:off
## JFROG ARTIFACTORY SYSTEM CONFIGURATION FILE
## HOW TO USE: comment-out any field and keep the correct yaml indentation by deleting only the leading '#' character.
configVersion: 1
## NOTE: JFROG_HOME is a place holder for the JFrog root directory containing the deployed product, the home directory for all JFrog products.
## Replace JFROG_HOME with the real path! For example, in RPM install, JFROG_HOME=/opt/jfrog

## NOTE: Sensitive information such as passwords and join key are encrypted on first read.
## NOTE: The provided commented key and value is the default.

## SHARED CONFIGURATIONS
## A shared section for keys across all services in this config
shared:
  ## Java 21 distribution to use
  javaHome: "/usr/local/jfrog/artifactory/app/third-party/java"							
  ## Extra Java options to pass to the JVM. These values add to or override the defaults.
  #extraJavaOpts: "-Xms512m -Xmx2g"

  ## Security Configuration
  security:
    ## Join key value for joining the cluster (takes precedence over 'joinKeyFile')
    #   joinKey: "<Your joinKey>"

    ## Join key file location
    joinKeyFile: "/usr/local/jfrog/artifactory/var/etc/security/join.key"
    ## Master key file location
    ## Generated by the product on first startup if not provided
    masterKeyFile: "/usr/local/jfrog/artifactory/var/etc/security/master.key"
    ## Maximum time to wait for key files (master.key and join.key)
    #bootstrapKeysReadTimeoutSecs: 120
    #
  ## Node Settings
  node:
    ## A unique id to identify this node.
    ## Default auto generated at startup.
    id: "art1"
    ## Default auto resolved by startup script
    # ip: 

    ## Sets this node as primary in HA installation
    primary: true
    ## Sets this node as part of HA installation
    haEnabled: true
  ## Database Configuration
  database:
    ## To run Artifactory with any database other than PostgreSQL allowNonPostgresql set to true.
    #   allowNonPostgresql: false

    ## One of mysql, oracle, mssql, postgresql, mariadb
    ## Default Embedded derby

    ## Example for postgresql
    type: postgresql
    driver: org.postgresql.Driver
    url: "jdbc:postgresql://localhost:5432/artifactory"				
    username: XXXXXXXX                               --> use your own username!
    password: XXXXXXXX                               --> use your own password!
user: artifactory
group: artifactory
access:

## Extra Java options to pass to the JVM. These values add to or override the defaults.
#extraJavaOpts: "-XX:InitialRAMPercentage=20 -XX:MaxRAMPercentage=25"
```
<br/>

6.\ Start as an OS Service (Recommended for Production). As mentioned in outputs from previous installation steps, the Artifactory service should be started for the first time manually to complete PostgreSQL installation process (see step 5):

```c
# For systemd-based systems
sudo systemctl start artifactory.service 

# For systemd-base, enable it to start on boot
sudo systemctl enable artifactory.service
```
<br/>

NOTE:<br/>
Later on you can check/restart/stop the service by running the following commands (for systemd-based systems):

```c
Start Artifactory with:
> systemctl start artifactory.service

Check Artifactory status with:
> systemctl status artifactory.service

Stop Artifactory with:
> systemctl stop artifactory.service

Restart Artifactory with:
> systemctl restart artifactory.service
```
<br/>

7.\ If no error appears in previous installation steps, you can open the URL in web-browser and conclude the initial setup of Artifactory management system:

http://localhost:8082 


Youu can add custom domain name into the `BASE URL` parameter (e.g.  http://mytest-artifactory.com) and reach the Artifactory storage system from any network station. For this purpose the update of hosts file on the client machine is required to map the custom domain name to the IP address of the Artifactory server. Edit the hosts file in Lunux machine:
		

```c
sudo nano /etc/hosts

# Then add the following line to hosts file
127.0.0.1   mytest-artifactory.com
```
<br/>

## Troubleshooting 

In case of issues with Artifactory installation, you can check the logs in the `$JFROG_HOME/artifactory/var/log/artifactory-service.log`. The logs provide detailed information about the installation process and any errors that occurred during the installation.


### Error for missing PostgreSQL username in installation step 6.

If you encounter an error related to missing PostgreSQL username in the installation step 6, you can follow these steps to resolve the issue:

```c
# Open PostgreSQL terminal in command line
sudo -u postgres psql

# Show all users in PostgreSQL
\du

# Add 'artifactory' user and password into DB if missing
CREATE USER artifactory WITH PASSWORD 'mypasswd';
CREATE DATABASE artifactory OWNER artifactory;

# Close PostgreSQL session
\q

# Restart Artifactory service
sudo systemctl start artifactory.service
```