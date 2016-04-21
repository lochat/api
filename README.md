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
	
    $ make run_develop
		
Executing tests:
	
	$ make run_tests

