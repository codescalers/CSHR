# Runing the project using Docker and Docker Compose

To run the full project with all instances, follow these steps:

1. Set Environment Variables

Create a `.env` file beside the [config](./config/) directory and set the necessary environment variables. Refer to the previous section for sample environment variable configurations.

2. Execute Docker Compose

Run the following command to start the Docker containers:

```sh
cd docker
docker compose --env-file=.././config/.env  up --build 
```

After executing the command, you should see a confirmation similar to the following:

3. Verify Successful Deployment

This indicates that the Docker containers are being created and the services are starting up.

- ![docker-compose-deployments](docs/docker-compose-deployments.png)
