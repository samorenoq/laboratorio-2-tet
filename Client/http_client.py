#!/usr/bin/python

# Import libraries for socket communicaton and constants

import client_constants as cc
import requests

# Initialize constants
server_address = cc.SERVER_ADDRESS
server_port = cc.SERVER_PORT
encoding = cc.ENCODING_FORMAT

# Start the client


def execute_client():
    request_body = ''

    while request_body != str(cc.EXIT):
        request_body = handle_inputs()
        # Only send request if body is not empty
        if request_body not in [None, str(cc.EXIT)]:
            req = requests.post(f'http://{server_address}:{server_port}',
                                data=request_body.encode(encoding))
            print('______________________________________\n')
            print(f'Reader response: {req.status_code} -> {req.reason}')
            if req.status_code == 200:
                print(f'Message from Reverser: {req.text}')
            print('______________________________________\n')
    # If the user exits the program
    print('Exiting...')

# Handle client prompts and commands
def handle_inputs() -> str:
    message_prompt = "Enter a message (a-z or A-Z only) or press '0' to exit: "
    message = ''

    message = input(message_prompt)

    # Check that message is not empty
    if message == '':
        print('Empty message! Please try again...\n')
    else:
        return message


def main():
    print('______________________________________\n')
    print('-------------HTTP  CLIENT-------------\n')
    print('______________________________________\n')
    execute_client()


if __name__ == '__main__':
    main()
