## Description
HON is a web application to implement human reading experiments in medical imaging enabling common methodologies such as VGA, m-AFC (m=2,4,6,8), ROC, LROC and FROC experiments. You can find a demo version of the application on <a href="https://hondemo.pythonanywhere.com/" target="_blank" rel="noopener noreferrer"> Pythonanywhere </a> or <a href="http://hon-demo.herokuapp.com/studies/overview" target="_blank" rel="noopener noreferrer"> Heroku </a>.

The software was designed as a web application to avoid the need for installation on diagnostic workstations and enable platform-independence as well as multi-center studies. The code is open-source (MIT licence). The application backend was built using mainly Flask (v2.0.2) and Flask-SQLAlchemy (v2.5.1). To simplify access HON can be installed using docker (for development flasks development server is used, while gunicorn and nginx are used during production). For a full list of dependencies see the requirments.txt. The frontend of the application was developed using bootstrap (v4.1) and jQuery (v3.4.1) in addition to plain HTML, CSS, and JavaScript. The JavaScript library cornerstone (v2.2.7) and cornerstone-tools (v5.1) were used to implement dicom-viewer capabilities, such as the display of files (DICOM ,JPEG, PNG) as single images or scrollable stacks, options for modifying display settings and features to collect annotation data. 

## Upcoming changes
- update frontend using vuejs (about 40% finished, update will be available in August), new features will include
  - more freedom regarding images displayed simultaneously and image layout
  - simplified working with stacks 
  - improved performance, stability and maintainability
- update backend (flask) tests
- simplify deployment
  - add traefik to enable HTTPS 

