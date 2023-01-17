# <div align="center"><img src="docs/img/api-logo.jpg" alt="API Logo" style="width: 20%;"> <p align="center"> Generic API: : The All-Purpose Solution for Your API Needs </p></div>

This GitHub repo contains code for a generic API in Python using the FastAPI framework. Includes examples for HTTP requests, auth, data validation, error handling, and has a config file for easy setup. Also includes example usage with a sample client app.

## Prerequisites
Before running the code in this repository, you must create a ```.env``` file containing the necessary environment variables to run the framework and place it in the root of the repository, as explained [here](docs/env_file/env-file-description.md).

Additionally, you must have KeyCloak installed and configured using Docker Compose.

### KeyCloak Installation using Docker Compose
1. Make sure you have Docker and Docker Compose installed on your system. If not, you can download Docker from the official website (https://www.docker.com/get-started) and follow the instructions for your operating system to install it. If you install the Docker Desktop, Docker Compose may be installed automatically. You can also install Docker Compose by following the instructions on this link (https://docs.docker.com/compose/install/)
2. Use the existing ```docker-compose.yml``` file in the root of the repo, you can find the file here: [docker-compose.yml](docker-compose.yaml)
3. Run KeyCloak container by running the following command in the root directory of the repository where the ```docker-compose.yml``` file is located:

```
docker-compose up -d
```

4. Configure Keycloak by following the steps outlined in the [Keycloak Configuration Steps](docs/keycloak-configuration.md)

Once you have completed these steps, you should be able to run the code in this repository. 

Please note that the code in this repository is just an example and you will need to adapt it to your own needs.
Please also note that, if you want to run keycloak on different ports or use different environment variables, you can change them accordingly in the `docker-compose.yml` file.
