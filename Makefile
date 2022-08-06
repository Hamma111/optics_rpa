SHELL=/bin/bash

docker_compose := docker-compose -f
cr_compose     := $(docker_compose) docker-compose.cr.yml
dev_compose    := $(docker_compose) docker-compose.dev.yml
stage_compose  := $(docker_compose) docker-compose.stage.yml
prod_compose   := $(docker_compose) docker-compose.prod.yml
test_compose   := $(docker_compose) docker-compose.test.yml
success        := success

%.all: %.build %.up.d
	@echo $(success)
%.deploy: %.build %.down %.up.d %.migrate %.collectstatic
	@echo $(success)

%.build:
	@$($*_compose) build

%.up.d:
	@$($*_compose) up -d

%.up:
	@$($*_compose) up

%.down:
	@$($*_compose) down --remove-orphans

%.restart:
	@$($*_compose) restart

%.logs:
	@$($*_compose) logs -f

cr:
	@$($@_compose) up --build

fcshell:
	@$(dev_compose) exec frontend /bin/bash

%.dcshell:
	@$($*_compose) exec django /bin/bash

%.dshell:
	@$($*_compose) exec django python manage.py shell

%.ipshell:
	@$($*_compose) exec django python manage.py shell -i ipython

%.attach:
	@docker attach $*

%.migrate:
	@$($*_compose) exec -T django python manage.py makemigrations
	@$($*_compose) exec -T django python manage.py migrate

%.collectstatic:
	@$($*_compose) exec -T django python manage.py collectstatic --no-input

test:
	@$(test_compose) up --build -d
	@$(test_compose) exec -T django python manage.py migrate
	@$(test_compose) exec -T django python manage.py collectstatic --no-input
	@$(test_compose) exec -T django coverage run --source='.' manage.py test --settings=config.settings.test --no-input
	@$(test_compose) exec -T django coverage html
	@$(test_compose) down --remove-orphans

%.psql:
	@$($*_compose) exec postgres psql -U postgres

%.rediscli:
	@$($*_compose) exec redis redis-cli -h redis
