# Solution to Insight DevOps Engineering Systems Puzzle

## Table of Contents
1. [Initial Thoughts](README.md#initial-thoughts)
2. [Communication](README.md#communication)
3. [Database](README.md#database)
4. [Solving the Success Page](README.md#solving-the-success-page)

# Initial Thoughts

As clued in by the puzzle instructions, running the system as follows leads to some errors. The solution will have the following startup method below. First, bootstrap these commands from the working directory:  

    docker-compose up -d db
    docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

Then run the system: 

    docker-compose up -d

Using Chrome Version 78.0.3904.70, navigating to 'localhost:8080' finds the connection is broken. Being somewhat unfamiliar with the various components, I'll go through the documentation of Docker, Flask, nginx, and PostgreSQL to see how each component is communicating. 

# Communication

After exploring the documentation, tutorials, and and bridge drivers in *docker-compose.yml*, the system is organized as follows. nginx -> <- flask -> <- postgresql. nginx and Flask communicate for the **web_network** and flask and postgresql communicate to make up the **db_network**. After searching through the files, in docker-compose.yml, it turns out nginx was reversed in communicating with flask on line 24. This hasn't solved the communication issue, so I'm looking into the container logs. Looking at the Dockerfile, the container exposes port 5001. Need to make sure this is correct. This didn't connect to the local host either. The documentation states that the default port is 5000, so will change 5001 -> 5000 in app.py and flask config file to see if that fixes something I'm missing. Now it loads! However, the success page returns an internal service error so will check the container logs and dive into the backend. 

# Database

Postgres container utilizes Port 5432. Referring to documentation, this is the default and confirmed this is not a communication issue with the other containers. The docker log for         **ecommerce-solution_db_1** reports an error that 'items' does not exist at character 13. Also in the flask app container logs, 

*LINE 1: INSERT INTO items (name, quantity, description, date_added) ...* 

highlights a sql database error. This points to an issue in the **models.py** file with creating an item in the database. After  studying the **app.py** and its dependency on the models, database, and forms files, the quantity field is stored as a string in **forms.py**, but structured as an integer in **models.py**. **Forms.py** changed to define quantity as an integer field, and import from library. Non integer entries are not enterable in quantity. Time permitting, error handling here would be a good idea for user quality. The success field now loads, but the string is blank. Side note: the success field navigates to 'localhost,localhost:8080/success'. The repetition does not appear part of the coding challenge itself...maybe a browser issue. 

# Solving the Success Page

The success page shows blank comma separated fields, which indicates another database error. Looking at the success function in **app.py** returning a string of db_session queries seems to be part of the error. Comparing with the **add-item** function, **success** should return a formatted version based on an html template, not just a list of strings. I've adapted the **index.html** to **submitted.html** and had the success function return this to show the final results. The success page shows all the correctly entered items for sale. 

