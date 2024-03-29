# %%
# import the libraries
from sqlalchemy import create_engine, inspect, MetaData, Table, text
import pandas as pd


# %%
# defining the parameters for the database connection as global variables
def infodb(host, user, passw, dbname, show_url=False):
    # write a docstring for this function
    """
    This function is used to define the parameters for the database connection as global variables.
    This function also defines the MySQL database url for the connection.

    :param host: object
    :param user: object
    :param passw: object
    :param dbname: object
    :return:
    """

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
    databaseurl = "mysql://" + user + ":" + password + "@" + host + "/" + databasename

    # if show_url is True then print the database url
    if show_url:
        print(f"The database url is: {databaseurl}")


# %%
# defining the list all tables in the database function
def listtb():
    """
    This function is used to list all the tables in the database.
    :return:
    """
    try:
        # Create a SQLAlchemy engine to connect to the database
        engine = create_engine(databaseurl)

        # Create an Inspector for the engine
        inspector = inspect(engine)

        # Get the table names from the database
        table_names = inspector.get_table_names()

        # return the table names
        return pd.DataFrame(table_names)

    except Exception as e:

        # if error return the error
        return str(e)


# %%
# upload a dataframe to the database
def uploadtb(df, tbname):
    """
    This function is used to upload a dataframe to the database.
    :param df: dataframe
    :param tbname: object
    :return:
    """

    # convert the table name to string
    tbname = str(tbname)

    try:
        # Create a SQLAlchemy engine to connect to the database
        engine = create_engine(databaseurl)

        # engine.execute(text('DELETE FROM NseTicker'))
        with engine.connect() as conn:
            conn.execute(text(f"DELETE FROM {tbname}"))
            conn.commit()

        # upload the dataframe to the database
        df.to_sql(tbname, engine, if_exists="append", index=False)

        # return a success message
        return "Dataframe uploaded successfully"

    except Exception as e:

        # if error return the error
        return str(e)


# %%
# download a table from the database
def downloadtb(tbname):
    """
    This function is used to download a table from the database.
    :param tbname: object
    :return:
    """

    # convert the table name to string
    tbname = str(tbname)

    try:
        # Create a SQLAlchemy engine to connect to the database
        engine = create_engine(databaseurl)

        # download the table from the database
        df = pd.read_sql(tbname, engine)

        # return the dataframe
        return df

    except Exception as e:

        # if error return the error
        print(str(e))


# %%
# delete a table from the database
def deletetb(tbname):
    """
    This function is used to delete a table from the database.
    :param tbname: object
    :return:
    """

    # convert the table name to string
    tbname = str(tbname)

    try:
        # Create a SQLAlchemy engine to connect to the database
        engine = create_engine(databaseurl)

        # Create a MetaData object
        metadata = MetaData()

        # Reflect the existing table
        existing_table = Table(tbname, metadata, autoload_with=engine)

        # Drop the table
        existing_table.drop(engine, checkfirst=True)

        # return a success message
        return "Table deleted successfully"

    except Exception as e:

        # if error return the error
        return str(e)
