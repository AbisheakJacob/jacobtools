# JacobTools

**JacobTools** is a my personal python library that contains code to automate day to day activities.

## Installation and updating

Installing the package from the github repository

```bash
pip install git+https://github.com/AbisheakJacob/JacobTools
```

Installing the local repository so that it updates automatically when a change is made.

```bash
pip install .
```

### Creating C extension

```python
from setuptools import setup 
from Cython.Build import cythonize

setup(
        ext_modules=cythonize("src/jacobtools/harmonic_mean.pyx")
        )
```

## Structure

### gbq_queries

This module contains codes to connect and work with data in Google BigQuery.

| Function Name     | Description                                        |
| ----------------- | -------------------------------------------------- |
| query_gbq         | Read a table from GBQ as a DataFrame               |
| fillrate_analysis | Perfrom Fill Rate Analysis on GBQ dataset or table |

### preprocessing

This module contains preprocessing steps to be performed on the data before actual analysis.

| Function Name          | Description                                                                 |
| ---------------------- | --------------------------------------------------------------------------- |
| drop_columns_by_schema | Drop the columns that are markded in the Schema Document                    |
| enforce_schema         | Apply the datatypes provided in schema document to the Columns in the Table |

### sql_generation

This module automatically generate SQL codes from DataFrame for ease of use.

#### postgres

| Function Name             | Description                                                        |
| ------------------------- | ------------------------------------------------------------------ |
| generate_create_table_sql | Generates SQL code to create the schema to upload data to postgres |

## Next Steps

1. Custom function to perform basic eda on a given dataframe (info, null values, shape, size)
2. Function to perform match% analysis and perfrom a venn diagram for easier visualization

## License

**_The Reference to this library can be found here:_**
The base construct of this library is referenced from [this article](https://mikehuls.medium.com/create-your-custom-python-package-that-you-can-pip-install-from-your-git-repository-f90465867893)
