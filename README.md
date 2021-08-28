# Laboratorio 2 - Tópicos Especiales en Telemática: HTTP
Repositorio con todo lo necesario para completar el Laboratorio 2 de Tópicos Especiales en Telemática - 2021-2

- [Laboratorio 2 - Tópicos Especiales en Telemática: HTTP](#laboratorio-2---tópicos-especiales-en-telemática-http)
  - [Estructura](#estructura)
  - [Instrucciones de uso](#instrucciones-de-uso)
  - [Ejemplo](#ejemplo)
  - [Información adicional](#información-adicional)

## Estructura
Esta aplicación tiene cuatro componentes principales:
* *HTTPClient*: el cliente, desarrollado en Python, que hace una petición HTTP al HTTPReader (que se describe más abajo). El cliente es un programa sencillo que recibe texto escrito por el usuario, verifica que no esté vacío, y lo envía al HTTPReader, que luego lo verificará y hará otra petición HTTP al HTTPCapitalizer.
* *HTTPReader*: este es el servidor con el que el cliente tiene contacto directo. Es un servicio desarrollado en Python, que corre en el puerto 50003. Su función es recibir el mensaje del cliente y verificar que sea válido. Un mensaje válido es aquel que solamente consta de letras, sin espacios, números u otros caracteres especiales. Si el mensaje es válido, el HTTPReader enviará enviará el mensaje por HTTP al HTTPCapitalizer, que luego lo enviará al HTTPReverser y, finalmente, el HTTPReader entregará la respuesta del HTTPReverser al cliente. El HTTPReader tiene un protocolo que está definido de la siguiente manera:
  * 200 -> Sending to HTTPCapitalizer: el mensaje recibido está en el formato correcto y se hará una petición HTTP al HTTPCapitalizer para que lo convierta en mayúsculas.
  * 400 -> INVALID CHARACTERS: si el mensaje del cliente contiene algún caracter no válido, la respuesta HTTP que el HTTPReader retorna al cliente es un error 400 (que es bad request) y en este caso significa que el mensaje contiene caracteres inválidos.
* *HTTPCapitalizer*: este es un servicio ubicado en otro servidor en el puerto 50004 y desarrollado en Python. Este servicio recibe peticiones HTTP del HTTPReader y convierte los mensajes en mayúscula (ejemplo: hello -> HELLO), que luego envía al HTTPReverser (que se describe más abajo) por HTTP. Luego recibe la respuesta del HTTPReverser y se la envía al HTTPReader, para que éste a su vez se la pueda enviar al cliente en su respuesta a la petición HTTP original. El protocolo de respuestas del HTTPCapitalizer está definido de la siguiente manera:
  * 200 -> Sending to HTTPReverser: este es el código de éxito del HTTPCapitalizer, que le retorna al HTTPReader que el mensaje fue exitosamente convertido a mayúsculas y se enviará al HTTPReverser. (_Nota_: es importante destacar que este servicio ya no necesita tener un componente tan importante de error handling para los mensajes del cliente, ya que el HTTPReader los filtró previamente antes de enviarlos aquí).
* *HTTPReverser*: este es el último servicio, que está en un tercer servidor en el puerto 50005 y está desarrollado en Python. El HTTPCapitalizer envía por HTTP el mensaje en mayúsculas, que luego el HTTPReverser procede a invertir (ejemplo: HELLO -> OLLEH) y lo retorna al HTTPCapitalizer, que a su vez lo retorna al HTTPReader y luego este al cliente. El protocolo está definido de la siguiente manera:
  * 200 -> Message reversed: este código se retorna cuando el mensaje ha sido correctamente reversado.

## Instrucciones de uso
En este momento hay tres instancias de EC2 en AWS, cada una con uno de los tres servicios mencionados anteriormente. A agosto 16, 2021, la información de los servidores es la siguiente:
* HTTPReader
  * IP Pública: 3.91.184.82
  * DNS: ec2-3-91-184-82.compute-1.amazonaws.com
* HTTPCapitalizer
  * IP Pública: 54.211.206.199
  * DNS: ec2-54-211-206-199.compute-1.amazonaws.com
* HTTPReverser
  * IP Pública: 54.164.81.206
  * DNS: ec2-54-164-81-206.compute-1.amazonaws.com

Para correr el cliente, correr el comando python \<_ruta a http_client.py_\>. Esto permitirá al usuario escribir mensajes que luego el HTTPHTTPClient enviará al HTTPReader por HTTP. Aquí, el cliente le pedirá al usuario ingresar un mensaje, que puede contener solamente caracteres a-z o A-Z, o que ingrese '0' para salir. Cualquier otro mensaje, que no siga esta estructura o que no sea el mensaje de salida, generará un código 400 -> INVALID CHARACTERS por parte del HTTPReader. Por el contrario, si el mensaje es válido, el usuario verá el código 200 -> Sending to Capitalizer -> \<mensaje que escribió\> y luego el resultado final del HTTPReverser, que será Message from Reverser: \<mensaje en mayúsculas y reversado\>.

## Ejemplo

* HTTPClient

  ![plot](Example%20Images/client-example.png)

* HTTPReader
  
  ![plot](Example%20Images/reader-example.png)

* HTTPCapitalizer
  
  ![plot](Example%20Images/capitalizer-example.png)

* HTTPReverser
  
  ![plot](Example%20Images/reverser-example.png)


## Información adicional

* Este es un sistema distribuido y las conexiones entre cualquier par de servicios funcionan como una arquitectura cliente/servidor separada. Por ejemplo, entre HTTPClient y HTTPReader hay una arquitectura cliente/servidor en la que HTTPClient es el cliente y HTTPReader es el servidor. Entre HTTPReader y HTTPCapitalizer también hay una arquitectura cliente/servidor en la que HTTPReader es el cliente y HTTPCapitalizer es el servidor. Entre HTTPCapitalizer y HTTPReverser también hay una arquitectura cliente/servidor en la que el HTTPCapitalizer es el cliente y el HTTPReverser el servidor.
* En este caso, a diferencia del laboratorio pasado, no toca definir sockets entre los servicios, sino que cada uno de los servidores está activamente escuchando peticiones HTTP y responde cuando reciba alguna. Esto implica que no ocurre ningún error si se desconecta el cliente y, por ende, no hay que enviar el comando de EXIT a los servidores para desconectar el cliente, porque ya no necesitan cerrar el socket, como en el laboratorio 1, sino que simplemente el cliente hace peticiones y se desconecta cuando quiera.
* Como no hay que mantener abierto un socket por cada cliente, los servidores procesan la respuesta a medida que les llega por HTTP, sin necesidad de esperar a que otro cliente se desconecte antes.
* En las tres instancias EC2 de AWS en las que están el HTTPReader, HTTPCapitalizer y HTTPReverser, se usó PM2 para la gestión de procesos, para correrlos como daemon en segundo plano y mantenerlos activos.
* Todas las peticiones HTTP que se hicieron entre todos los servicios fueron peticiones POST.
* La librería de Python que se usó para hacer peticiones fue _requests_
* La librería de Python que se usó para correr el servidor fue http.server, y los módulos usados fueron ThreadingHTTPServer para correr el servidor y BaseHTTPRequestHandler que se usó para crear otra clase que heredara de esta para gestionar las peticiones que llegan de la manera apropiada según el servicio.