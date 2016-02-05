# lochat API

configure
---------

	$ git clone https://github.com/lochat/api
	$ docker build -t lochat-base
	$ vim set_envs.env

Usage
-------

.. Executando servidor de desenvolvimento:
		$ docker-compose up
.. Executando testes:
		$ docker-compose run lochat-base python3.4 manage.py test

