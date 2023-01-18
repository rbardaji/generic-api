import dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

# Import the dotenv library to load environment variables from .env file
config = dotenv.load_dotenv()

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
@app.get("/")
async def root():
    # Return a JSON response with message "API is working!"
    return {"message": "API is working!"}

if __name__ == "__main__":
    # Start the web server on localhost at port 5000
    uvicorn.run(app, host="127.0.0.1", port=5000)
