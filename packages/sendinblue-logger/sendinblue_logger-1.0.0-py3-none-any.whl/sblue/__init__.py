"""
sendinblue-logger is a logging handler for Python's logging module to send log messages over sendinblue's transactional email service.
"""


import requests
import logging


class LoggingHandler(logging.Handler):
    def __init__(self, level, api_key, from_email, to_email):
        super().__init__(level)
        self.api_key = api_key
        self.from_email = from_email
        self.to_email = to_email


    def emit(self, record):
        self.format(record)
        path = record.pathname
        function = record.funcName
        message = record.message
        line = record.lineno

        content = f'''
            <p>Filepath: {path}</p>
            <p>Function Name: {function}</p>
            <p>Line Number: {lineno}</p>
            <p>Message: {message}</p>
        '''

        url='https://api.sendinblue.com/v3/smtp/email'
        headers = {
            'accept': 'application/json',
            'api-key': self.api_key,
            'content-type': 'application/json',
        }
        data = {
            'sender': {
                'name': 'Sendinblue Logging Handler',
                'email': self.from_email
            },
            'to': [
                {
                    'email': self.to_email,
                }
            ],
            'subject': 'New Log Message.',
            'htmlContent': content
        }

        try:
            resp = requests.post(url, headers=headers, json=data)
        except Exception as e:
            print(f"Couldn't log over sendinblue: {e}")
