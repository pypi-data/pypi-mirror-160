# implement a roscore like node
# it should be able to start a socket server and receive data from N clients
# it receives the name of a topic and if it is subbing or publishing
# if it is subbing, sends back the IP and port of the node that publishes the topic
# if it is publishing, it should remember the IP and port of the node

import socket
import time
from threading import Thread

publishing_clients = {}


class message_class:
    len_start_bytes = 8
    start_bytes = b'rosmini!'
    len_header_bytes = 2
    # header bytes should be the len of the topic name + if it is publishing or subscribing (0 or 1)




def server(publishing_clients):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 6464))
    s.listen(5)

    while True:
        try:
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established!")
            t = Thread(target=handleClient, args=(clientsocket, address, publishing_clients))
            t.daemon = True
            t.start()
        except KeyboardInterrupt:
            print('Server closed')
            s.close()
            exit()
        except:
            print('Server closed')
            s.close()
            exit()

def handleClient(clientsocket, address, publishing_clients):
    last_send = time.time()
    try:
        data = clientsocket.recv(message_class.len_start_bytes)
        if data:
            if data.decode() == message_class.start_bytes.decode():
                data = clientsocket.recv(message_class.len_header_bytes)
                if data:
                    header = data.decode()
                    topic_name = header[:len(header) - 1]
                    if header[-1] == '0':
                        # publishing
                        if topic_name in publishing_clients:
                            clientsocket.sendall(bytes(publishing_clients[topic_name], 'utf-8'))
                        else:
                            publishing_clients[topic_name] = address
                    else:
                        # subscribing
                        pass
        else:
            clientsocket.close()
            exit()

    except KeyboardInterrupt:
        clientsocket.close()
        exit()
    except:
        clientsocket.close()
        exit()



if __name__ == "__main__":
    
    server(publishing_clients)