# AnalyticsStack

**AnalyticsStack** is a my personal python library that contains code to automate day to day activities.

## Installation and updating

Installing the package from PyPI

```bash
pip install AnalystStack
```

OR

Installing the package from the github repository

```bash
pip install git+https://github.com/AbisheakJacob/AnalyticsStack
```

Installing the local repository so that it updates automatically when a change is made.

```bash
pip install .
```


## Structure

### Connectors

This module contains codes to connect and work with data in Google BigQuery and Databricks.

| Function Name     | Description                                        |
| ----------------- | -------------------------------------------------- |
| read_data         | Read a table from database as a DataFrame               |
| write_data | Write data to database from DataFrame |
| get_all_table_names | Get all table names in a given project/catalog |
| get_datatypes | Get the datatypes for all columns in a table |
| get_fillrate | Get Fill Rate Analyssi for all the columns in a table |

### Format

This module support formatting python code or SQL queries.

| Function Name          | Description                                                                 |
| ---------------------- | --------------------------------------------------------------------------- |
| pyton | Format python code                    |
| sql         | Format SQL code |

### IO

This module makes it easier to read and write data.

#### postgres

| Function Name             | Description                                                        |
| ------------------------- | ------------------------------------------------------------------ |
| reader.excel | read data from an excel |
| reader.csv | read data from a csv |
| writer.exel | write data to excel |
| writer.csv | Write data to csv |
| writer.markdown | write tables and string to markdown |
| writer.txt | write tables and string to text file |
| writer.clipboard | copy data to clipboard |

## Next Steps

1. Custom function to perform basic eda on a given dataframe (info, null values, shape, size)
2. Function to perform match% analysis and perfrom a venn diagram for easier visualization

## License

**_The Reference to this library can be found here:_**
The base construct of this library is referenced from [this article](https://mikehuls.medium.com/create-your-custom-python-package-that-you-can-pip-install-from-your-git-repository-f90465867893)
