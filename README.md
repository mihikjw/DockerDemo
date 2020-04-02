# DockerDemo

This repository is designed for beginners/newcomers to Docker to learn the software from the ground up, providing documentation, examples & links to other useful resources. I've attempted to link this document to as much source-code as possible so if you really want to get into how Docker/Containers work you can browse the source at your leisure.

Some basic Linux Kernel & CLI knowledge is required to make best use of this document however I've tried to explain these features in laymans terms for those not so familiar with Linux OS.

## What Are Docker Containers?
### Low-Level Functionality
You may have heard containers referred to as 'lightweight virtual machines' - this is not true, although the output result looks similar. The fundamental concept is simply process isolation, this functionality is provided through the following [Linux Kernel](https://github.com/torvalds/linux) features:
- [cgroups](https://github.com/torvalds/linux/tree/master/kernel/cgroup): control groups, allows you to limit & account for resource usage (CPU, memory, disk I/O, network etc) of a collection of processes. Initial Kernel release 2.6.24, 2008. Since this time further features have been added, including kernfs (cgroup virtual file systems - Kernel 3.14, 2014), firewalling and unified hierarchy
- namespacing: allows the reuse of names in different contexts, there are 6 namespaces:
    - PID namespace
    - Mount namespace
    - UTS namespace
    - Network namespace
    - IPC namespace
    - User namespace

This is a fundamental difference from a Virtual Machine, which must distribute their own Kernel. Containers still make use of the host operating system and have a PID, unlike a VM.

This process isolation was originally achieved using [LXC](https://github.com/lxc/lxc) (Linux Containers), an abstraction over low-level cgroups and namespaces, released in 2008. Docker was originally an abstraction over LXCs, however since Docker 0.9 it has included its own component, [libcontainer](https://github.com/opencontainers/runc/tree/master/libcontainer), to directly use the Kernel virtualization facilities in addition to abstracted interfaces such as LXC, [libvirt](https://github.com/libvirt/libvirt) and [systemd-nspawn](https://github.com/systemd/systemd/tree/master/src/nspawn). As these are all Linux-specific features, other implementations (such as OSX or Windows) will run a Linux Virtual Machine in the background to actually host the containers. 

#### How To Write A Container From Scratch
Embedded below is a great presentation from Liz Rice, explaining the process of coding-up a container from scratch in Go. For those that would prefer a quick scim-over what a container looks like in code (C), links below:
- [child process in new namespace](https://github.com/w-vi/diyC/blob/master/src/nsexec.c)
- [container runtime implementation](https://github.com/w-vi/diyC/blob/master/src/diyc.c)

[![Building A Container From Scratch](https://res.cloudinary.com/marcomontalbano/image/upload/v1585823559/video_to_markdown/images/youtube--Utf-A4rODH8-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=Utf-A4rODH8 "Building A Container From Scratch")

### What Is Docker?
Docker's core component is the [Docker Engine](https://github.com/docker/engine) (this is itself a fork of [Moby](https://github.com/moby/moby)), which is exposed over an [HTTP API](https://github.com/docker/engine/tree/master/docs/api) on the host machine. This is accessable over a UNIX Socket (/var/run/docker.sock) on localhost, but it can also be exposed over TCP - by default this is disabled for security purposes. This socket is referred to as the 'Docker Socket'. The Docker Engine is responsible for spawning, orchestrating and monitoring the containers, as well as responding to client requests over the API. 

You would not typically communicate directly with the Docker Socket however, but use the [Docker CLI](https://github.com/docker/cli). The Docker CLI provides a user-interface for the Docker Socket and makes API requests much easier to manage. We will be using the Docker CLI throughout this documentation and to make use of Docker containers you should be very familiar with this tool.

### Why Use Docker?
- "Works On My PC", "Ship Your PC To The Customer Then" - effectively Docker is doing the latter! Due to the environment isolation provided by containers, this allows application developers to control the dependencies and environments of their applications, and keep this consistent throughout the entire development/test/deployment pipeline. Everything from networks, files, environment variables, exposed ports, and more are the responsibility of the developer. All of this configuration is bundled together into a Docker Image (containers are created from images, more on this later) and not shared with the Host OS or other Docker Images
    - Example: You have a 5-microservice application where each service is written in a different language, requires different packages, config etc. All that is required on the Host OS is a docker install, you can simply add these Docker Images and run them. All config, language runtimes, libraries, OS packages etc are bundled in the Docker Image.
- Bug/Issue circuit breaker - processes isolation stops issues in container A affecting container B or the Host OS in any way. You can even check out CLI commands/tools you are not sure about by starting a container simply with a shell, preventing any damage being done to your Host OS
- Centralised Docker Image Repository: Docker (the company) provides a centralised, open image repository - this allows you to take virtually any software, clone to your local PC, then run it. No configuration required. A particularly useful example is a database - you're putting together a schema and want to test it, if you get it wrong you can just restart the container instead of clearing configs and files then starting again. The development process is significantly faster.
    - Inspect: Docker allows you to 'inspect' a downloaded container, as well as get access to a bash terminal for a running container. You can use this to check the configuration of a 3rd party tool and either configure your own, or perform reverse-engineering. More on this functionality later
- Monitor/Orchestrate applications: by default Docker Containers take over stdin, stdout, stderr when started. However you can easily add a flag to send these to the background and free your terminal, then easily use a single interface, the Docker CLI, to monitor and control running applications

## Installation, Docker CLI & Docker-Compose
### Docker CLI
The Docker CLI is the primary way of interacting with a singular Docker Container. I won't bore you by copying and pasting the [official documentation](https://docs.docker.com/engine/reference/commandline/cli/), but instead give a short list of some of the most useful commands you will need. Please read the official Docker CLI documentation.
- [Linux](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
- [OSX](https://docs.docker.com/docker-for-mac/install/)
- [Windows](https://docs.docker.com/docker-for-windows/install/) - HyperV required (Win10 Pro)

### Docker-Compose
[Docker-Compose](https://github.com/docker/compose) is a Python3 program produced by docker, for orchestrating multiple containers and defining your container in YAML rather than at the CLI. Fundamentally this is still communicating with the Docker Socket in the same way as the CLI but is a much more user-friendly way of configuring containers are runtime. We will go into more detail in this document on how Docker-Compose works as this is how you should be running containers rather than through the CLI, this document is designed to supplement, not replace, the [official documentation](https://docs.docker.com/compose/) and [official reference](https://docs.docker.com/compose/compose-file/)
- [Install](https://docs.docker.com/compose/install/)

## Running Your First Docker Container
There is no better way of explaining the Docker workflow like running your first container! Docker distribute a 'hello-world' container for just this purpose.
1. Get the Image: ```docker pull hello-world```. Containers are creating from Images. You can have multiple instances of a Container created and running from a single Image. The Image contains all the configuration, files and dependencies that are then loaded into a Container to be run. Once you execute this command, you will see a download taking place, defaulting to the latest version of the Image. This is downloaded from the [Central Docker Hub Repository](https://hub.docker.com/_/hello-world).
2. Inspect the Image: ```docker inspect hello-world```. This command allows you to view the makeup of an Image. You can view environment variables, the command run inside the Container, SHA256 hash for the Image, Architecture (e.g. hello-world is amd64 not x86-64) and other configuration. It is useful to know some of these details before pulling and running an Image.
3. Run a Container from the Image: ```docker run hello-world```: This command creates a Container from the downloaded Image, and runs the 'cmd' command you saw whilst running the Inspect command. You should get a simple splash-screen saying 'hello world' and explaining what took place to create the container.
4. View Container: ```docker ps -a```. The hello-world Container just prints some text and then exits. However we can see some of the details that were assigned to it after it closed by running this command. We can see that each container is assigned a unique ID, what image it was created from, the command used to run the application inside the container, when the container was created, when the container exited, any port mappings that were assigned, and the name of the container (if not supplied this is randomly generated).
5. View Output: ```docker logs {container_name}```. Docker will capture and save STDOUT for any Container run. You can then access this from any container (running or stopped) using the Docker Logs command. You can add a '-t' arg to also get the timestamps of the log output.
6. Remove The Container: ```docker rm {container_name}```. Once the container has finished, you should remove the record of it from the system as not to clutter your ```docker ps -a``` output report. Unfortunatly this command does not support wilcards and if you need to remove multiple Containers from the list you have to do each one-by-one or write a shell script to do it for you.

You should now see that an Image is pulled from the central repository, a Container is created from an Image, and how to monitor your Container.

## Building Your First Image
Images can be pulled from the central repository, but you can also build them yourself. These are declared in a Dockerfile, which is essentially a glorified shell script with a format, for building Docker Images. We will use Docker-Compose to control this process as it provides more visibility rather than a large CLI command.
This example demonstrates building an Image to run a 'hello world' Python3 script, using a basic Image based on Ubuntu Linux OS.

**NOTE:** Each step in a Dockerfile is stored as part of the image, which allows for caching build steps if multiple containers have the same first few lines for example, and so end users can see what you've done to build the container. HOWEVER, as a result this means large Dockerfiles means large output Images. To minimise your output image sizes, chain as many commands into one line as you can.

1. ```mkdir test_image && cd test_image && echo "print('Hello World')" >> main.py && touch Dockerfile && touch docker-compose.yml```
2. Take the below and save into ```Dockerfile```:
``` Dockerfile
FROM ubuntu
RUN apt update -y && apt install -y python3
WORKDIR /code
COPY ./main.py .
CMD ["python3", "main.py"]
```
    - ```FROM ubuntu```: The 'FROM' clause dictates the base Image to build your Image from. If in doubt, Ubuntu is a good start or Alpine for an ultra-small Linux distro.
    - ```RUN apt update -y && apt install -y python3```: The 'RUN' command allows you to run any shell command inside the image, any changes or output files will be stored in the image. The example command is to install the Python3 interpreter as a dependency.
    - ```WORKDIR /code```: So far all commands have been running in directory '/'. The 'WORKDIR' command creates and changes your working directory to the specified dir. General best practice is to create your own at the root, as seen in this Dockerfile example.
    - ```COPY ./main.py .```: The 'COPY' command, copies a file from the Host to the Image. The first arg is the source, the latter the target. You must give the full path relative to the location of the Dockerfile. If the target filename is the same as the source, you can just put '.'. The target file will be put into the directory relative to the set 'WORKDIR' path.
    - ```CMD ["python3", "main.py"]```: The 'CMD' command, declares the command to be run when the Container is executed. Each arg is seperated in an array, this is reasonably self-explanatory.
3. Take the below and save into ```docker-compose.yml```:
``` YAML
version: '3'
services:
  test:
    container_name: test
    build:
      context: .
      dockerfile: Dockerfile
    image: testing:test
```
    - ```version: '3'```: The defines the version of docker-compose - unless a new version is released, 3 is the default
    - ```services:``` Defines the services
        - ```test:``` This is the name of the image in the YAML file - must be unique inside the YAML file
            - ```container_name:``` This is the name of the container once created, additional replicas will be appended with '_X' where X is a number
            - ```build:``` This defines options for building the container
                - ```context: .``` This defines the directory to search for a Dockerfile
                - ```dockerfile: Dockerfile``` This defines the name of the Dockerfile to use during the build, default is 'Dockerfile' but its in this example to be specific
            - ```image:``` This defines the name of the image to be saved, in the format {repository}:{image_name}
4. Start the Build & Run workflow with the command ```docker-compose up``` from inside the 'test_image' directory. You'll see the Ubuntu base image being pulled, then the process of building your image, then running the container and exiting. 
5. To cleanup all the created containers in the docker-compose.yml file, run ```docker-compose down```.

This process demonstrates building a simple Docker Image and how a simple docker-compose file works. For more complex features you can use the [docker-compose reference](https://docs.docker.com/compose/compose-file/) and [dockerfile reference](https://docs.docker.com/engine/reference/builder/).

## Useful Docker CLI/Compose Cheat Sheet
- Docker CLI
    - Bash Shell in a running container: ```docker exec -ti {container_name} /bin/bash```
    - View all containers, including shut-down errors: ```docker ps -a```
    - List Images: ```docker image list```
    - Delete Image: ```docker image rm {image_id}```
    - Inspect Image: ```docker inspect {image_id}```
    - Stop Container: ```docker stop {container_name}```
    - Kill Container: ```docker kill {container_name}```
    - View Processes In Container: ```docker top {container_name}```
- Docker-Compose
    - Run a docker-compose.yml file with attached shell: ```docker-compose up```
        - exit attached shell, keep processes running: ctrl + z
        - exit attached shell, perform 'docker stop' on all containers: ctrl + c
    - Run a docker-compose.yml file with a detached shell: ```docker-compose up -d```
    - Build/Pull a docker-compose.yml file's images: ```docker-compose build```

## Example Application
Building simple Images and running simple Containers is all well and good, but what would a real-world application look like? Provided in this repository is an [example web application](./webapp), explained below.

**WIP**