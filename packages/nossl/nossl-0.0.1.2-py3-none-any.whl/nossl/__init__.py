import ssl
import requests

import pathlib


def turn_off_ssl():
    print('======== Turn off SSL... ========')

    ssl_path = pathlib.Path(ssl.__file__)
    req_path = pathlib.Path(requests.__file__).parent / 'sessions.py'

    # Break SSL of ssl library.
    with ssl_path.open('r') as f:
        data = f.read()
        data = data.replace(
            '_create_default_https_context = create_default_context',
            '_create_default_https_context = _create_unverified_context'
        )

    with ssl_path.open('w') as f:
        f.write(data)


    print(f'"{ssl_path}": Done.')

    # Break SSL of requests library.
    with req_path.open('r') as f:
        data = f.read()
        data = data.replace(
            'self.verify = True',
            'self.verify = False'
        )

    with req_path.open('w') as f:
        f.write(data)

    print(f'"{req_path}": Done.')


def turn_on_ssl():
    print('======== Turn on SSL... ========')

    ssl_path = pathlib.Path(ssl.__file__)
    req_path = pathlib.Path(requests.__file__).parent / 'sessions.py'

    # Break SSL of ssl library.
    with ssl_path.open('r') as f:
        data = f.read()
        data = data.replace(
            '_create_default_https_context = _create_unverified_context',
            '_create_default_https_context = create_default_context',
        )

    with ssl_path.open('w') as f:
        f.write(data)


    print(f'"{ssl_path}": Done.')

    # Break SSL of requests library.
    with req_path.open('r') as f:
        data = f.read()
        data = data.replace(
            'self.verify = False',
            'self.verify = True',
        )

    with req_path.open('w') as f:
        f.write(data)

    print(f'"{req_path}": Done.')