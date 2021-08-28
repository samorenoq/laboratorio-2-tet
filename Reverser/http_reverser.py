# Import constants
import reverser_constants as rc

# Import libraries for creating an http server
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
#Import library for I/O operations with bytes
from io import BytesIO
#Import library for making requests
import requests

#Define some constants
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

        self.send_response(200, 'Message reversed')

        print('\n**************************************\n')

        #Print message from capitalizer
        print(
            f'Message from Capitalizer at {client_ip}:{client_port}: {body.decode(encoding)}')

        #Reverse the message
        modified_body = body.decode(encoding)[::-1]

        print(f'Reversed message: {modified_body}')

        # Reverse the text and send it back to Capitalizer
        response.write(modified_body.encode(encoding))

        self.end_headers()
        print('______________________________________\n')
        self.wfile.write(response.getvalue())


# Function for starting the server
def execute_server():
    # Create server to listen on all available IP addresses on the specified port
    with ThreadingHTTPServer(('', rc.REVERSER_PORT), RequestHandler) as httpd:
        print("Reverser serving on port ", rc.REVERSER_PORT)
        httpd.serve_forever()


def main():
    print('______________________________________\n')
    print('-------------HTTP REVERSER-------------\n')
    print('______________________________________\n')
    execute_server()


if __name__ == '__main__':
    main()
