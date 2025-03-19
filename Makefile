dir=${CURDIR}
namespace=updevision
registry={registry}
project=test
interactive:=$(shell [ -t 0 ] && echo 1)
ifneq ($(interactive),1)
	optionT=-T
endif

uid=$(shell id -u)
gid=$(shell id -g)
c=
p=

dc:
	@docker-compose -f ./docker-compose.yml --env-file=.env $(cmd)

init:
	docker network ls | grep $(namespace)_network > /dev/null || docker network create $(namespace)_network
	@make dc cmd="up -d"
	@make ports

logs:
	@make dc cmd="logs"

deepclean:
	@make dc cmd="down -v"

build:
	@make dc cmd="build"

collect_static:
	@make dc cmd="exec $(namespace)-$(project) python ./manage.py collectstatic --noinput --clear -v 0"

up:
	@make dc cmd="up -d"
	make ports

stop:
	@make dc cmd="stop"

down:
	@make dc cmd="down"

restart:
	@make dc cmd="stop"
	@make dc cmd="up -d"

bash:
	@make dc cmd="exec $(namespace)-$(project) bash"

pg_bash:
	@make dc cmd="exec $(namespace)-$(project)-postgres bash"

shell:
	@make dc cmd="exec $(namespace)-$(project) python ./manage.py shell"

migrations:
	@make dc cmd="exec $(namespace)-$(project) python ./manage.py makemigrations"

migrate:
	@make dc cmd="exec $(namespace)-$(project) python ./manage.py migrate"

ports:
	docker ps --format="table {{.ID}}\t{{.Names}}\t{{.Ports}}" | grep "$(namespace)-$(project)"
