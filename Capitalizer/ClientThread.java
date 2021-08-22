package Capitalizer;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class ClientThread extends Thread {
    private Socket clientSocket, reverserSocket;
    private String encodingFormat;
    private String clientAddress;
    private Integer clientPort;

    public ClientThread(Socket clientSocket, Socket reverserSocket, String encodingFormat) {
        this.clientSocket = clientSocket;
        this.reverserSocket = reverserSocket;
        this.encodingFormat = encodingFormat;
        this.clientAddress = clientSocket.getInetAddress().toString().substring(1);
        this.clientPort = clientSocket.getPort();
    }

    public void run() {
        try {
            // Object to read client input
            InputStream inputStream = clientSocket.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream, encodingFormat));

            // Output stream
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(clientSocket.getOutputStream(),
                    encodingFormat);
            // Output stream to socket and flush buffer
            PrintWriter printWriter = new PrintWriter(outputStreamWriter, true);

            String clientText = "";

            do {
                clientText = bufferedReader.readLine();
                String allCapsText = clientText.toUpperCase();

                // If the client isn't quitting, print message
                if (!clientText.equals("0")) {
                    System.out.println("______________________________________\n");
                    // Print client text
                    System.out.println("Message from the reader at " + clientAddress + ":" + clientPort + ": "
                            + clientText + "\n");
                    // Print modified text
                    System.out.println("Message to reverser: " + allCapsText + "\n");
                    // Send capitalizer response through socket
                    printWriter.println("40 - MSG OK -> " + allCapsText);

                    // Send message through socket to the reverser
                    ReverserClient reverserClient = new ReverserClient(reverserSocket, this.encodingFormat);
                    String reverserResponse = reverserClient.sendMessageToReverser(allCapsText);

                    // Print the reverser response
                    System.out.println("Reverser response: " + reverserResponse);

                    System.out.println("______________________________________\n");

                    // Send reverser response through socket
                    printWriter.println(reverserResponse + "\n");
                }
            } while (!clientText.equals("0"));

            // Send message through socket to the reverser
            ReverserClient reverserClient = new ReverserClient(reverserSocket, this.encodingFormat);
            String reverserResponse = reverserClient.sendMessageToReverser(clientText);

            // Print the reverser response
            System.out.println("Reverser response: " + reverserResponse + "\n");

            System.out.println("Closing connection to Reverser...\n");

            System.out.println("Client with address " + clientSocket.getInetAddress().toString().substring(1)
                    + " on port " + clientSocket.getPort() + " disconnected\n");

            // Send exit response to Reader
            printWriter.println("10 - QUIT");
            clientSocket.close();

        } catch (IOException ex) {
            System.out.println("Server exception: " + ex.getLocalizedMessage());
        }
    }
}
