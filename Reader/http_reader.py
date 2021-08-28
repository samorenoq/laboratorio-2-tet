# Import constants
import reader_constants as rc

# Import libraries for creating an http server
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
# Import library for I/O operations with bytes
from io import BytesIO
# Import library for making requests
import requests

# Define some constants
cap_address = rc.CAPITALIZER_ADDRESS
cap_port = rc.CAPITALIZER_PORT
encoding = rc.ENCODING_FORMAT


# Class for defining requests
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get client address and port
        (client_ip, client_port) = self.client_address

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        response = BytesIO()
        print('______________________________________\n')
        # Verify if message is valid
        if (self.is_valid(body)):
            self.send_response(200, 'Sending to Capitalizer')
            # Bytes buffer to respond to client
            print(
                f'Message from client at {client_ip}:{client_port}: {body.decode(encoding)}')

            print('\n**************************************\n')

            # Send request to Capitalizer
            req = requests.post(
                f'http://{cap_address}:{cap_port}', data=body)

            #Print response from Capitalizer
            print(f'Capitalizer response: {req.status_code} -> {req.reason}')
            print(f'Read message: {body.decode(encoding)}')

            #Send Capitalizer response to Reader
            response.write(req.text.encode(encoding))

        else:
            self.send_error(400, 'INVALID CHARACTERS')
        self.end_headers()
        print('______________________________________\n')
        self.wfile.write(response.getvalue())

    # Method to check if message is valid
    def is_valid(self, body: bytes) -> bool:
        return body.decode(encoding).isalpha()


# Function for starting the server
def execute_server():
    # Create server to listen on all available IP addresses on the specified port
    with ThreadingHTTPServer(('', rc.READER_PORT), RequestHandler) as httpd:
        print("Reader serving on port ", rc.READER_PORT)
        httpd.serve_forever()


def main():
    print('______________________________________\n')
    print('-------------HTTP  READER-------------\n')
    print('______________________________________\n')
    execute_server()


if __name__ == '__main__':
    main()
