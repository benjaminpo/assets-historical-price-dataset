.PHONY: clean
clean:
	make down
	docker container prune -f
	docker system prune -af
	rm -rf ./volumes/db

.PHONY: down
down:
	docker-compose down --volumes

.PHONY: freeze
freeze:
	pip freeze > requirements.txt

.PHONY: rebuild
rebuild:
	make clean
	docker-compose build
	docker-compose up -d
	make up

.PHONY: up
up:
	docker system prune -f
	docker-compose build
	docker-compose -f docker-compose.yml up --build

.PHONY: update
update:
	git add .
	git commit -m "update"
	git push -f

.PHONY: updatedata
updatedata:
	make up
	git add .
	git commit -m "update datasets"
	git push -f

.PHONY: venv
venv:
	virtualenv venv
