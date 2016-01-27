# Group-9-Project
CAMEL E - Learning System developed Group 9

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
 pip install Pillow
```

**Note:** For OS X users running this with Python3, Pillow requires an additional package to be installed. To aquire this package via brew:
```sh
 $ brew install libtiff libjpeg webp little-cms2
```
** Don't have brew installed: **[Get Brew from here!](http://brew.sh)
### Set up datebase & create admin
```sh
 py manage.py migrate
 py manage.py createsuperusers
```
### To run the camal system on django
```sh
 py manage.py runserver
```