# Group-9-Project
CAMEL E - Learning System developed Group 9
___

# Getting Started
To create all the tables for Django:
```sh
 py manage.py syncdb
 py manage.py makemigrations
 py manage.py migrate
```
In order to use the latex parser:
```sh
 py manage.py parselatexfile file.tex
```
**Note:** Can eitehr use main.tex or tex/MA0000/main.tex to add files to CAMEL. The latex file used, must be syntactically correct before using the parser. So use a latex compiler before adding to CAMEL. 

![CAMEL][logo]
[logo]:https://github.com/Ryan95Z/Group-9-Project/blob/master/Archive/CAMEL2/media/camel_logo_reversed.png