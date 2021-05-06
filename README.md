## Description
HON is a web application to implement human reading experiments in medical imaging enabling common methodologies such as VGA, m-AFC (m=2,4,6,8), ROC, LROC and FROC experiments. You can find a demo version of the application <a href="http://hon-demo.herokuapp.com/studies/overview">here</a>.
## Installation with docker
> Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications (https://docs.docker.com/get-started/overview/).

Docker presents the easiest way to run your own version of HON locally. 
1. Please download and install the appropriate docker version for your OS <a href="https://docs.docker.com/get-docker">here</a>.
2. Git clone or download and unzip this git repo.

Once you successfully installed and started docker there are two options two build and start the application.
### Option 1: Build and start the application using a GUI e.g. DockStation
3. Download, install and then open <a href="https://dockstation.io/">Dockstation</a>.
4. Add a new project with Dockstation.
- define a name for the project and set the path to the downloaded code (step 2)
- start the application 
5. open your browser, enter 0.0.0.0:8000 in the address field to access the application

or

### Option 2: Build and start the application using the docker CLI  
3. open the terminal (MacOS, Linux)/ command line (windows)
- using the cd command navigate to the path with the application code e.g.
```
cd /"path_to_app_code"
```
4. Build the application by typing: 
```
docker-compose build
```
5. Start the app with: 
```
docker-compose up
```
6. open your browser, enter 0.0.0.0:8000 in the address field to access the application

## Install (developer)
to do

## Hosting Tutorial
to do

