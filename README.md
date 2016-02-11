# lochat API

Requirements
-------

Install docker-compose:
		
	$ pip install docker-compose

Configure
---------

	$ git clone https://github.com/lochat/api
	$ cd api
    $ docker build -t lochat-base .
    $ mv set_envs.env.template set_envs.env

Usage
-------

Executing development server:	
	
    $ docker-compose up
		
Executing tests:
	
	$ docker-compose run -e FLASK_CONFIG=testing lochat-base python3.4 manage.py test

