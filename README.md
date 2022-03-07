## Description
HON is a web application to implement human reading experiments in medical imaging enabling common methodologies such as VGA, m-AFC (m=2,4,6,8), ROC, LROC and FROC experiments. You can find a demo version of the application on <a href="https://hondemo.pythonanywhere.com/" target="_blank" rel="noopener noreferrer"> Pythonanywhere </a> or <a href="http://hon-demo.herokuapp.com/studies/overview" target="_blank" rel="noopener noreferrer"> Heroku </a>.

The software was designed as a web application to avoid the need for installation on diagnostic workstations and enable platform-independence as well as multi-center studies. The code is open-source (MIT licence). The application backend was built using mainly Flask (v2.0.2) and Flask-SQLAlchemy (v2.5.1). To simplify access HON can be installed using docker (for development flasks development server is used, while gunicorn and nginx are used during production). For a full list of dependencies see the requirments.txt. The frontend of the application was developed using bootstrap (v4.1) and jQuery (v3.4.1) in addition to plain HTML, CSS, and JavaScript. The JavaScript library cornerstone (v2.2.7) and cornerstone-tools (v5.1) were used to implement dicom-viewer capabilities, such as the display of files (DICOM ,JPEG, PNG) as single images or scrollable stacks, options for modifying display settings and features to collect annotation data. 

## Upcoming changes
- update frontend using vuejs
- update backend (flask) tests


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

6. build and start the application
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

6. if you start HON for the first time switch to the containers menu 
- select HON and press the exec button, this should open a terminal
- in this terminal enter 
```
flask init-app
```
- this command initializes/resets the databases and creates 3 default users

7. to access the application press the web button in dockstation or open your browser and enter the  ip address/domain name of your machine (e.g. 127.0.0.1 if you are using a local setup) 
- the default user logins are: 

| username  | password | role |
| ------------- | ------------- | ------------- |
| user  | user  | study-participant |
| sadmin  | sadmin | study-admin |
| uadmin  | uadmin | user-admin |

### Docker setup option 2: Build and start the application using the docker CLI  
3. open the terminal (MacOS, Linux)/ command line (windows)
- using the cd command navigate to the path with the application code e.g.
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
6. if you start HON for the first time enter 
- development mode 
```
docker exec -it HON_dev flask init-app
```
- prodcution mode 
```
docker exec -it HON_prod flask init-app
```
- this command initializes/resets the databases and creates 3 default users

7. to access the application open your browser and enter the ip address/domain name of your machine (e.g. 127.0.0.1 if you are using a local setup) 
- the default user logins are: 

| username  | password | role |
| ------------- | ------------- | ------------- |
| user  | user  | study-participant |
| sadmin  | sadmin | study-admin |
| uadmin  | uadmin | user-admin |


## Setup without docker
1. Git clone or download and unzip this git repo.
2. It is recommended to create a virtual environment e.g. using conda or python-venv.
3. Activate the virtual environment.
4. Install the python requirments by running the following command inside the repo
```
pip install -r requirments.txt
```
4. Set the flask environmental variables
```
export FLASK_APP=app
export FLASK_ENV=development
```
5. If you start HON for the first time enter 
```
flask init-app 
```
6. Start HON
```
flask run
```
7. to access the application open your browser and enter the ip address/domain name of your machine (e.g. 127.0.0.1 if you are using a local setup) 
- the default user logins are: 

| username  | password | role |
| ------------- | ------------- | ------------- |
| user  | user  | study-participant |
| sadmin  | sadmin | study-admin |
| uadmin  | uadmin | user-admin |

## How to deploy the application on Pythonanywhere
to do

## How to deploy the application on Heroku
to do
