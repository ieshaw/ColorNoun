# Packages

This is the directory of the Tridens Capital repository where all software packages will be housed and available for import by team members. 

## Package Use

Since all scripts are designed to be run from the Tridens home directory, at the top of any script simply import directly from the file in the Packages directory.

```
from Packages.subdir.file import module
```

## Available Packages

 - API
  * Bittrex
    + bittrex : the bittrex official api package
    + helper: functions specific to executing on the Bittrex exchange
  * Helper
    + helper: functions to support api interface (ex: retrieve_key)
