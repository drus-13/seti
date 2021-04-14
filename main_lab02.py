from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user("andrey", "12345", "C:/Users/seses", perm="elradfmw",
                    msg_login="Welcome to FTP server!", msg_quit="Goodbye!")
authorizer.add_anonymous("C:/Users/seses", perm="elr",
                         msg_login="You are logged in to the server as a guest, so you have read and download only rights.",
                         msg_quit="Goodbye!")

handler = FTPHandler
handler.authorizer = authorizer

text = "Select the server operating mode: \n" \
       "1 - Active mode \n" \
       "2 - Passive mode \n"

while True:
    mode = input(text)
    if mode == "1" or mode == "2":
        break
    else:
        print("Expected input of one of the numbers.")

if mode == "1":
    server = FTPServer(("localhost", 1000), handler)
    server.serve_forever()
elif mode == "2":
    handler.passive_ports = range(60000, 65535)
    server = FTPServer(("localhost", 1000), handler)
    server.serve_forever()
