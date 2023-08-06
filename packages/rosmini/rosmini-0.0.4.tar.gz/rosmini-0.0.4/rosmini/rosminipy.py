import socket
import time

import ast
import select
from threading import Thread


ANY = "0.0.0.0"
SENDERPORT = 32000
MCAST_ADDR = "237.252.249.227"


def communicate_rosminicore(sock, topic):
    topic_bytes = bytes(topic, encoding='utf8')
    # size of len_topic_bytes should be 4 bytes (int)
    # zero padding is added to the beginning of the len_topic_bytes
    len_topic_bytes = bytes(str(len(topic)), encoding='utf8')
    len_topic_bytes = len_topic_bytes.ljust(4, b' ')
    print(len(topic), len_topic_bytes)
    message = b'rosmini!' + b'\n' + len_topic_bytes + b'\n' + topic_bytes
    sock.sendall(b'rosmini!')
    sock.sendall(len_topic_bytes)
    sock.sendall(topic_bytes)
    data, rosminicore_addr = sock.recvfrom(4)
    if data:
        len_topic = int(data.decode())
        data, rosminicore_addr = sock.recvfrom(len_topic, socket.MSG_WAITALL)
        if data:
            ip_port = data.decode()
            pub_ip, pub_port = ast.literal_eval(ip_port)
            print('Topic registered: ' + topic + ' on ' + pub_ip + ':' + str(pub_port))
            return pub_port
    return False

def assign_node(topic):
    sock_rosminicore = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock_rosminicore.bind((socket.gethostname(), 6464))
    sock_rosminicore.connect((socket.gethostname(), 6464))
    pub_port = communicate_rosminicore(sock_rosminicore, topic)
    sock_rosminicore.close()
    if(not pub_port):
        print("Topic could not be registered")
        return
    return pub_port


class Publisher:

    def __init__(self, topic):

        pub_port = assign_node(topic)

        self.MCAST_PORT = pub_port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
            socket.IPPROTO_UDP)
        self.sock.bind((ANY, 0))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



    def send(self, data):
        data_bytes = bytes(str(data), encoding='utf8')
        len_data_bytes = bytes(str(len(data_bytes)), encoding='utf8').ljust(16, b' ')
        self.sock.sendto(len_data_bytes, (MCAST_ADDR, self.MCAST_PORT))
        self.sock.sendto(bytes(str(data), encoding='utf8'), (MCAST_ADDR, self.MCAST_PORT))
        print(bytes(str(data), encoding='utf8'))

class Subscriber:

    def __init__(self, topic, callback=None):

        pub_port = assign_node(topic)

        self.MCAST_PORT = pub_port

        #create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        #allow multiple sockets to use the same PORT number
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        #Bind to the port that we know will receive multicast data
        self.sock.bind((ANY, self.MCAST_PORT))
        #tell the kernel that we are a multicast socket
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        #Tell the kernel that we want to add ourselves to a multicast group
        #The address for the multicast group is the third param
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY))

        if(callback):
            self.callback = callback
            t = Thread(target=self.receive_loop)
            t.daemon = True
            t.start()
            

    def receive(self):
        data, addr = self.sock.recvfrom(16)
        len_data = int(data.decode())
        print(len_data)
        data, addr = self.sock.recvfrom(len_data, socket.MSG_WAITALL)
        return data.decode('utf-8')
    
    def empty(self):
        input = [self.sock]
        while 1:
            inputready, o, e = select.select(input,[],[], 0.0)
            if len(inputready)==0: break
            for s in inputready: s.recv(1)
        
    def receive_loop(self):
        while True:
            data = self.receive()
            self.callback(data)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('topic', type=str)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    topic = args.topic
    if args.publish:
        pub = Publisher(topic)
        print('sending messages to topic: ' + topic)
        while True:
            print('Sending message')
            # pub.send(b'Hi' + b' ' + bytes(str(time.time()), encoding='utf8'))
            pub.send("E lá vamos nós")
            time.sleep(0.1)

    
    else:
        def callback(data):
            print(data)
        sub = Subscriber(topic, callback)
        print('getting messages from topic: ' + topic)
        while True:
            pass
    