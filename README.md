# Group-9-Project
Code for group 9, also contains the original camel system. 

# Getting camel to work
### Installing django on Python 3
```sh
$ pip install django
```
### Install extra python modules for camel to work
```sh
$ pip install django-mptt
$ pip install django-debug-toolbar
$ pip install django-extensions
```
### Set up datebase & create admin
```sh
$ python3 manage.py migrate
$ python3 manage.py createsuperusers
```
### To run the camal system on django
```sh
$ python3 manage.py runserver
```