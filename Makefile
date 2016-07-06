build:
	docker-compose build

up:
	docker-compose up web

shell:
	docker-compose run web bash

test:
	docker-compose run web python -m pytest

quality:
	docker-compose run web flake8 .

deploy: build
	heroku container:release

start:
	docker-machine start default

connect: start
	eval $(shell docker-machine env)

stop:
	docker-machine stop default

clean:
	# Delete exited containers.
	docker rm -v $(shell docker ps -a -q -f status=exited)
	# Delete dangling images.
	docker rmi $(shell docker images -f "dangling=true" -q)
