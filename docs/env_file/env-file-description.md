# Using the .env File to Manage Environment Variables in Your Generic API

This document provides information about environment variables available for configuring the Generic API.

We have created an [.env_template file](./.env_template) for you to use as a template. Rename the file to .env and move it to the root of your repository to get started.

## Keycloak Docker Image

### KEYCLOAK_VERSION

`KEYCLOAK_VERSION` is the version of Keycloak Docker image. It is used to specify the version of Keycloak that will be used for the container.

**Default**: 20.0.3

### KEYCLOAK_ADMIN

`KEYCLOAK_ADMIN` is the username of the admin user that will be created in the KeyCloak container. This user is used to access the Keycloak admin console.

**Default**: admin

### KEYCLOAK_ADMIN_PASSWORD

`KEYCLOAK_ADMIN_PASSWORD` is the password of the admin user that will be created in the KeyCloak container. This user is used to access the KeyCloak admin console.

**Default**: admin

### KEYCLOAK_PORT

`KEYCLOAK_PORT` is the port number on which the KeyCloak container will be listening. This is used to specify the port that the KeyCloak container will be listening on.

**Default**: 8080

### KEYCLOAK_DATA_FOLDER

The KEYCLOAK_DATA_FOLDER is the directory on your local host where the Keycloak's configuration files and user databases will be saved.

**Default**: ./keycloak_data