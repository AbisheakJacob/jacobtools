# import the libraries

import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine


# defining the create database function

def createdb(database_name):
    
    
    # pulling in the login credentials from the txt file
    
    credential = open('credentials.txt')
    line = credential.readlines()
    password = line[1][:-1]
    
    
    # establishing a connection

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password=password
    )
    conn.autocommit=True
    
    
    # creating a cursor object using the cursor() method

    cursor = conn.cursor()
    
    
    # Preparing the query to create a database

    drop_db = 'DROP DATABASE IF EXISTS ' + database_name + ';'
    create_db = 'CREATE DATABASE ' + database_name + ';'
    
    
    # drop any database of the existing name

    cursor.execute(drop_db)
    
    
    # creating a database

    cursor.execute(create_db)
    
    
    # close the connection

    conn.close()
    
    
    return print("Database " + database_name + ' created successfully.')
# defining the create database function

def dropdb(database_name):
    
    
    # pulling in the login credentials from the txt file
    
    credential = open('credentials.txt')
    line = credential.readlines()
    password = line[1][:-1]
    
    
    # establishing a connection

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password=password
    )
    conn.autocommit=True
    
    
    # creating a cursor object using the cursor() method

    cursor = conn.cursor()
    
    
    # Preparing the query to drop a database

    drop_db = 'DROP DATABASE IF EXISTS ' + database_name + ';'
    
    
    # drop any database of the existing name

    cursor.execute(drop_db)
    
    
    # close the connection

    conn.close()
    
    
    return print("Database " + database_name + ' dropped successfully.')
# defining the list all databases function

def listdb():
    
    
    # pulling in the login credentials from the txt file
    
    credential = open('credentials.txt')
    line = credential.readlines()
    password = line[1][:-1]
    
    
    # establishing a connection

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password=password
    )
    conn.autocommit=True
    
    
    # Preparing the query to list all the databases database

    list_db_query = 'SELECT datname FROM pg_database;'
    
    
    # read all the databases in the postgres server

    all_db = pd.read_sql(list_db_query, con=conn)
    
    
    # convert the tuple all_db into dataframe df_db
    
    
    df_db = pd.DataFrame(all_db)
    
    
    # close the connection

    conn.close()
    
    
    return df_db
# defining the create table from pandas dataframe

def createtb(database_name, table_name, df_name):


    # pulling in the login credentials from the txt file
    
    credential = open('credentials.txt')
    line = credential.readlines()
    password = line[1][:-1]
    
    
    # establish the path to the database

    database_path = 'postgresql://postgres:' + password + '@localhost:5432/' + database_name
    
    
    # establish the connection to the database to add the table

    engine = create_engine(database_path)
    
    
    # adding the table to the database

    df_name.to_sql(table_name, con=engine, if_exists='replace', index=False)
    
    
    # closing the connection to the database that was established

    engine.dispose()
    
    return print("Table " + table_name + " created successfully")
# defining a read table to pandas dataframe function

def readtb(database_name, table_name):


    # pulling in the login credentials from the txt file
    
    credential = open('credentials.txt')
    line = credential.readlines()
    password = line[1][:-1]
    
    
    # establishing a connection

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database=database_name,
        user="postgres",
        password=password
    )
    conn.autocommit=True
    
    
    # creating the query to pull the data from the table
    
    query1 = "SELECT * FROM " + table_name + ";"
    
    
    # read the information in the table into a dataframe
    
    new_tuple = pd.read_sql(query1, con=conn)
    new_df = pd.DataFrame(new_tuple)


    # close the connection
    
    conn.close()
    
    
    # print the particulars
    
    print("the information from the table " + table_name + " in the database " + database_name + " was extracted into the dataframe new_df\n"), 
    
    
    return new_df
# defining the list all tables in the database function

def listtb(database_name):
    
    
    # pulling in the login credentials from the txt file
    
    credential = open('credentials.txt')
    line = credential.readlines()
    password = line[1][:-1]
    
    
    # establishing a connection

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database=database_name,
        user="postgres",
        password=password
    )
    conn.autocommit=True
    
    
    # Preparing the query to list all the tables in the database

    list_tb_query = "SELECT * FROM information_schema.tables WHERE table_schema = 'public';"
    
    
    # read all the tables in the database

    all_tb = pd.read_sql(list_tb_query, con=conn)
    
    
    # convert the tuple all_db into dataframe df_db
    
    
    df_tb = pd.DataFrame(all_tb)
    
    
    # close the connection

    conn.close()
    
    
    return df_tb['table_name']