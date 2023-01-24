import dotenv
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pymongo import MongoClient

from .routers import user_router, token_router, record_one_router

# Import the dotenv library to load environment variables from .env file
config = dotenv.dotenv_values(".env")

# Create a new FastAPI application
app = FastAPI()

# Add CORS middleware to the application
# This allows for cross-origin resource sharing
# and allows for all origins, credentials, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the 'StaticFiles' class at the route '/static'
# This allows the application to serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Create an instance of the 'Jinja2Templates' class
# This class allows to use Jinja2 template engine to render the HTML pages
# and will look into the directory specified to find the correct templates
templates = Jinja2Templates(directory="app/templates")


# Define a function that runs when the application starts up
@app.on_event("startup")
def startup_db_client():
    # Set the database client and check the connection
    mongo_uri = f'mongodb://{config["MONGO_ADMIN"]}:' + \
        f'{config["MONGO_ADMIN_PASSWORD"]}@localhost:{config["MONGO_PORT"]}' + \
            '/?authMechanism=DEFAULT'
    app.mongodb_client = MongoClient(mongo_uri)
    app.database = app.mongodb_client[config["MONGO_DB_NAME"]]

    try:
        # The sercer_info() command will throw an exception if the connection
        # fails
        app.mongodb_client.server_info()
        print("INFO:     Connected to the MongoDB database.")
    except Exception as e:
        print(f"ERROR:    Unable to connect to the MongoDB database. {e}")


# Define a function that runs when the application shuts down
@app.on_event("shutdown")
def shutdown_db_client():
    # Close the MongoDB client connection
    app.mongodb_client.close()

# Define a function that handles GET requests to the root route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "API is running."
    })


app.include_router(user_router.router, tags=["users"], prefix="/user")
app.include_router(record_one_router.router, tags=["records"], prefix="/record")
app.include_router(token_router.router, tags=["tokens"], prefix="/token")

def custom_openapi():
    """
    Generates an OpenAPI schema for the Flask application by calling the get_openapi function and passing in
    the title, version, description, and routes of the application. The generated schema is cached in the
    app.openapi_schema attribute for future use.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=config["TITLE"],
        version=config["VERSION"],
        description=config["DESCRIPTION"],
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    # Start the web server on localhost at port 5000
    uvicorn.run(app, host="127.0.0.1", port=5000)
