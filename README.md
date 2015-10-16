# Group-9-Project
Code for group 9, also contains the original camel system. 

# Getting camel to work
### Installing django on Python 3 for Windows:
```sh
 pip install django
```
### Install extra python modules for camel to work
```sh
 pip install django-mptt
 pip install django-debug-toolbar
 pip install django-extensions
```
### Set up datebase & create admin
```sh
 py manage.py migrate
 py manage.py createsuperusers
```
### To run the camal system on django
```sh
 py manage.py runserver
```