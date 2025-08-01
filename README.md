# jacobtools

**jacobtools** is a Python package that contains handy functions the tackle day to day code. 
It's main goal, however, is to demonstrate how to create a package.  

article for a detailed explanation on how to create your 
custom Python package that is installable from your GitHub repo!

## Installation and updating
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Toolbox like below. 
Rerun this command to check for and install  updates .
```bash
pip install git+https://github.com/Muls/toolbox
```

## Usage
Features:
* functions.listChunker  --> generator that chunks and interable in evenly sized chunks 
* functions.weirdCase    --> converts a string to a totally unreadable format
* functions.report      --> prints to the console with a timestamp
* decorators.singleton  --> used for decoratint your class to make it a singleton

#### Demo of some of the features:
```python
import jacobtools
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Database module (db.py)

### infodb(hostname, username, password, databasename)
The infodb function takes in the database credentials and stores them as global variables, that can be used in by other functions.
- This function also creates the database URL that can be used by SQLAlchemy module (only for MySQL databases)

### listtb()
The listtb function provides the list of all the tables in the given database.

***The Reference to this library can be found here:***
Check out [this](https://mikehuls.medium.com/create-your-custom-python-package-that-you-can-pip-install-from-your-git-repository-f90465867893)
