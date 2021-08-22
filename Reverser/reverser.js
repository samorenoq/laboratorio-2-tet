const net = require("net");

const HOST = "172.31.71.163"; //AWS instance private IP
const PORT = 50002;
const ENCODING = "utf8";
const EXIT = 0;

console.log("______________________________________\n");
console.log("_______________REVERSER_______________\n");
console.log("______________________________________\n");

//Create a new node server
const reverser = net.createServer();
reverser.listen(PORT, HOST);
console.log(`Reverser is listening on port ${PORT}\n`);

//Event to handle when the client connects
reverser.on("connection", (clientSocket) => {
  const clientAddress = clientSocket.remoteAddress;
  const clientPort = clientSocket.remotePort;
  console.log(
    `\n${clientAddress} has connected using their port ${clientPort}\n`
  );

  //Handle data received from the client
  clientSocket.on("data", (data) => {
    //If the client is not quitting
    if (data.toString(ENCODING) != EXIT) {
      console.log("______________________________________\n");

      //Print message from the capitalizer
      console.log(
        `Message from the capitalizer at ${clientAddress}:${clientPort}: ${data.toString(
          ENCODING
        )}`
      );

      //Reverse string and send back through socket
      const reversedString = data
        .toString(ENCODING) //Decode
        .split("") //Convert to array of chars
        .reverse() //Reverse array order
        .join("") //Convert array back to string
        .trim(); //Remove leading and trailing whitespace

      console.log(`Reversed string: ${reversedString.trim()}`);
      console.log("______________________________________\n");

      //Send message to client through socket
      const reverserResponse = `50 - MSG OK -> ${reversedString}\n`;
      clientSocket.write(reverserResponse);
    } else {
      //If client is quitting, send response and close socket
      clientSocket.write("10 - QUIT\n");
      clientSocket.destroy();
    }
  });

  //Handle event when the client closes the connection
  clientSocket.on("close", (data) => {
    console.log(
      `Client with address ${clientAddress} on port ${clientPort} has disconnected\n`
    );
  });
});
