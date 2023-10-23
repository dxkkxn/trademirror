# trade-mirror README

This README provides instructions for using the Makefile and Docker Compose configuration for the trade-mirror project. These tools help simplify common development tasks related to building, starting, stopping, and cleaning up Docker containers.

## Prerequisites

- **Docker**: Ensure you have Docker installed on your system. You can download it from [Docker's official website](https://www.docker.com/get-started).

## Configuration

1. Create a file named `.env.test` in your project directory, containing environment variables used by your containers.

2. Customize the `docker-compose.yml` file to match your project's requirements, including image names, container names, and ports.

## Usage

### 1. Build Docker Containers

To build the Docker containers as defined in the `docker-compose.yml` file, use the following command:

```shell
make build
```

This command builds the containers using environment variables from the .env.test file.

### 2. Start Docker Containers

To start the Docker containers in detached mode, run this command:

```shell
make start
```

This command starts the containers, and they will run in the background.

### 3. Stop Docker Containers

To stop the running Docker containers, use this command:

```shell
make stop
```

This command gracefully stops the containers without removing them.

### 4. Access the Backend Container's Shell

To access a shell inside the backend container, use this command:

```shell
make bash-backend
```

This command opens a shell session inside the container, allowing you to run commands and inspect the environment.

### 5. Clean Up

To remove the Docker containers and associated images, use this command:

```shell
make clean
```

This command stops and removes the containers defined in the docker-compose.yml file and deletes their corresponding images.

### Customization

Feel free to modify the Makefile or Docker Compose configuration files to suit your project's specific needs. You can change container names, ports, and environment variables by editing the .env.test file and the docker-compose.yml file.

### Troubleshooting

If you encounter issues or errors while using the Makefile and Docker Compose, ensure that Docker is properly installed and configured on your system. Check the environment variables in your .env.test file and the configuration in your docker-compose.yml file for any typos or errors.

For more detailed troubleshooting, refer to Docker's documentation and your specific application's documentation.

That's it! You should now be able to use the provided Makefile and Docker Compose configuration to manage your trade-mirror project's Docker containers.
