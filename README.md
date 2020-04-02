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
Embedded below is a great presentation from Liz Rice, explaining the process of coding-up a container from scratch in Go. For those that would prefer a quick scim-over what a container looks like in code, I have provided an [example in C](./containers/main.c) making use of the POSIX API.

[![Building A Container From Scratch](https://res.cloudinary.com/marcomontalbano/image/upload/v1585823559/video_to_markdown/images/youtube--Utf-A4rODH8-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=Utf-A4rODH8 "Building A Container From Scratch")

### What Is Docker?
Docker's core component is the [Docker Engine](https://github.com/docker/engine) (this is itself a fork of [Moby](https://github.com/moby/moby)), which is exposed over an [HTTP API](https://github.com/docker/engine/tree/master/docs/api) on the host machine. This is accessable over a UNIX Socket (/var/run/docker.sock) on localhost, but it can also be exposed over TCP - by default this is disabled for security purposes. This socket is referred to as the 'Docker Socket'. The Docker Engine is responsible for spawning, orchestrating and monitoring the containers, as well as responding to client requests over the API. 

You would not typically communicate directly with the Docker Socket however, but use the [Docker CLI](https://github.com/docker/cli). The Docker CLI provides a user-interface for the Docker Socket and makes API requests much easier to manage. We will be using the Docker CLI throughout this documentation and to make use of Docker containers you should be very familiar with this tool.