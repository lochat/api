# lochat API

Requirements
-------

Install docker-compose:
		
	$ pip install docker-compose

configure
---------

	$ git clone https://github.com/lochat/api
	$ cd api
    $ docker build .
    $ mv set_envs.env.template set_envs.env
    $ nano set_envs.env

Usage
-------

Executando servidor de desenvolvimento:
		
	$ docker-compose up
		
Executando testes:
	
	$ docker-compose run -e FLASK_CONFIG=testing lochat-base python3.4 manage.py test

