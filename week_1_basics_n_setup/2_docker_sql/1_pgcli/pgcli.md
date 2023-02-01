## how to install pgcli into docker?

To install pgcli into a Docker container, you can use the following steps:

 -   Create a new Dockerfile in the directory where you want to build the image.

-    In the Dockerfile, add the following lines to install pgcli and its dependencies:


```docker
FROM python:3
RUN pip install pgcli
```

  -  Build the Docker image by running the following command in the same directory as the Dockerfile:

```bash
docker build -t pgcli .
```
-    Once the image is built, you can run a container from the image by running the following command:

```bash
docker run -it pgcli pgcli
```

Note: you may also need to pass in environment variables for the database connection and run the image with the appropriate flag to access the host network.

You can also use pre-built images from the Docker hub to install pgcli directly without building the image yourself.

```bash
docker pull postgres:latest
docker run -it --network host postgres:latest pgcli
```

This will install the latest version of Postgres and pgcli, and run the pgcli command in an interactive terminal in the container, allowing you to connect to a Postgres server running on the host machine.
