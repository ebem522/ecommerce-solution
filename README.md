# Solution to Insight DevOps Engineering Systems Puzzle

## Table of Contents
1. [Initial Thoughts](README.md#initial-thoughts)
2. [Framework](README.md#framework)


# Initial Thoughts

As clued in by the puzzle instructions, running the system as follows leads to some errors. The solution will have the following bootstrapping method outlined below. First, bootstrap these commands from the working directory:  

    docker-compose up -d db
    docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

Then run the system: 

    docker-compose up -d

Using Chrome Version 78.0.3904.70, navigating to 'localhost:8080' finds the connection is broken. Being somewhat unfamiliar with the various components, I'll go through the documentation of Docker, Flask, nginx, and PostgreSQL to see how each component is communicating. 

# Framework

After exploring the documentation, tutorials, and the codebase, the system is organized as follows. nginx -> <- flask -> <- postgresql. Nginx and flask communicate for the **web_network** and flask and postgresql communicate to make up the **db_network**. 
