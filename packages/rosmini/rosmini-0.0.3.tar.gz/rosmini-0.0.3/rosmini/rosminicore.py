
from collections import defaultdict
import threading
import socket

    
    

class rosminicore_organizer():
    topic_dict = defaultdict(bool) # "/topic" -> (ip, port)
    ports = []
    
    def add_topic(self, topic, ip):
        if(topic in self.topic_dict):
            return self.topic_dict[topic]
        port = self.ports[-1] + 1 if len(self.ports) > 0 else 9000
        if(port > 9999):
            port = 9000
        self.topic_dict[topic] = (ip, port)
        self.ports.append(port)
        return self.topic_dict[topic]

        
class message_class:
    len_start_bytes = 8
    start_bytes = b'rosmini!'
    len_header_bytes = 4
    # header bytes should be the len of the topic name
    start_bytes_read_topics = b'rmtopic!'




class rosminicore_receive():
    def __init__(self, ip="", port=6464):
        UDP_IP = ip
        UDP_PORT = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.sock.bind((UDP_IP, UDP_PORT))
    
    def read(self):
        data, addr = self.sock.recvfrom(message_class.len_start_bytes, socket.MSG_WAITALL)
        print(str(addr) + ' is trying to connect')
        if data:
            if data.decode() == message_class.start_bytes.decode():
                data, addr = self.sock.recvfrom(message_class.len_header_bytes, socket.MSG_WAITALL)
                if data:
                    len_topic = int(data.decode())
                    print('Topic length: ' + str(len_topic))
                    print(data)
                    data, addr = self.sock.recvfrom(len_topic, socket.MSG_WAITALL)
                    if data:
                        topic = str(data.decode())
                        print(str(addr) + ' registered on topic ' + topic)
                        ip, port = rosminicore_topics.add_topic(topic, addr[0])
                        message = str((ip, port))
                        len_message = len(message)
                        message_bytes = bytes(message, encoding='utf8')
                        self.sock.sendto(bytes(str(len_message), encoding='utf8').ljust(4, b' '), addr)
                        self.sock.sendto(message_bytes, addr)
            elif data.decode() == message_class.start_bytes_read_topics.decode():
                print(rosminicore_organizer.topic_dict.items())
                message = str(rosminicore_topics.topic_dict.items())
                len_message = len(message)
                self.sock.sendto(bytes(str(len_message), encoding='utf8').ljust(4, b' '), addr)
                self.sock.sendto(bytes(message, encoding='utf8'), addr)
                    
    
    def close(self):
        self.sock.close()



lock = threading.Lock()
rosminicore_topics = rosminicore_organizer()
import time

def main():
    print(socket.gethostname())

    rosminicore_connection = rosminicore_receive(socket.gethostname(), 6464)
            
    def listen_trigger_data():
        global trigger
        while True:
            ok = rosminicore_connection.read()



    s = threading.Thread(target=listen_trigger_data)
    s.daemon = True
    s.start()

    print('Starting')
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('Closing')
            rosminicore_connection.close()
            exit()
        except:
            print('Closing')
            rosminicore_connection.close()
            exit()

        
        


if __name__ == "__main__":
    main()