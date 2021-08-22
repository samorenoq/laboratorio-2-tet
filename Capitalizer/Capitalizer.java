package Capitalizer;

import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * This program receives a string from a socket and turns it into all caps.
 * Example: Input: "Hello" Output: "HELLO"
 * 
 * @author Santiago Moreno
 */
public class Capitalizer {
    public static final int capitalizerPort = 50001;
    public static final String capitalizerAddress = "172.31.7.193";

    public static final int reverserPort = 50002;
    public static final String reverserAddress = "3.239.0.55";

    public static final String encodingFormat = "UTF-8";

    public static void main(String[] args) {
        System.out.println("_______________________________________\n");
        System.out.println("______________CAPITALIZER______________\n");
        System.out.println("_______________________________________\n");
        try {
            // Create a new server socket on port 50001
            ServerSocket serverSocket = new ServerSocket(capitalizerPort, 5, InetAddress.getByName(capitalizerAddress));
            System.out.println("Capitalizer is listening on port " + capitalizerPort + "\n");

            // Accept new connections
            while (true) {
                // New client connections
                Socket clientSocket = serverSocket.accept();
                System.out.println("\n" + clientSocket.getInetAddress().toString().substring(1)
                        + " connected on their port " + clientSocket.getPort() + "\n");

                // Connect to reverser socket
                Socket reverserSocket = new Socket(reverserAddress, reverserPort);

                // Create new thread to handle client
                new ClientThread(clientSocket, reverserSocket, encodingFormat).start();
            }

        } catch (IOException ex) {
            System.out.println("Server exception: " + ex.getLocalizedMessage());
        }
    }
}