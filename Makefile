include .env.test


ENV= .env.test
DOCKER = docker
DOCKER_COMPOSE=docker-compose

build:
	$(DOCKER_COMPOSE) --env-file $(ENV) build 

start:
	$(DOCKER_COMPOSE) --env-file $(ENV) up -d
stop:
	$(DOCKER_COMPOSE) --env-file $(ENV) stop 
bash-backend:
	$(DOCKER) exec -it $(RESTAPI_CONTAINER) /bin/bash
clean:
	$(DOCKER_COMPOSE) --env-file $(ENV) down
	$(DOCKER) rmi $(RESTAPI_IMAGE) $(FRONTEND_IMAGE) $(REDIS_IMAGE) -f 


