# Using the .env File to Manage Environment Variables in Your Generic API

This document provides information about environment variables available for configuring the Generic API.

We have created an [.env_template file](./.env_template) for you to use as a template. Rename the file to .env and move it to the root of your repository to get started.

## OpenAPI configurarion

### TITLE

`TITLE` is the text that is displayed on the OpenAPI documentation page.

### DESCRIPTION

`DESCRIPTION` is the text that describes the purpose of the API. It is displayed on the OpenAPI documentation page.

### VERSION

`VERSION` of the API.

## Route configuration

### RECORD_ONE_NAME

`RECORD_ONE_NAME` is the name of the first record. This variable is used to specify the name of the first record that will be created in the API.

### RECORD_ONE_TAG

`RECORD_ONE_TAG` is the tag associated with the first record. This variable is used to specify the tag that will be associated with the first record in the API.

## Connection to KeyCloak

### KEYCLOAK_URL

`KEYCLOAK_URL` is the URL of the Keycloak server that the Generic API will use for authentication.

### KEYCLOAK_REALM

`KEYCLOAK_REALM` is the name of the realm that will be used by the Generic API for authentication. This variable specifies the realm within the Keycloak server that the Generic API will use to authenticate and authorize users. The default value is "myrealm", but it can be [set]((../keycloak-configuration.md)) to any realm created on Keycloak server.

### KEYCLOAK_ADMIN_SECRET

`KEYCLOAK_ADMIN_SECRET` is the secret used to access the Keycloak admin API. This secret is used to configure the Generic API to communicate with the Keycloak server. It is important to note that this variable cannot be completed until Keycloak has been properly configured and the secret has been obtained (more information [here](../keycloak-configuration.md)). Once the secret has been obtained and the variable has been set, it will be necessary to restart the docker-compose ```docker-compose down``` and ```docker-compose up --build --force-recreate --no-deps -d``` in order for the changes to take effect.

### KEYCLOAK_REALM_SECRET

`KEYCLOAK_REALM_SECRET` is the secret used to access the Keycloak REALM API. This secret is used to configure the Generic API to communicate with the your REALM from the Keycloak server. It is important to note that this variable cannot be completed until Keycloak has been properly configured and the secret has been obtained (more information [here](../keycloak-configuration.md)). Once the secret has been obtained and the variable has been set, it will be necessary to restart the docker-compose ```docker-compose down``` and ```docker-compose up --build --force-recreate --no-deps -d``` in order for the changes to take effect.

### KEYCLOAK_ADMIN

`KEYCLOAK_ADMIN` is the username of the admin user that will be created in the KeyCloak container. This user is used to access the Keycloak admin console.

### KEYCLOAK_ADMIN_PASSWORD

`KEYCLOAK_ADMIN_PASSWORD` is the password of the admin user that will be created in the KeyCloak container. This user is used to access the KeyCloak admin console.

## Connection to MongoDB

### MONGO_HOST

`MONGO_HOST` is the hostname and port of the MongoDB server. It is used to specify where the MongoDB server can be found.

### MONGO_PORT

`MONGO_PORT` is the port number on which the MongoDB container will be listening. This is used to specify the port that the MongoDB container will be listening on.

### MONGO_ADMIN

`MONGO_ADMIN` is the username of the admin user that will be created in the MongoDB container. This user is used to access the MongoDB admin console.

### MONGO_ADMIN_PASSWORD

`MONGO_ADMIN_PASSWORD` is the password of the admin user that will be created in the MongoDB container. This user is used to access the MongoDB admin console.

### MONGO_DB_NAME

`MONGO_DB_NAME` is the name of the MongoDB database that will be used by the Generic API. 

## Generic API Docker Image

### GENERIC_API_PORT

`GENERIC_API_PORT` is the port number on which the Generic API container will be listening. This is used to specify the port that the Generic API container will be listening on.

## MongoDB Docker Image

### MONGO_VERSION

`MONGO_VERSION` is the version of MongoDB Docker image. It is used to specify the version of MongoDB that will be used for the container.

### MONGO_DATA_FOLDER

The `MONGO_DATA_FOLDER` is the directory on your local host where the MongoDB's data files will be saved.

## Keycloak Docker Image

### KEYCLOAK_VERSION

`KEYCLOAK_VERSION` is the version of Keycloak Docker image. It is used to specify the version of Keycloak that will be used for the container.

### KEYCLOAK_PORT

`KEYCLOAK_PORT` is the port number on which the KeyCloak container will be listening. This is used to specify the port that the KeyCloak container will be listening on.

### KEYCLOAK_DATA_FOLDER

The KEYCLOAK_DATA_FOLDER is the directory on your local host where the Keycloak's configuration files and user databases will be saved.

## Postgres Docker Image

### POSTGRES_USER

`POSTGRES_USER` is the username of the user that will be created in the Postgres container. This user is used to access the Postgres database.

### POSTGRES_PASSWORD

`POSTGRES_PASSWORD` is the password of the user that will be created in the Postgres container. This user is used to access the Postgres database.

### POSTGRES_DB

`POSTGRES_DB` is the name of the Postgres database that will be used by the Generic API. 

### POSTGRES_PORT

`POSTGRES_PORT` is the port number on which the Postgres container will be listening. This is used to specify the port that the Postgres container will be listening on.

### POSTGRES_DATA_FOLDER

`POSTGRES_DATA_FOLDER` is the directory on your local host where the Postgres's data files will be saved.
