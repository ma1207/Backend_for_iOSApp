# Backend_for_iOSApp
### This is the web service for the internship iOS App in https://github.com/ma1207/Frontend_for_iOSApp.
# Prerequisite
### Ubuntu 22.04 server
# How to Install and Run 
### Install Docker and create an account.
## On the build machine...
### Go to the project's directory
### Create a Docker image using ```docker image build [path]```
### Push Docker image using ```docker push [filename]:tag```
## On the server machine...
### Create a file called docker-compose.yml with the following code:
```
version: "3"

services:
  demo:
    image: [filename]
    network_mode: host
```
    
### Pull Docker image using ```docker pull [filename]:tag```
### Build and start a container using ```docker compose up [filename]:tag```
