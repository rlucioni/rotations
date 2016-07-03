build:
	docker-compose build

serve:
	docker-compose up web

shell:
	docker-compose run shell

requirements:
	pip install -r requirements.txt

quality:
	flake8 .

clean:
	# Delete exited containers.
	docker rm -v $(shell docker ps -a -q -f status=exited)
	# Delete dangling images.
	docker rmi $(shell docker images -f "dangling=true" -q)

deploy: build
	heroku container:release

migrate:
	python manage.py migrate
