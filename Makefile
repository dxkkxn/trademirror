include .env.test


ENV= .env.test
DOCKER = docker
# arch-linux based check if u have docker-compose
DOCKER_COMPOSE=docker-compose
# other os check if u have docker compose
# uncomment if u have 
#DOCKER_COMPOSE=docker compose

build:
	$(DOCKER_COMPOSE) --env-file $(ENV) build 

start:
	$(DOCKER_COMPOSE) --env-file $(ENV) up -d
start-debug:
	$(DOCKER_COMPOSE) --env-file $(ENV) up
stop:
	$(DOCKER_COMPOSE) --env-file $(ENV) stop 
bash-backend:
	$(DOCKER) exec -it $(RESTAPI_CONTAINER) /bin/bash
clean:
	$(DOCKER_COMPOSE) --env-file $(ENV) down
	$(DOCKER) rmi $(RESTAPI_IMAGE) $(FRONTEND_IMAGE) $(REDIS_IMAGE) -f 


