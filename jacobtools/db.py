# import the libraries
from sqlalchemy import create_engine, inspect


# defining the parameters for the database connection as global variables
def infodb(host, user, passw, dbname):
    
    # define the global variables
    global hostname
    global username
    global password
    global databasename
    global databaseurl

    # assign the values of the database credentials to the global variables
    hostname = str(host)
    username = str(user)
    password = str(passw)
    databasename = str(dbname)
    databaseurl = f'mysql://{username}:{password}@{hostname}/{databasename  }'


# defining the create table from pandas dataframe
# def createtb(database_name, table_name, df_name):


#     # pulling in the login credentials from the txt file
#     credential = open('credentials.txt')
#     line = credential.readlines()
#     password = line[1][:-1]
    
    
#     # establish the path to the database

#     database_path = 'postgresql://postgres:' + password + '@localhost:5432/' + database_name
    
    
#     # establish the connection to the database to add the table

#     engine = create_engine(database_path)
    
    
#     # adding the table to the database

#     df_name.to_sql(table_name, con=engine, if_exists='replace', index=False)
    
    
#     # closing the connection to the database that was established

#     engine.dispose()
    
#     return print("Table " + table_name + " created successfully")
# # defining a read table to pandas dataframe function

# def readtb(database_name, table_name):


#     # pulling in the login credentials from the txt file
    
#     credential = open('credentials.txt')
#     line = credential.readlines()
#     password = line[1][:-1]
    
    
#     # establishing a connection

#     conn = psycopg2.connect(
#         host="localhost",
#         port="5432",
#         database=database_name,
#         user="postgres",
#         password=password
#     )
#     conn.autocommit=True
    
    
#     # creating the query to pull the data from the table
    
#     query1 = "SELECT * FROM " + table_name + ";"
    
    
#     # read the information in the table into a dataframe
    
#     new_tuple = pd.read_sql(query1, con=conn)
#     new_df = pd.DataFrame(new_tuple)


#     # close the connection
    
#     conn.close()
    
    
#     # print the particulars
    
#     print("the information from the table " + table_name + " in the database " + database_name + " was extracted into the dataframe new_df\n"), 
    
    
#     return new_df


# defining the list all tables in the database function
def listtb(database_name):
    
    try:
        # Create a SQLAlchemy engine to connect to the database
        engine = create_engine(databaseurl)

        # Create an Inspector for the engine
        inspector = inspect(engine)

        # Get the table names from the database
        table_names = inspector.get_table_names()

        # return the table names
        return table_names

    except Exception as e:

        # if error return the error
        return str(e)