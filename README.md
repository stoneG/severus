![alt text](https://raw.github.com/stoneG/severus/master/potion.png "This is more interesting then a picture of a server")
Severus
=======
a study in implementing different levels of python server abstractions. Named
after the [late wizard](http://en.wikipedia.org/wiki/Severus_Snape) that always served Mr. Potter a piece of his mind.

Repository Map
--------------
####socket
* Networking using only the *socket* library.
* Multiple process forks for each request.

####BaseHTTPServer
* Simple implementation of the *BaseHTTPServer* library server, complete with
  test file.

####print
* Two simple servers, one is a print server and the other is a repr server.
* Useful for seeing what requests clients are sending the server.

####wsgiref
* Simple WSGI server and app using the wsgiref library.