## Setup using docker
> Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications (https://docs.docker.com/get-started/overview/).

Docker presents the easiest way to run your own version of HON. 
1. Please download and install the appropriate docker version for your OS <a href="https://docs.docker.com/get-docker" target="_blank" rel="noopener noreferrer">here</a>.
2. Git clone or download and unzip this git repo.

Once you successfully installed and started docker there are two options two build and start the application.
### Docker setup option 1: Build and start the application using DockStation
3. Download, install and then open <a href="https://dockstation.io/" target="_blank" rel="noopener noreferrer">Dockstation</a>.
4. Open dockstation. An account is not necessary, you can use the application with a guest account.
5. Add a new project.
- define a name for the project and set the path to the downloaded code

6. Build and start the application.
- you can start HON in development or production mode 
- do not use the development mode when deploying HON, it is intended for use only during local development

6. 1. development mode
- build and start the application via the appropriate buttons in dockstation

6. 2. production mode
- set the secret key as descibed under "Docker setup option 2" 4.2
- press the build button
- switch to the settings menu of the project and select docker-compose.prod.yml as default compose file
- press the build button again
- start the application

7. if you start HON for the first time switch to the containers menu 
- select HON and press the exec button, this should open a terminal
- in this terminal enter 
```
flask init-app
```
- this command initializes/resets the databases and creates 3 default users

8. Access the application
- press the web button in dockstation or open your browser and enter the ip address/domain name of your machine (e.g. 127.0.0.1 if you are using a local setup) 
- the default user logins are: 

| username  | password | role |
| ------------- | ------------- | ------------- |
| user  | user  | study-participant |
| sadmin  | sadmin | study-admin |
| uadmin  | uadmin | user-admin |

### Docker setup option 2: Build and start the application using the docker CLI  
3. open the terminal (MacOS, Linux)/ command line (windows)
- using the cd command navigate to the path with the application code
```
cd /"path_to_app_code"
```
4. Build the application by typing:
- you can start HON in development or production mode 
- do not use the development mode when deploying HON, it is intended for use only during local development

4. 1. development mode
```
docker-compose build
```
4. 2. production mode
- before deploying the application ensure to set a secret key in the config.py file
- the secret key is needed to keep the client-side sessions secure
- open the config.py file using a text editor
- under class ProductionConfig set the secret key
- a guide to generate a good secret key can be found <a href="https://flask.palletsprojects.com/en/1.0.x/quickstart/#sessions" target="_blank" rel="noopener noreferrer">here</a>
- the production build uses the development build as a basis
- therefore after setting the secret-key first build HON in development mode 
```
docker-compose build
```
- follwed by running
```
docker-compose -f docker-compose.prod.yml build 
```
5. Start the app

- development mode 
```
docker-compose up -d
```
- production mode
```
docker-compose -f docker-compose.prod.yml up -d
```
6. If you start HON for the first time enter 
- development mode 
```
docker exec -it HON_dev flask init-app
```
- prodcution mode 
```
docker exec -it HON_prod flask init-app
```
- this command initializes/resets the databases and creates 3 default users

7. Access the application 
- open your browser and enter the ip address/domain name of your machine (e.g. 127.0.0.1 if you are using a local setup) 
- the default user logins are: 

| username  | password | role |
| ------------- | ------------- | ------------- |
| user  | user  | study-participant |
| sadmin  | sadmin | study-admin |
| uadmin  | uadmin | user-admin |


## Setup without docker
1. Git clone or download and unzip this git repo.
2. It is recommended to create a virtual environment e.g. using <a href="https://docs.conda.io/projects/conda/en/latest/index.html" target="_blank" rel="noopener noreferrer"> conda </a> or <a href="https://docs.python.org/3/tutorial/venv.html" target="_blank" rel="noopener noreferrer"> python venv </a>.
3. Activate the virtual environment.
4. Install the python requirments by running the following command inside the repo
```
pip install -r requirments.txt
```
5. Run get_js_dep.sh or download the files listed within this script into "app/static/dependencies/" manually.
6. Set the flask environmental variables
```
export FLASK_APP=app
export FLASK_ENV=development
```
7. If you start HON for the first time enter 
- adjust the file config.py:
- set IMAGE_PATH to "/PATH TO REPO/instance/images" 
- set SQLALCHEMY_DATABASE_URI "/PATH TO REPO/instance/sqlite.db"
```
flask init-app 
```
8. Start HON
```
flask run
```
9. Access the application 
- open your browser and enter the ip address/domain name of your machine (e.g. 127.0.0.1 if you are using a local setup) 
- the default user logins are: 

| username  | password | role |
| ------------- | ------------- | ------------- |
| user  | user  | study-participant |
| sadmin  | sadmin | study-admin |
| uadmin  | uadmin | user-admin |

## How to deploy the application using an VPS (e.g. contabo) and docker
1. Create an account at <a target="_blank" rel="noopener noreferrer" href="https://www.contabo.com/"> contabo </a> or another VPS server provider
- if you use contabo use the Ubuntu 22.04 image
- the smallest server with 4 vCPU, 8 GB RAM, 32 TB Traffic and 50 GB NVM should be enough
2. After the account has been set up connect to it via ssh
- in case of contabo the command will look like this using a command line interface, for more information see the <a target="_blank" rel="noopener noreferrer" href="https://contabo.com/blog/establishing-connection-server-ssh/"> contabo tutorial for ssh connection</a>
```
ssh root@<ip-adress>
```
3. Install docker engine on your server
- after connecting via ssh install the docker engine following the instructions in the "Install using the repository" section of the <a href="https://docs.docker.com/engine/install/ubuntu/" target="_blank" rel="noopener noreferrer"> docker documentation </a>
4. Git Clone the repository
- clone the application code to your VPS with
```
git clone https://github.com/genskeu/HON
```
5. Follow the steps described under docker setup option 2: "Build and start the application using the docker CLI"


## How to deploy using pythonanywhere
1. Register at <a target="_blank" rel="noopener noreferrer" href="https://www.pythonanywhere.com/"> pythonanywhere </a>
- the username you choose will later be part of the url used to access the application
  - in the following tutorial replace \<username\> with the username you choose here 
- a free account does not offer enough space and cpu time to run HON conveniently
- in the past we have been using a custom account before switching to self-hosting 
- for the custom account we used: 
  - CPU time per day: 3000 seconds
  - Number of web apps: 1
  - Number of web workers: 3 
  - Number of always-on tasks: 2
  - Disk space: 10 GB
- these settings may differ for you depending on your needs
2. Log into pythonanywhere and open a bash console in a new tab
- create the console using the Consoles section
- using the console clone the repository by running
```
git clone https://github.com/genskeu/HON
```
- next create an virtual environment using the following command 
```
mkvirtualenv myvirtualenv --python=/usr/bin/python3.8
```
- move into the path with the application code and install the python dependencies
```
cd /"path_to_app_code" should be /home/<username>/HON
pip install -r requirements.txt
```
- download javascript dependencies by executing the get_js_dep.sh script
```
chmod +x get_js_dep.sh
./get_js_dep.sh
```
- don't close the console yet, we will come back to it later
3. adjust the config file (ProductionConfig)
- use the Files section to navigate to and open the config file within the HON folder (path should be /home/<username>/HON/config)
- as described under "Docker setup option 2: Build and start the application using the docker CLI" set a secret key
- set IMAGE_PATH to "/home/<username>/HON/instance/images_prod"
- set SQLALCHEMY_DATABASE_URI "sqlite://////home/<username>/HON/instance/prod.db"
- afterwards switch back to the tab with the open bash console and run
```
export FLASK_APP=app
export FLASK_ENV=production
flask init-app 
```  
- this concludes the bash part of the setup
4. Pythonanywhere configuration
- in the Web section of you pythonanywhere account press "add a new web app" and select manual config
- on the same side under "Code" adjust the "Source Code" path, it should be /home/<username>/HON
- addjust the path to your Virtual environment, it should be /home/<username>/.virtualenvs/myvirtualenv/
- enable HTTPS
- (optionally) enable password protection for extra layer of security

5. adjust WSGI configuration file
- open by pressing the link /var/www/<username>_pythonanywhere_com_wsgi.py
- add the end of the file in the FLASK section add
```
import sys
path = '/home/<username>/HON'
if path not in sys.path:
    sys.path.append(path)

from app import create_app
application = create_app()
```

6. access web app
- press the reload <username>.pythonanywhere.com button
- application should be available under <username>.pythonanywhere.com

## How to deploy the application using Heroku
to do
