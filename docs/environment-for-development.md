# Creating a Python Virtual Environment with venv

Python virtual environments are used to create isolated development environments to keep project-specific dependencies separate from other projects. This tutorial will show you how to create a virtual environment using the `venv` module in Python 3.

## Step 1: Install `venv`

The `venv` module is included in Python 3, so you don't need to install it.

## Step 2: Create a Virtual Environment 

Create a directory for your project, and then create a virtual environment in that directory. This can be done with the following command:

```
python -m venv path/to/my_project
```

## Step 3: Activate the Virtual Environment 

Once you've created the virtual environment, you need to activate it. This can be done with the following command:

```
source path/to/my_project/bin/activate
```

## Step 4: Install Dependencies 

You can now install the dependencies for your project. This can be done by using the `pip` command to install from the `requirements.txt` file.

```
pip install -r requirements.txt
```

# Running Code

Using the command line tool "uvicorn" to execute the code with the command `uvicorn app.main:app --reload` on the root folder is necessary to execute code.

It is recommended to run the code locally on a computer to test and debug it prior to deploying it to a production environment.

# Running Tests

It is recommended to run the pytest tests if changes have been made to the code. To run the tests, simply type the command `pytest` in the root directory of the repository. This will ensure that any changes made to the code have not broken any existing functionality.
