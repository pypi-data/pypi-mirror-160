import socket
import ast


ANY = "0.0.0.0"
SENDERPORT = 32000
MCAST_ADDR = "237.252.249.227"


def communicate_rosminicore(sock):
    sock.sendall(b'rmtopic!')
    data, rosminicore_addr = sock.recvfrom(4, socket.MSG_WAITALL)
    if data:
        len_topic = int(data.decode())
        data, rosminicore_addr = sock.recvfrom(len_topic, socket.MSG_WAITALL)
        if data:
            topic = ast.literal_eval(data.decode().split('s(')[1].split('])')[0] + ']')
            print(str(topic))



class TopicList:

    def __init__(self):

        sock_rosminicore = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock_rosminicore.bind((socket.gethostname(), 6464))
        sock_rosminicore.connect((socket.gethostname(), 6464))
        communicate_rosminicore(sock_rosminicore)

if __name__ == '__main__':
    pub = TopicList()