# lochat API

configure
---------

	$ git clone https://github.com/lochat/api
	$ cd api
    $ docker build .

Usage
-------

Executando servidor de desenvolvimento:
		
	$ docker-compose up
		
Executando testes:
	
	$ docker-compose run lochat-base python3.4 manage.py test

