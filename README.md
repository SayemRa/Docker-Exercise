
Synopsis
The purpose of this exercise is to learn (or recap) how to create a system of two interworking 
services that are started up and stopped together. This requires creation of your own Dockerfiles
and docker-compose.yaml, and also creation the simple applications. The applications can be 
implemented in any programming language (shell script and HTML not allowed), but different 
programming language must be used for the two applications. You also need to play with some 
operating system concepts.

Learning goals
• Recap your hands on with Docker and Docker Compose. This is assumed to be known from 
earlier courses and will be needed in the next steps of the course.
• Understand the relation of containers to the operating system and networking.
• Ensure hands on with Linux.
• See the value of virtualization for application development.

Task definition
In this exercise we will build a simple system composed of two small services (Service1 and
Service2) implemented in different programming languages. The services are small programs 
running in separate containers. Both of these applications collect information from the container:
- IP address of the container
- Running processes (e.g. output of “ps -ax” on Ubuntu)
- Available disk-space in the root file systems of the container (e.g. command “df”)
- Time since last boot
The composition of two containers (services) works as a single service, so that one service works 
as an HTTP-server (waiting in port 8199) for external clients. Only one Service1 can be accessed 
from outside, so it needs to ask information from Service2 within the composition.
The response to the HTTP-request should be
Service 
- IP address information
- list of running processes
- available disk space
- time since last boot
Service2
- IP address information
- list of running processes
- available disk space
- time since last boot
Use JSON formatting
Some notes
The IP address may be IP4 or IP6 address – depending on the system. For example the “:ffff:”-
prefix provided by some libraries can be included.
Give the images unique names.
Submitting for grading
After the system is ready the student should return (in the git repository – in branch “exercise1”).
• Content of two Docker and docker-compose.yaml files
• Source codes of the applications.
• Output of “docker container ls” and “docker network ls” (executed when the 
services are up and running.) in a text file “docker-status.txt”
• A short (max 300 words ) text file describing your findings on what containers share with 
the host. Put that to “findings.txt”
• Optional “llm.txt” (see below)
Please do not include extra files in the repository.
These files are returned with some git service. Courses-gitlab repositories can created to coursegitlab if you request one. Any git-repo that the staff can access without extra effort is ok. 
You should prepare your system in a way that the course staff can test the system with the 
following procedure (on Linux):
$ git clone -b exercise1 <the git url you gave>
$ docker-compose up –-build
… wait for 10s
$ curl localhost:8199
$ docker-compose down
