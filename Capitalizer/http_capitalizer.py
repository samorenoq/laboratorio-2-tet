# Import constants
import capitalizer_constants as cc

# Import libraries for creating an http server
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
# Import library for I/O operations with bytes
from io import BytesIO
# Import library for making requests
import requests

# Define some constants
encoding = cc.ENCODING_FORMAT
rev_address = cc.REVERSER_ADDRESS
rev_port = cc.REVERSER_PORT

# Class for defining requests


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get client address and port
        (client_ip, client_port) = self.client_address

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        response = BytesIO()
        print('______________________________________\n')

        self.send_response(200, 'Sending to Reverser')

        #Print message from Reader
        print(
            f'Message from Reader at {client_ip}:{client_port}: {body.decode(encoding)}')
        print('\n**************************************\n')

        # Modify body to all-caps and send it to Reader
        modified_body = body.decode(encoding).upper()

        # Send request to Reverser
        req = requests.post(
            f'http://{rev_address}:{rev_port}', data=modified_body.encode(encoding))

        # Print response from Reverser
        print(f'Reverser response: {req.status_code} -> {req.reason}')
        print(f'Capitalized message: {modified_body}')

        # Send Reverser response to Capitalizer
        response.write(req.text.encode(encoding))

        self.end_headers()
        print('______________________________________\n')
        self.wfile.write(response.getvalue())


# Function for starting the server
def execute_server():
    # Create server to listen on all available IP addresses on the specified port
    with ThreadingHTTPServer(('', cc.CAPITALIZER_PORT), RequestHandler) as httpd:
        print("Capitalizer serving on port ", cc.CAPITALIZER_PORT)
        httpd.serve_forever()


def main():
    print('______________________________________\n')
    print('-----------HTTP CAPITALIZER-----------\n')
    print('______________________________________\n')
    execute_server()


if __name__ == '__main__':
    main()
