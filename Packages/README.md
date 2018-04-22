# Packages

This is the directory of the Tridens Capital repository where all software packages will be housed and available for `pip install` by team members.

## Available Packages

 - API
  * Bittrex
    + bittrex : the bittrex official api package
  * api_helper
  	+ api_helper: functions to support api interface (ex: retrieve_key)

## Notes
Still under intitial organization. The Data directory is dirty, waiting for upgrade to SQL organization. 

## Package Development

Write the package in a `new_package.py' file. Create a directory 

* Packages
  * new_package
    * setup.py
    * __init__.py
    * new_package
      * __init__.py
      * new_package.py

Now change to the directory with `setup.py`

```
cd Packages\new_package
```

Then run the following command to create a wheel

```
python setup.py bdist_wheel
```
