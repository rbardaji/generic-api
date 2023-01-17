# generic-api
This GitHub repo contains code for a generic API in Python using the FastAPI framework. Includes examples for HTTP requests, auth, data validation, error handling, and has a config file for easy setup. Also includes example usage with a sample client app.

## Prerequisites
Before running the code in this repository, you must have KeyCloak installed and configured using Docker Compose.

### KeyCloak Installation using Docker Compose
1. Make sure you have Docker and Docker Compose installed on your system. If not, you can download Docker from the official website (https://www.docker.com/get-started) and follow the instructions for your operating system to install it. You can install Docker Compose by following the instructions on this link (https://docs.docker.com/compose/install/)
2. Create a new file named `docker-compose.yml` in the root of your project and paste the following content:

```
version: '3'
services:
keycloak:
image: jboss/keycloak
environment:
- KEYCLOAK_USER=admin
- KEYCLOAK_PASSWORD=password
- PROXY_ADDRESS_FORWARDING=true
ports:
- "8080:8080"
```

3. Run KeyCloak container by running the following command in the same directory where you created the `docker-compose.yml` file:


```
docker-compose up
```

4. Access the KeyCloak server by opening a web browser and navigating to `http://localhost:8080/auth`
5. Create a new realm and configure it to your needs.

### KeyCloak Configuration
1. Add the client that you will use to connect to the KeyCloak server.
2. Configure the client with the appropriate settings, such as valid redirect URIs and granted permissions.
3. Obtain the `client_id` and `client_secret` for the client that you just created.
4. Use this `client_id` and `client_secret` in your application to connect to the KeyCloak server.

Once you have completed these steps, you should be able to run the code in this repository. 

Please note that the code in this repository is just an example and you will need to adapt it to your own needs.
Please also note that, if you want to run keycloak on different ports or use different environment variables, you can change them accordingly in the `docker-compose.yml` file.
