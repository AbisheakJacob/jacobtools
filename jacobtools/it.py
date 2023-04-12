# importing the packages

from itertools import combinations
from collections import Counter
import pandas as pd
# creating a function to calculate the count of all the possible combinations

def combo(df_data, column_name, groupby_column, combo_no):
    
    
    # create the groupby column and the column name
    # groupby column - the column which you choose to use as the pivot for the entire combination operation
    # column_name - the column that you wish to create the combinations along a pivot
    # creating a dataframe along the groupby column where the combination column will form a list
    
    new_data = df_data.groupby(groupby_column)[column_name].agg[list].reset_index()
    
    
    # creating a new column all-combinations that contains all the combinations of the items as per the combo_no
    
    new_data['all_combinations'] = new_data[column_name].apply(lambda x: list(combinations(x,combo_no)))
    
    
    # count the number of occurances of each particular combinations
    
    combinations_counter = Counter([tuple(sorted(i)) for sublist in new_data['all_combinations'] for i in sublist])
    
    
    # sort all the combinations in the descending order
    
    all_combinations_sorted = combinations_counter.most_common()
    
    
    # returns the sorted series 
    
    return all_combinations_sorted