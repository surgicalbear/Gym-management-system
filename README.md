Health and Fitness Club Management System

### Requirements

Ensure you have the following installed: 
+ [PostegreSQL](https://www.postgresql.org/download/)
+ [Python3](https://www.python.org/downloads/)
+ [Psycopg2](https://www.psycopg.org/install/)
+ [Rich](https://github.com/Textualize/rich)
+ [PgAdmin](https://www.pgadmin.org/download/)

### Getting Started

#### Create a new database
Connect to PostgreSQL server using the `psql` client tool:
```
psql -U postgres
```
Then, create a new database: 
```
CREATE DATABASE <>
```
Alternatively, you can do this in PgAdmin

#### Connecting to PostgreSQL database from python

Open the configuration file called `database.ini` in the project directory to store database connection parameters:
```
[postgresql]
host=localhost
database=<>
user=postgres
password=<>
port=5432
```
In the `database.ini` file, you need to replace the `<>` with your username and password. 
#### Running the program
To run the program execute the following command in the terminal:
```
python main.py
```


