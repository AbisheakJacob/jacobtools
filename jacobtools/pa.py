# importing the packages

import pandas as pd
# defining a fuction to convert the function to lowercase

def fheader(df_name):


    # creating a list of the column titles in the dataframe
    
    column_titles = list(df_name.columns)

    
    # converting all the elements in the list to lowercase
    
    column_titles = [x.lower() for x in column_titles]

    
    # removing empty space in the beginging and the end of all the headers
    
    column_titles = [x.strip() for x in column_titles]

    
    # converting all the spaces left in the header to underscore
    
    column_titles = [x.replace(" ", "_") for x in column_titles]
    
    
    # replacing the old header names with the new ones
    
    df_name.columns = column_titles


    return df_name