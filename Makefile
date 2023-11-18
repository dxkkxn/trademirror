include .env.test


ENV= .env.test
DOCKER = docker
# arch-linux based check if u have docker-compose
DOCKER_COMPOSE=docker-compose
FIREFOX=firefox
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
	$(DOCKER) rmi $(RESTAPI_IMAGE) $(FRONTEND_IMAGE) $(REDIS_IMAGE)  $(CONSUMER_FTD_IMAGE) $(REDIS_COMMANDER_IMAGE) $(ZOOKEPER_IMAGE) $(KAFKA_IMAGE) $(PRODUCER_FTD_IMAGE) -f 
mockdata:
	$(DOCKER) exec $(RESTAPI_CONTAINER) python3 /app/helper/mockdata.py 
remove-database:
	$(DOCKER) exec -it $(REDIS_CONTAINER) redis-cli FLUSHDB 
remove-all:
	$(DOCKER) exec -it $(REDIS_CONTAINER) redis-cli FLUSHALL

# Use this command only if have firefox installed
see-database:
	$(FIREFOX) http://localhost:8081/ &
	




