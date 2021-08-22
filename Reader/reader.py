# Import libraries for socket communication, threading, and reader_constants

import reader_constants
import socket
import threading
import time

# Define some variables that are constant
encoding = reader_constants.ENCODING_FORMAT
buff_size = reader_constants.RECV_BUFFER_SIZE

# Define new socket connection object for the reader
reader_socket = socket.socket()
reader_address = reader_constants.READER_ADDRESS
reader_port = reader_constants.READER_PORT

# Define capitalizer constants
capitalizer_address = reader_constants.CAPITALIZER_ADDRESS
capitalizer_port = reader_constants.CAPITALIZER_PORT


# Start the server
def execute_server():
    reader_tuple = (reader_address, reader_port)
    reader_socket.bind(reader_tuple)
    # Allow five unaccepted connections before refusing new connections
    reader_socket.listen(5)
    print(f'Reader is listening on port {reader_port}...\n')

    # Start handling client messages
    while True:
        client_socket, client_address = reader_socket.accept()
        print(
            f'{client_address[0]} has connected using their port {str(client_address[1])}\n')
        # Create a new thread to take care of each new client
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        client_thread.start()
    print('Closing reader socket...')
    reader_socket.close()


# Functionality for handling client messages
def handle_client(client_socket: socket.socket, client_address: tuple) -> None:
    client_is_connected = True

    # Connect to capitalizer socket
    capitalizer_socket = socket.socket()
    capitalizer_tuple = (capitalizer_address, capitalizer_port)
    capitalizer_socket.connect(capitalizer_tuple)

    while client_is_connected:
        client_message = str(client_socket.recv(
            buff_size).decode(encoding))

        # If the client wants to exit
        if client_message == str(reader_constants.EXIT):
            response = '10 - QUIT'
            client_socket.sendall(response.encode(
                encoding
            ))
            client_is_connected = False

            # Close connection to Capitalizer
            capitalizer_socket.send(
                (str(reader_constants.EXIT)+'\n').encode(encoding))
            # Print capitalizer response
            capitalizer_response = capitalizer_socket.recv(buff_size)
            print(
                f'Capitalizer response: {capitalizer_response.decode(encoding)}')
            print('Closing connection to Capitalizer...\n')
            capitalizer_socket.close()

        # If the client's message contains invalid characters
        elif not client_message.isalpha():
            response = '20 - INVALID CHARACTERS\n'
            send_to_client(client_socket, response)
            print('Client input is not valid')

        # Otherwise, the client's message is ok
        else:
            response = f'30 - MSG OK -> {client_message}'
            send_to_client(client_socket, response)
            print('______________________________________\n')
            print(
                f'Message from the client at {client_address[0]}:{client_address[1]}: {client_message}\n')
            print(f'Message to capitalizer: {client_message}\n')
            send_to_capitalizer(capitalizer_socket,
                                client_socket, client_message)

    print(
        f'Client with address {client_address[0]} on port {client_address[1]} disconnected')
    client_socket.close()


# Function to send client text to StringCapitalizer
def send_to_capitalizer(capitalizer_socket: socket.socket, client_socket: socket.socket, msg: str) -> None:
    # Append new line to message for BufferedReader
    capitalizer_socket.send((msg+'\n').encode(encoding))
    capitalizer_response = capitalizer_socket.recv(buff_size)
    print(
        f'Capitalizer response: {capitalizer_response.decode(encoding).strip()}')
    print('______________________________________\n')

    # Send the reverser response, received from the capitalizer, to the client
    reverser_response = capitalizer_socket.recv(buff_size)
    if (reverser_response):
        send_to_client(client_socket,
                       f'{reverser_response.decode(encoding)}\n')


# Function to define behavior for sending messages to the client
def send_to_client(client_socket: socket.socket, msg: str) -> None:
    client_socket.send(msg.encode(encoding))


def main():
    print('______________________________________\n')
    print('________________READER________________\n')
    print('______________________________________\n')
    execute_server()


if __name__ == "__main__":
    main()
