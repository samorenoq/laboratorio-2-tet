package Capitalizer;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class ReverserClient {
    private Socket reverserSocket;
    private String encodingFormat;

    public ReverserClient(Socket reverserSocket, String encodingFormat) {
        this.reverserSocket = reverserSocket;
        this.encodingFormat = encodingFormat;
    }

    public String sendMessageToReverser(String msg) {
        String reverserResponse = "";
        try {
            // Output stream writer
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(reverserSocket.getOutputStream());
            // Output stream to socket and flush buffer
            PrintWriter printWriter = new PrintWriter(outputStreamWriter, true);
            // Send message to reverser through socket
            printWriter.println(msg);

            // Receive reverser response
            InputStream inputStream = reverserSocket.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream, this.encodingFormat));

            reverserResponse = bufferedReader.readLine();

        } catch (UnknownHostException ex) {
            System.out.println("Server not found " + ex.getLocalizedMessage());

        } catch (IOException ex) {
            System.out.println("There was an I/O error: " + ex.getLocalizedMessage());
        }

        // Return the response from the reverser
        return reverserResponse;
    }
}
