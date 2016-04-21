run_develop:
	docker-compose up

run_tests:
	docker-compose run -e FLASK_CONFIG=testing lochat-base python3.4 manage.py test
