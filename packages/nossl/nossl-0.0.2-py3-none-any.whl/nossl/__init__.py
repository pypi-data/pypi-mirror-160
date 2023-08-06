import sys

import ssl
import requests

import pathlib


def turn_off_ssl():
    print('======== Turn off SSL... ========')

    ssl_path = pathlib.Path(ssl.__file__)
    req_path = pathlib.Path(requests.__file__).parent / 'sessions.py'

    # Turn off SSL of ssl library.
    with ssl_path.open('r') as f:
        data = f.read()
        data = data.replace(
            '_create_default_https_context = create_default_context',
            '_create_default_https_context = _create_unverified_context'
        )

    with ssl_path.open('w') as f:
        f.write(data)

    print(f'"{ssl_path}": Done.')

    # Turn off SSL of requests library.
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

    # Turn on SSL of ssl library.
    with ssl_path.open('r') as f:
        data = f.read()
        data = data.replace(
            '_create_default_https_context = _create_unverified_context',
            '_create_default_https_context = create_default_context',
        )

    with ssl_path.open('w') as f:
        f.write(data)

    print(f'"{ssl_path}": Done.')

    # Turn on SSL of requests library.
    with req_path.open('r') as f:
        data = f.read()
        data = data.replace(
            'self.verify = False',
            'self.verify = True',
        )

    with req_path.open('w') as f:
        f.write(data)

    print(f'"{req_path}": Done.')


def main():
    if len(sys.argv) != 2:
        print('Usage: nossl on or nossl off')
        sys.exit(1)

    if sys.argv[1] == 'on':
        turn_on_ssl()
    elif sys.argv[1] == 'off':
        turn_off_ssl()
    else:
        print('Invalid argument', sys.argv[1])


if __name__ == '__main__':
    main()