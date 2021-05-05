## Description
HON is a web application to implement human reading experiments in medical imaging enabling common methodologies such as VGA, m-AFC (m=2,4,6,8), ROC, LROC and FROC experiments.
## Installation with docker
> Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications (https://docs.docker.com/get-started/overview/).

Docker presents the easiest way to run your own version of HON locally. 
1. Please download and install the appropriate docker version for your OS here https://docs.docker.com/get-docker/
2. Git clone or download and unzip this git repo
Once you successfully installed and started docker there are two options two build and start the application
### Build and start the application using a GUI e.g. DockStation
3. Download, install and then open Dockstation https://dockstation.io/
4. Add a new project with Dockstation
- define a name for the project and set the path to the downloaded code
- start the application 
5. open your browser, enter 0.0.0.0:8000 in the address field to access the application
<p align="center">
or
</p>
### Build and start the application using the docker CLI  
3. open the terminal (MacOS, Linux)/ command line (windows)
- using the cd command navigate to the path with the application code 
4. build the application by typing 
```
docker compose-build to 
```
5. start the app with 
```
docker compose-up
```

## Install (developer)
to do

## Hosting Tutorial
to do

