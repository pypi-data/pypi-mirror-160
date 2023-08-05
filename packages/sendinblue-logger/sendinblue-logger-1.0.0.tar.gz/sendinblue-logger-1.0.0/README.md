## Description
This is a logging handler for Python's [logging](https://docs.python.org/3/library/logging.html) module to send log messages over [sendinblue](https://www.sendinblue.com/)'s transactional email service.

## Installation
```shell
$ pip install sendinblue-logger
```

## Usage
```python
import sblue
import logging
import os

handler = sblue.LoggingHandler(
    level=logging.ERROR,
    api_key=os.getenv('SENDINBLUE_API_KEY'),
    from_email='sender-email@domain.com',
    to_email='recipient-email@domain.com',
)

logging.basicConfig(
    filename='/home/user/project/project.log', 
    encoding='utf-8', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=(handler,)
)
```