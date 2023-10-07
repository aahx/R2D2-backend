attempting to host on aws lambda

- Mangun wrapper is good

## Issue 1: Zipped files were too large > 100 mb.
#### Resolved: 
- Removed unncessary dependencies.

<br/>

## Issue 2: Can not locate dependency pydantic_core
#### Resolved: 
- https://github.com/pydantic/pydantic/issues/6557
- ` "Well there's you're issue - you're installing the x86_64 wheel but trying to run it on amd64." `
- Was building AWS Lambda function on amd64 architecture, changed to x86_64 and issue was resolved

<br/>

## Issue 3: AWS module could not fine models.py
#### Resolved: 
- Created models dir and __ init__.py
- Ran command `zip -ru aws_lambda_artifact.zip models`  to include 'models' directory on the same level as main.py

<br/>


## Issue 4: "errorMessage": "Unable to import module 'main': Error importing numpy: you should not try to import numpy from\n        its source directory; please exit the numpy source tree, and relaunch\n        your python interpreter from there.",

### Not Resolved:
### Attempts:
- Create Numpy layer and added to AWS lambda function - did not resolve

